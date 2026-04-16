# Free Fallback TTS Setup

StoryCast supports `ElevenLabs` as a temporary fallback when you do not yet have Seed Speech activated.

## Why ElevenLabs

Official ElevenLabs docs currently state:

- API access is included in all plans, including the free plan.
- The free plan currently gives `10,000` characters per month with no credit card required.

## Get The API Key

1. Sign up or log in at `https://elevenlabs.io`.
2. Open the API keys page: `https://elevenlabs.io/app/developers/api-keys`.
3. Create an API key and store it as `ELEVENLABS_API_KEY`.

Official docs:

- Quickstart: https://elevenlabs.io/docs/eleven-api/guides/cookbooks/text-to-speech
- Pricing: https://elevenlabs.io/pricing/api
- Help center API auth: https://help.elevenlabs.io/hc/en-us/sections/14163158308369-API

## Default Voice Setup

StoryCast defaults to ElevenLabs voice `George` with voice ID `JBFqnCBsd6RMkjVDRZzb`, which is the ID shown in the official quickstart.

If you want a different voice:

1. Open `My Voices` in ElevenLabs.
2. Click the three-dot menu on a voice.
3. Choose `Copy voice ID`.
4. Set `ELEVENLABS_VOICE_ID`.

Voice ID docs:

- https://help.elevenlabs.io/hc/en-us/articles/14599760033937-How-do-I-find-the-voice-ID-of-my-voices-via-the-website-and-API

## GitHub Setup

For GitHub Actions, add this repo secret:

- `ELEVENLABS_API_KEY`

Then run the `generate-storycast` workflow with `tts_provider=elevenlabs`.

## Important Note

ElevenLabs is a development fallback for this repo. For strict BytePlus-only challenge compliance, switch back to `TTS_PROVIDER=seed_speech` before your final official submission.
