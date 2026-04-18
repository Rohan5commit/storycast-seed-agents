# Submission Package

Updated: April 18, 2026

## Submission Links

- Landing page: https://rohan5commit.github.io/storycast-seed-agents/
- Repository: https://github.com/Rohan5commit/storycast-seed-agents
- Successful GitHub render: https://github.com/Rohan5commit/storycast-seed-agents/actions/runs/24514194069
- Architecture: https://github.com/Rohan5commit/storycast-seed-agents/blob/main/docs/architecture.md
- Demo runbook: https://github.com/Rohan5commit/storycast-seed-agents/blob/main/docs/demo-runbook.md

## Recommended Challenge Area

Track 01: AI Video Agents

This is an inference from the public BetaHacks page as of April 18, 2026. StoryCast also overlaps with Content Automation, but AI Video Agents is the strongest fit.

## One-Line Pitch

StoryCast is an autonomous multimodal agent that turns a single topic into a narrated one-minute short film using the BytePlus Seed generation stack.

## Short Summary

StoryCast takes one plain-English idea like `the death of a star` and autonomously writes a scene-based narrative, generates storyboard images, synthesizes scene narration, animates each scene into video, and assembles the final film. The result is a complete explainer-style video from a single prompt.

## Longer Project Description

StoryCast is built to show what a real video agent looks like when the orchestration itself is part of the product. A user provides one topic, and the system breaks it into a structured scene blueprint with narration, visual direction, motion cues, and tone metadata. Each scene becomes a storyboard frame, each frame becomes a video clip, each scene receives narration, and the pipeline merges everything into a polished 60-second film. The full process is visible, modular, and explainable, which makes it easy to demo and easy for judges to evaluate as true agentic execution rather than a single opaque generation call.

## What Makes It Strong

- It creates a finished video artifact, not just intermediate assets.
- It makes the agent steps visible: planning, keyframing, narration, animation, and assembly.
- It is easy to understand in a two-minute demo because one input becomes one finished output.
- It is public and reproducible in GitHub, including a successful workflow render.

## Technical Stack

- `Seed 2.0`: scene planning and narrative structure
- `Seedream 5.0`: keyframe image generation
- `Seedance 2.0`: image-to-video clip generation
- `Seed Speech` or temporary fallback TTS: scene narration
- `ffmpeg`: clip muxing and final concatenation
- `FastAPI`: demo surface
- `GitHub Actions`: cloud render path inside the public repository

## Suggested Demo Video Structure

- `0:00-0:20`: Open with the finished StoryCast video output
- `0:20-1:05`: Show the user prompt, generation flow, and final result inside the app or GitHub workflow
- `1:05-1:35`: Walk through the architecture and explain the model roles
- `1:35-2:00`: Explain the future vision for education, science communication, and brand storytelling

## Current Proof Points

- Public repo with documentation and CI
- Successful end-to-end GitHub render run
- Submission landing page
- Copy-paste demo runbook

## Honest Compliance Note

The current successful public render used an `ElevenLabs` fallback for TTS because BytePlus Speech credentials were not available at run time. For strict BytePlus-only final compliance, switch the narration layer back to `Seed Speech` and rerun the pipeline with real `BYTEPLUS_TTS_APP_ID`, `BYTEPLUS_TTS_TOKEN`, and `BYTEPLUS_TTS_CLUSTER` values.