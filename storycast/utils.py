from __future__ import annotations

import base64
import json
import mimetypes
import re
import shutil
from pathlib import Path
from typing import Any

import httpx


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:48] or "storycast"


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: Any) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def extract_json_object(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned)
        cleaned = re.sub(r"```$", "", cleaned).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Could not find JSON object in model response: {raw}")
    return cleaned[start : end + 1]


def download_to_path(url: str, destination: Path) -> Path:
    ensure_directory(destination.parent)
    with httpx.Client(follow_redirects=True, timeout=120.0) as client:
        response = client.get(url)
        response.raise_for_status()
        destination.write_bytes(response.content)
    return destination


def path_to_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def ensure_command(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required command `{name}` was not found in PATH")


def coerce_to_dict(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: coerce_to_dict(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [coerce_to_dict(item) for item in value]
    if hasattr(value, "model_dump"):
        return coerce_to_dict(value.model_dump())
    if hasattr(value, "dict"):
        return coerce_to_dict(value.dict())
    if hasattr(value, "__dict__"):
        return {
            key: coerce_to_dict(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return value


def first_present(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return mapping[key]
    return None
