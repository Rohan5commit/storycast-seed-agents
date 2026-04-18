# Demo Runbook

Updated: April 18, 2026

This is the exact two-minute structure to record for submission.

## Recording Goal

Show one clear user flow, prove that StoryCast is an agentic system rather than a single generation call, and end on a believable post-hackathon vision.

## Before Recording

- Keep the repository homepage open: https://rohan5commit.github.io/storycast-seed-agents/
- Keep the successful GitHub render run open as backup: https://github.com/Rohan5commit/storycast-seed-agents/actions/runs/24514194069
- Keep the app UI or CLI ready with a prompt like `the death of a star`
- If a fully live generation is too slow, show the successful render output first and then explain the pipeline

## Script

### 0:00 to 0:15

On screen: final StoryCast video clip already playing.

Say:

"StoryCast turns one plain-English topic into a narrated short film. You give it one idea, and it writes the story, builds the visuals, voices the narration, animates the scenes, and edits the final video automatically."

### 0:15 to 0:55

On screen: prompt input and generation flow.

Say:

"Here the user enters a topic like `the death of a star`. StoryCast then triggers a multi-step agent pipeline: first it plans scenes and narration, then it generates storyboard keyframes, then it creates narration for each scene, then it animates those images into video clips, and finally it stitches everything into one finished film."

### 0:55 to 1:20

On screen: architecture page or README diagram.

Say:

"The key point is that the agent work is explicit. Seed 2.0 outputs a structured story blueprint, Seedream 5.0 generates the visual keyframes, Seedance 2.0 handles image-to-video generation, the narration layer voices each scene, and ffmpeg muxes and concatenates the final result. That makes the system modular, inspectable, and easy to debug."

### 1:20 to 1:45

On screen: manifest, scene assets, or workflow artifact.

Say:

"Every run produces scene-level assets and a final manifest, so we can inspect exactly what the agent produced at each stage. That gives the system a strong developer experience in addition to a polished final video."

### 1:45 to 2:00

On screen: final video again.

Say:

"After the hackathon, StoryCast becomes an always-on explainer engine for education, science media, and branded storytelling. The same pipeline can expand into multi-format outputs like shorts, lesson clips, and interactive topic journeys."

## Backup Plan

If a live render does not finish in time, use the already successful GitHub Actions run as the proof artifact and keep the rest of the demo focused on the agent pipeline and the final video output. For a short judging video, clarity matters more than forcing a full live render.