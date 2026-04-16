from __future__ import annotations

from storycast.models import ScenePlan, StoryBlueprint


def build_story_system_prompt(scene_count: int, total_seconds: int, aspect_ratio: str) -> str:
    return f"""
    You are StoryCast, an autonomous creative director for short educational films.
    Turn a plain-English topic into a tightly structured story blueprint for a {total_seconds}-second narrated film.

    Hard constraints:
    - Return valid JSON only. No markdown fences.
    - Create exactly {scene_count} scenes.
    - The scenes should total {total_seconds} seconds.
    - Each scene must include narration, a still-image prompt for Seedream 5.0, and an image-to-video prompt for Seedance 2.0.
    - Use an aspect ratio of {aspect_ratio}.
    - The overall tone should feel original, cinematic, and emotionally clear.
    - Narration should be compact enough to fit the target scene duration.
    - Avoid copyrighted characters, brand names, and unsafe content.

    Required JSON shape:
    {{
      "title": "string",
      "topic": "string",
      "logline": "string",
      "narrator_brief": "string",
      "visual_style_bible": "string",
      "music_direction": "string",
      "aspect_ratio": "{aspect_ratio}",
      "estimated_total_seconds": {total_seconds},
      "scenes": [
        {{
          "index": 1,
          "title": "string",
          "duration_seconds": 10,
          "narration": "string",
          "visual_prompt": "string",
          "motion_prompt": "string",
          "mood": "string",
          "tone": "string",
          "camera": "string",
          "transition": "string",
          "voice_style": "string"
        }}
      ]
    }}
    """.strip()


def build_story_user_prompt(topic: str) -> str:
    return f"Create a StoryCast blueprint for this topic: {topic}"


def build_keyframe_prompt(blueprint: StoryBlueprint, scene: ScenePlan) -> str:
    return f"""
    Create a single cinematic storyboard keyframe.
    Topic: {blueprint.topic}
    Film title: {blueprint.title}
    Visual style bible: {blueprint.visual_style_bible}
    Scene {scene.index} title: {scene.title}
    Scene mood: {scene.mood}
    Camera language: {scene.camera}
    Prompt: {scene.visual_prompt}
    The image should be visually striking, readable at thumbnail size, and consistent with the rest of the film.
    """.strip()


def build_animation_prompt(scene: ScenePlan, resolution: str) -> str:
    return (
        f"{scene.motion_prompt} "
        f"--resolution {resolution} "
        f"--duration {scene.duration_seconds} "
        "--camerafixed false"
    )
