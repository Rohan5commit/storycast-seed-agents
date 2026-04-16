from __future__ import annotations

import json
import time
from pathlib import Path

from byteplussdkarkruntime import Ark
from tenacity import retry, stop_after_attempt, wait_exponential

from storycast.config import Settings
from storycast.models import ScenePlan, StoryBlueprint
from storycast.prompting import build_animation_prompt, build_keyframe_prompt, build_story_system_prompt, build_story_user_prompt
from storycast.utils import coerce_to_dict, download_to_path, extract_json_object, first_present, path_to_data_url


class ModelArkClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = Ark(base_url=settings.ark_base_url, api_key=settings.ark_api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    def generate_story_blueprint(self, topic: str) -> StoryBlueprint:
        completion = self.client.chat.completions.create(
            model=self.settings.seed_story_model,
            messages=[
                {"role": "system", "content": build_story_system_prompt(self.settings.scene_count, self.settings.duration_seconds, self.settings.video_aspect_ratio)},
                {"role": "user", "content": build_story_user_prompt(topic)},
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        content = completion.choices[0].message.content
        if isinstance(content, list):
            raw = "".join(str(item) for item in content)
        else:
            raw = str(content)
        payload = json.loads(extract_json_object(raw))
        blueprint = StoryBlueprint.model_validate(payload)
        return blueprint.normalized(self.settings.duration_seconds)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    def generate_keyframe(self, blueprint: StoryBlueprint, scene: ScenePlan, output_path: Path) -> str:
        prompt = build_keyframe_prompt(blueprint, scene)
        images_response = self.client.images.generate(
            model=self.settings.seedream_model,
            prompt=prompt,
            size=self.settings.image_size,
            response_format="url",
            watermark=False,
        )
        image_url = getattr(images_response.data[0], "url", None)
        if not image_url:
            image_url = coerce_to_dict(images_response)["data"][0]["url"]
        download_to_path(image_url, output_path)
        return image_url

    def animate_scene(self, scene: ScenePlan, first_frame_path: Path, output_path: Path) -> str:
        request = self.client.content_generation.tasks.create(
            model=self.settings.seedance_model,
            content=[
                {"type": "text", "text": build_animation_prompt(scene, self.settings.resolution)},
                {"type": "image_url", "image_url": {"url": path_to_data_url(first_frame_path)}},
            ],
        )
        task_dict = coerce_to_dict(request)
        task_id = first_present(task_dict, "id", "task_id", "taskId")
        if not task_id:
            raise RuntimeError(f"Seedance task creation did not return an id: {task_dict}")

        for _ in range(self.settings.seedance_poll_attempts):
            result = self.client.content_generation.tasks.get(task_id=task_id)
            result_dict = coerce_to_dict(result)
            status = first_present(result_dict, "status", "Status")
            if status == "succeeded":
                content = result_dict.get("content", {})
                video_url = first_present(content, "video_url", "videoUrl", "VideoURL")
                if not video_url:
                    video_urls = first_present(content, "video_urls", "videoUrls", "VideoURLs")
                    if isinstance(video_urls, list) and video_urls:
                        video_url = video_urls[0]
                if not video_url:
                    raise RuntimeError(f"Seedance task succeeded without a video URL: {result_dict}")
                download_to_path(video_url, output_path)
                return video_url
            if status == "failed":
                error = result_dict.get("error") or result_dict
                raise RuntimeError(f"Seedance task failed: {error}")
            time.sleep(self.settings.seedance_poll_interval_seconds)

        raise TimeoutError(f"Timed out while waiting for Seedance task {task_id}")
