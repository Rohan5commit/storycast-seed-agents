from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    ark_api_key: str
    ark_base_url: str
    seed_story_model: str
    seedream_model: str
    seedance_model: str
    tts_provider: str
    elevenlabs_api_key: str
    elevenlabs_base_url: str
    elevenlabs_voice_id: str
    elevenlabs_model_id: str
    elevenlabs_output_format: str
    byteplus_tts_base_url: str
    byteplus_tts_app_id: str
    byteplus_tts_token: str
    byteplus_tts_cluster: str
    byteplus_tts_voice_type: str
    byteplus_tts_uid: str
    output_dir: Path
    resolution: str
    image_size: str
    scene_count: int
    duration_seconds: int
    video_aspect_ratio: str
    seedance_poll_interval_seconds: int
    seedance_poll_attempts: int

    @property
    def normalized_tts_provider(self) -> str:
        return self.tts_provider.strip().lower()

    @property
    def has_modelark(self) -> bool:
        return bool(self.ark_api_key)

    @property
    def has_seed_speech(self) -> bool:
        return bool(self.byteplus_tts_app_id and self.byteplus_tts_token and self.byteplus_tts_cluster)

    @property
    def has_elevenlabs_tts(self) -> bool:
        return bool(self.elevenlabs_api_key)


def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        ark_api_key=os.getenv("ARK_API_KEY", ""),
        ark_base_url=os.getenv("ARK_BASE_URL", "https://ark.ap-southeast.bytepluses.com/api/v3"),
        seed_story_model=os.getenv("SEED_STORY_MODEL", "seed-2-0-pro-260328"),
        seedream_model=os.getenv("SEEDREAM_MODEL", "seedream-5-0-260128"),
        seedance_model=os.getenv("SEEDANCE_MODEL", "dreamina-seedance-2-0-260128"),
        tts_provider=os.getenv("TTS_PROVIDER", "elevenlabs"),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", ""),
        elevenlabs_base_url=os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io"),
        elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"),
        elevenlabs_model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
        elevenlabs_output_format=os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"),
        byteplus_tts_base_url=os.getenv("BYTEPLUS_TTS_BASE_URL", "https://openspeech.byteoversea.com/api/v1/tts"),
        byteplus_tts_app_id=os.getenv("BYTEPLUS_TTS_APP_ID", ""),
        byteplus_tts_token=os.getenv("BYTEPLUS_TTS_TOKEN", ""),
        byteplus_tts_cluster=os.getenv("BYTEPLUS_TTS_CLUSTER", "volcano_tts_test"),
        byteplus_tts_voice_type=os.getenv("BYTEPLUS_TTS_VOICE_TYPE", "en_female_anna_mars_bigtts"),
        byteplus_tts_uid=os.getenv("BYTEPLUS_TTS_UID", "storycast-demo"),
        output_dir=Path(os.getenv("STORYCAST_OUTPUT_DIR", "runs")),
        resolution=os.getenv("STORYCAST_RESOLUTION", "720p"),
        image_size=os.getenv("STORYCAST_IMAGE_SIZE", "2K"),
        scene_count=int(os.getenv("STORYCAST_SCENE_COUNT", "6")),
        duration_seconds=int(os.getenv("STORYCAST_DURATION_SECONDS", "60")),
        video_aspect_ratio=os.getenv("STORYCAST_VIDEO_ASPECT_RATIO", "16:9"),
        seedance_poll_interval_seconds=int(os.getenv("STORYCAST_SEEDANCE_POLL_INTERVAL_SECONDS", "4")),
        seedance_poll_attempts=int(os.getenv("STORYCAST_SEEDANCE_POLL_ATTEMPTS", "60")),
    )
