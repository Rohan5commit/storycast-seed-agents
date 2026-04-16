from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from storycast.clients import ModelArkClient, SeedSpeechClient
from storycast.config import Settings, get_settings
from storycast.ffmpeg import concat_scene_videos, mux_scene_video
from storycast.models import RunManifest, SceneArtifact
from storycast.utils import ensure_command, ensure_directory, slugify, write_json

ProgressCallback = Callable[[str], None]


class StoryCastPipeline:
    def __init__(
        self,
        settings: Settings | None = None,
        modelark_client: ModelArkClient | None = None,
        seed_speech_client: SeedSpeechClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.modelark_client = modelark_client or ModelArkClient(self.settings)
        self.seed_speech_client = seed_speech_client or SeedSpeechClient(self.settings)

    def run(self, topic: str, progress_callback: ProgressCallback | None = None) -> RunManifest:
        ensure_command("ffmpeg")
        if not self.settings.has_modelark:
            raise RuntimeError("ARK_API_KEY is required to run StoryCast")
        if not self.settings.has_seed_speech:
            raise RuntimeError("Seed Speech credentials are required to run StoryCast")

        run_id = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{slugify(topic)}"
        run_dir = ensure_directory(self.settings.output_dir / run_id)
        manifest = RunManifest(
            run_id=run_id,
            topic=topic,
            created_at=datetime.now(UTC).isoformat(),
            status="running",
            run_dir=str(run_dir),
        )
        self._emit(progress_callback, "Planning story blueprint with Seed 2.0")

        try:
            blueprint = self.modelark_client.generate_story_blueprint(topic)
            manifest.blueprint = blueprint
            write_json(run_dir / "blueprint.json", blueprint.model_dump(mode="json"))
            write_json(run_dir / "manifest.json", manifest.model_dump(mode="json"))

            scene_outputs: list[Path] = []
            for scene in blueprint.scenes:
                prefix = f"scene_{scene.index:02d}"
                keyframe_path = run_dir / f"{prefix}.png"
                audio_path = run_dir / f"{prefix}.mp3"
                video_path = run_dir / f"{prefix}.mp4"
                muxed_path = run_dir / f"{prefix}_muxed.mp4"

                self._emit(progress_callback, f"Scene {scene.index}: generating keyframe with Seedream 5.0")
                keyframe_url = self.modelark_client.generate_keyframe(blueprint, scene, keyframe_path)

                self._emit(progress_callback, f"Scene {scene.index}: synthesizing narration with Seed Speech")
                self.seed_speech_client.synthesize(scene.narration, audio_path)

                self._emit(progress_callback, f"Scene {scene.index}: animating clip with Seedance 2.0")
                self.modelark_client.animate_scene(scene, keyframe_path, video_path)

                self._emit(progress_callback, f"Scene {scene.index}: muxing scene with ffmpeg")
                mux_scene_video(video_path, audio_path, muxed_path)
                scene_outputs.append(muxed_path)

                manifest.scenes.append(
                    SceneArtifact(
                        scene_index=scene.index,
                        title=scene.title,
                        duration_seconds=scene.duration_seconds,
                        narration=scene.narration,
                        keyframe_path=str(keyframe_path),
                        keyframe_source_url=keyframe_url,
                        audio_path=str(audio_path),
                        video_path=str(video_path),
                        muxed_video_path=str(muxed_path),
                    )
                )
                write_json(run_dir / "manifest.json", manifest.model_dump(mode="json"))

            self._emit(progress_callback, "Stitching final film with ffmpeg")
            final_video_path = concat_scene_videos(scene_outputs, run_dir / "storycast_final.mp4")
            manifest.final_video_path = str(final_video_path)
            manifest.status = "completed"
            write_json(run_dir / "manifest.json", manifest.model_dump(mode="json"))
            self._emit(progress_callback, "StoryCast render completed")
            return manifest
        except Exception as exc:
            manifest.status = "failed"
            manifest.error = str(exc)
            write_json(run_dir / "manifest.json", manifest.model_dump(mode="json"))
            self._emit(progress_callback, f"StoryCast failed: {exc}")
            raise

    @staticmethod
    def _emit(callback: ProgressCallback | None, message: str) -> None:
        if callback is not None:
            callback(message)
