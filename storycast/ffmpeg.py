from __future__ import annotations

import subprocess
from pathlib import Path


def build_mux_command(video_path: Path, audio_path: Path, output_path: Path) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-stream_loop",
        "-1",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output_path),
    ]


def mux_scene_video(video_path: Path, audio_path: Path, output_path: Path) -> Path:
    cmd = build_mux_command(video_path, audio_path, output_path)
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffmpeg failed while muxing scene")
    return output_path


def build_concat_command(scene_paths: list[Path], output_path: Path) -> list[str]:
    cmd = ["ffmpeg", "-y"]
    for path in scene_paths:
        cmd.extend(["-i", str(path)])
    inputs = "".join(f"[{index}:v:0][{index}:a:0]" for index in range(len(scene_paths)))
    filter_complex = f"{inputs}concat=n={len(scene_paths)}:v=1:a=1[outv][outa]"
    cmd.extend(
        [
            "-filter_complex",
            filter_complex,
            "-map",
            "[outv]",
            "-map",
            "[outa]",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )
    return cmd


def concat_scene_videos(scene_paths: list[Path], output_path: Path) -> Path:
    cmd = build_concat_command(scene_paths, output_path)
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffmpeg failed while concatenating scenes")
    return output_path
