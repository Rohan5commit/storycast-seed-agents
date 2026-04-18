# StoryCast

[![CI](https://github.com/Rohan5commit/storycast-seed-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/Rohan5commit/storycast-seed-agents/actions/workflows/ci.yml)

StoryCast is an autonomous multimodal storytelling agent built for the Beta University AI Lab: Seed Agents Challenge. Give it a single topic such as `the death of a star`, and it turns that idea into a narrated, visual 60-second short film using the BytePlus Seed stack end to end.

The project is intentionally shaped for the current judging rubric: strong video output, obvious agentic execution, and a demo flow that is easy to show live.

## Submission Links

- Landing page: https://rohan5commit.github.io/storycast-seed-agents/
- Successful GitHub render: https://github.com/Rohan5commit/storycast-seed-agents/actions/runs/24514194069
- Submission package: docs/submission-package.md
- Demo runbook: docs/demo-runbook.md

## Why This Fits The Challenge

- `Seed 2.0` writes a structured six-scene story blueprint with narration, visual prompts, motion prompts, and tone metadata.
- `Seedream 5.0` generates one keyframe per scene, turning the blueprint into a storyboard.
- `Seedance 2.0` animates each keyframe in image-to-video mode.
- A TTS layer generates voiceover for every scene. The repo supports both `Seed Speech` and a temporary `ElevenLabs` fallback.
- `ffmpeg` stitches the clips together and muxes scene audio into a final film.
- A FastAPI web app gives you a clean demo surface for judges, and a CLI gives you a dead-simple fallback.
- A GitHub Actions workflow lets you run renders entirely inside GitHub once repo secrets are configured.

## Compliance Note

The current repo supports `ElevenLabs` as a development fallback because getting Seed Speech activated can take longer than getting a ModelArk key. For a strict final challenge submission, switch `TTS_PROVIDER=seed_speech` and use real BytePlus Speech credentials.

## Product Flow

```mermaid
flowchart LR
    A[Topic] --> B[Seed 2.0 story director]
    B --> C[Scene blueprint JSON]
    C --> D[Seedream 5.0 keyframes]
    C --> E[TTS narration]
    D --> F[Seedance 2.0 I2V clips]
    E --> G[Scene muxing with ffmpeg]
    F --> G
    G --> H[Final 60-second StoryCast video]
```

## Quick Start

1. Create a virtual environment and install dependencies.
2. Add your credentials in `.env` or exported environment variables.
3. Run the CLI or web app.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
storycast create --topic "the death of a star"
```

To launch the demo UI:

```bash
storycast serve --reload
```

The web app starts on `http://127.0.0.1:8000` by default.

## GitHub-Only Render Path

If you want the generation run itself to happen entirely in GitHub:

1. Add repo secret `ARK_API_KEY`.
2. Add either `ELEVENLABS_API_KEY` or the BytePlus Speech secrets.
3. Open `Actions` and run `generate-storycast` with a topic and `tts_provider` choice.
4. Download the uploaded `runs/` artifact from the workflow run.

## Configuration

Core settings live in `.env.example`.

- `ARK_API_KEY`: ModelArk API key for Seed 2.0, Seedream 5.0, and Seedance 2.0.
- `TTS_PROVIDER`: `elevenlabs` or `seed_speech`.
- `ELEVENLABS_API_KEY`: Free-plan fallback TTS API key.
- `ELEVENLABS_VOICE_ID`: Defaults to ElevenLabs “George” (`JBFqnCBsd6RMkjVDRZzb`).
- `ELEVENLABS_MODEL_ID`: Defaults to `eleven_multilingual_v2`.
- `SEED_STORY_MODEL`: Defaults to `seed-2-0-pro-260328`.
- `SEEDREAM_MODEL`: Defaults to `seedream-5-0-260128`.
- `SEEDANCE_MODEL`: Defaults to `dreamina-seedance-2-0-260128`.
- `BYTEPLUS_TTS_APP_ID`, `BYTEPLUS_TTS_TOKEN`, `BYTEPLUS_TTS_CLUSTER`: Seed Speech credentials.
- `BYTEPLUS_TTS_VOICE_TYPE`: Narrator voice selection.

See [docs/byteplus-setup.md](docs/byteplus-setup.md) for the BytePlus stack and [docs/fallback-tts.md](docs/fallback-tts.md) for the free ElevenLabs setup.

## Demo Surfaces

- `storycast create --topic "..."`: Runs the full pipeline from the terminal.
- `storycast serve`: Starts the FastAPI app with a launch-ready interface for judges.
- `Actions > generate-storycast`: Runs the pipeline in GitHub with repository secrets.
- `GET /health`: Lightweight status endpoint.
- `POST /api/storycasts`: Creates a StoryCast job.
- `GET /api/storycasts/{job_id}`: Polls job status and returns the generated manifest.

## Repo Structure

```text
.
├── .github/workflows/ci.yml
├── .github/workflows/generate-storycast.yml
├── .env.example
├── Dockerfile
├── Makefile
├── README.md
├── docs/
│   ├── architecture.md
│   ├── byteplus-setup.md
│   ├── demo-script.md
│   ├── fallback-tts.md
│   └── submission-checklist.md
├── main.py
├── pyproject.toml
├── storycast/
│   ├── api.py
│   ├── cli.py
│   ├── config.py
│   ├── ffmpeg.py
│   ├── models.py
│   ├── pipeline.py
│   ├── prompting.py
│   ├── utils.py
│   ├── clients/
│   │   ├── elevenlabs_tts.py
│   │   ├── modelark.py
│   │   └── seed_speech.py
│   └── web/
│       ├── static/
│       └── templates/
└── tests/
    ├── test_ffmpeg.py
    ├── test_models.py
    └── test_utils.py
```

## Docs For The Submission

- [Architecture](docs/architecture.md)
- [BytePlus Setup](docs/byteplus-setup.md)
- [Free Fallback TTS Setup](docs/fallback-tts.md)
- [2-Minute Demo Script](docs/demo-script.md)
- [Submission Checklist](docs/submission-checklist.md)
- [Submission Package](docs/submission-package.md)
- [Demo Runbook](docs/demo-runbook.md)

## Notes On Challenge Positioning

As of April 16, 2026, the public challenge page shows four challenge areas plus six track-winner specialty prizes. This repo positions StoryCast as a creative multimodal entry that still clearly demonstrates video-agent behavior and full BytePlus Seed usage.

## References

- Beta University challenge page: https://www.betahacks.org/
- BytePlus ModelArk quick start: https://docs.byteplus.com/en/docs/ModelArk/1399008
- BytePlus Model list: https://docs.byteplus.com/en/docs/ModelArk/1330310
- BytePlus pricing: https://docs.byteplus.com/docs/ModelArk/1099320
- Seed Speech TTS overview: https://docs.byteplus.com/api/docs/byteplusvoice/TTS_Product_Overview
- BytePlus Speech TTS HTTP API: https://docs.byteplus.com/zh-CN/docs/speech/docs-http-api
- BytePlus Speech basic parameters: https://docs.byteplus.com/en/docs/speech/docs-request-parameters-2
- Supported Seed Speech voices: https://docs.byteplus.com/en/docs/speech/docs-voice-parameters-1
- ElevenLabs API quickstart: https://elevenlabs.io/docs/eleven-api/guides/cookbooks/text-to-speech
- ElevenLabs API pricing: https://elevenlabs.io/pricing/api
- ElevenLabs Create speech API: https://elevenlabs.io/docs/api-reference/text-to-speech/convert