from pathlib import Path

from storycast.ffmpeg import build_concat_command, build_mux_command


def test_mux_command_loops_video_to_match_audio() -> None:
    command = build_mux_command(Path("scene.mp4"), Path("voice.mp3"), Path("muxed.mp4"))

    assert "-stream_loop" in command
    assert str(command[-1]) == "muxed.mp4"


def test_concat_command_uses_concat_filter() -> None:
    command = build_concat_command([Path("a.mp4"), Path("b.mp4")], Path("final.mp4"))
    filter_complex = command[command.index("-filter_complex") + 1]

    assert "concat=n=2:v=1:a=1" in filter_complex
