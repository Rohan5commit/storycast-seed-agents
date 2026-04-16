from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ScenePlan(BaseModel):
    index: int = Field(ge=1)
    title: str
    duration_seconds: int = Field(ge=4, le=15)
    narration: str
    visual_prompt: str
    motion_prompt: str
    mood: str
    tone: str = "cinematic"
    camera: str = "gentle push-in"
    transition: str = "match cut"
    voice_style: str = "warm, confident, cinematic"


class StoryBlueprint(BaseModel):
    title: str
    topic: str
    logline: str
    narrator_brief: str
    visual_style_bible: str
    music_direction: str
    aspect_ratio: str = "16:9"
    estimated_total_seconds: int = Field(ge=20, le=120)
    scenes: list[ScenePlan]

    @model_validator(mode="after")
    def validate_scenes(self) -> "StoryBlueprint":
        if not self.scenes:
            raise ValueError("Story blueprint must include at least one scene")
        expected = list(range(1, len(self.scenes) + 1))
        actual = [scene.index for scene in self.scenes]
        if actual != expected:
            raise ValueError(f"Scene indexes must be consecutive starting at 1, got {actual}")
        return self

    def normalized(self, target_total: int) -> "StoryBlueprint":
        copy = self.model_copy(deep=True)
        delta = target_total - sum(scene.duration_seconds for scene in copy.scenes)
        if delta == 0:
            copy.estimated_total_seconds = target_total
            return copy

        step = 1 if delta > 0 else -1
        remaining = abs(delta)
        while remaining:
            changed = False
            scene_iterable = copy.scenes if step > 0 else list(reversed(copy.scenes))
            for scene in scene_iterable:
                candidate = scene.duration_seconds + step
                if 4 <= candidate <= 15:
                    scene.duration_seconds = candidate
                    remaining -= 1
                    changed = True
                    if remaining == 0:
                        break
            if not changed:
                break

        copy.estimated_total_seconds = sum(scene.duration_seconds for scene in copy.scenes)
        return copy


class SceneArtifact(BaseModel):
    scene_index: int
    title: str
    duration_seconds: int
    narration: str
    keyframe_path: str
    keyframe_source_url: str
    audio_path: str
    video_path: str
    muxed_video_path: str


class RunManifest(BaseModel):
    run_id: str
    topic: str
    created_at: str
    status: Literal["queued", "running", "completed", "failed"]
    run_dir: str
    blueprint: StoryBlueprint | None = None
    scenes: list[SceneArtifact] = Field(default_factory=list)
    final_video_path: str | None = None
    error: str | None = None
