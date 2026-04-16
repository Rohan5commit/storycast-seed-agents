from __future__ import annotations

from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from storycast.config import Settings
from storycast.utils import ensure_directory


class ElevenLabsTTSClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    def synthesize(self, text: str, output_path: Path) -> Path:
        ensure_directory(output_path.parent)
        response = httpx.post(
            f"{self.settings.elevenlabs_base_url}/v1/text-to-speech/{self.settings.elevenlabs_voice_id}",
            headers={
                "xi-api-key": self.settings.elevenlabs_api_key,
                "Content-Type": "application/json",
            },
            params={"output_format": self.settings.elevenlabs_output_format},
            json={
                "text": text,
                "model_id": self.settings.elevenlabs_model_id,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return output_path
