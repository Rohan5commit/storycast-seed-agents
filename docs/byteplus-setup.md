# BytePlus Setup

This repo uses two BytePlus surfaces:

- `ModelArk` for Seed 2.0, Seedream 5.0, and Seedance 2.0.
- `BytePlus Speech / Seed Speech` for narration.

## ModelArk Settings

Official base URL from the current ModelArk quick start:

- `https://ark.ap-southeast.bytepluses.com/api/v3`

Recommended model IDs used by this repo:

- Story planning: `seed-2-0-pro-260328`
- Image generation: `seedream-5-0-260128`
- Video generation: `dreamina-seedance-2-0-260128`

Lower-cost alternatives you can swap in while iterating:

- Story planning: `seed-2-0-lite-260228`
- Image generation: `seedream-5-0-lite-260128`
- Video generation: `dreamina-seedance-2-0-fast-260128`

Export your key:

```bash
export ARK_API_KEY="your_modelark_key"
```

## Seed Speech Settings

The current HTTP TTS docs point to:

- `https://openspeech.byteoversea.com/api/v1/tts`

You need three values from the BytePlus Speech console:

- `BYTEPLUS_TTS_APP_ID`
- `BYTEPLUS_TTS_TOKEN`
- `BYTEPLUS_TTS_CLUSTER`

The legacy basic-parameters doc shows `volcano_tts_test` for test access. If your console shows a different cluster, use the console value.

Example exports:

```bash
export BYTEPLUS_TTS_APP_ID="your_app_id"
export BYTEPLUS_TTS_TOKEN="your_token"
export BYTEPLUS_TTS_CLUSTER="volcano_tts_test"
export BYTEPLUS_TTS_VOICE_TYPE="en_female_anna_mars_bigtts"
```

## Source Links

- ModelArk quick start: https://docs.byteplus.com/en/docs/ModelArk/1399008
- Model list: https://docs.byteplus.com/en/docs/ModelArk/1330310
- Pricing: https://docs.byteplus.com/docs/ModelArk/1099320
- Seed Speech overview: https://docs.byteplus.com/api/docs/byteplusvoice/TTS_Product_Overview
- Speech token creation: https://docs.byteplus.com/en/docs/speech/docs-generating-account-tokens
- TTS HTTP API: https://docs.byteplus.com/zh-CN/docs/speech/docs-http-api
- TTS request fields: https://docs.byteplus.com/en/docs/speech/docs-request-parameters-2
- Voice catalog: https://docs.byteplus.com/en/docs/speech/docs-voice-parameters-1

## Practical Notes

- Seedance 2.0 is asynchronous, so StoryCast polls the task until completion.
- StoryCast downloads every remote artifact immediately into the run folder for reproducibility.
- The final demo path should use real credentials, not mock audio or placeholder clips.
