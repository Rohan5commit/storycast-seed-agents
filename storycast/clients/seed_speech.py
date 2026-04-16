from __future__ import annotations

import base64
from pathlib import Path
from uuid import uuid4

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from storycast.config import Settings
from storycast.utils import ensure_directory


class SeedSpeechClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _build_payload(self, text: str) -> dict:
        return {
            "app": {
                "appid": self.settings.byteplus_tts_app_id,
                "token": self.settings.byteplus_tts_token,
                "cluster": self.settings.byteplus_tts_cluster,
            },
            "user": {"uid": self.settings.byteplus_tts_uid},
            "audio": {
                "voice_type": self.settings.byteplus_tts_voice_type,
                "encoding": "mp3",
                "rate": 24000,
                "bitrate": 160,
                "speed": 10,
                "volume": 10,
                "pitch": 10,
            },
            "request": {
                "reqid": str(uuid4()),
                "text": text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
            },
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    def synthesize(self, text: str, output_path: Path) -> Path:
        ensure_directory(output_path.parent)
        response = httpx.post(
            self.settings.byteplus_tts_base_url,
            json=self._build_payload(text),
            timeout=120.0,
        )
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if content_type.startswith("audio/"):
            output_path.write_bytes(response.content)
            return output_path

        payload = response.json()
        audio_payload = payload.get("data") or payload.get("audio")
        if isinstance(audio_payload, dict):
            audio_payload = audio_payload.get("audio") or audio_payload.get("data")
        if not isinstance(audio_payload, str):
            raise RuntimeError(f"Seed Speech response did not include audio data: {payload}")

        output_path.write_bytes(base64.b64decode(audio_payload))
        return output_path
