---
title: Integrating a2swe narration
---

[a2swe](https://github.com/dayour/a2swe) is a Remotion/React/TypeScript video
production toolkit. It uses the Python speech stack for approved narration,
then resamples audio and generates project-specific frame timing.

## Runtime selection

| Setting | Behavior |
| --- | --- |
| `TTS_ENGINE=auto` | Select local Kokoro |
| `TTS_ENGINE=kokoro` | PyTorch pipeline |
| `TTS_ENGINE=kokoro_onnx` | ONNX runtime with explicit model/voice-bank paths |
| `TTS_ENGINE=piper` | Optional local Piper model |
| `TTS_ENGINE=edge` | Explicit external speech service |

```powershell
$env:TTS_ENGINE = "kokoro_onnx"
$env:KOKORO_ONNX_MODEL = "C:\models\kokoro-v1.0.onnx"
$env:KOKORO_ONNX_VOICES = "C:\models\voices-v1.0.bin"
$env:ONNX_PROVIDER = "CPUExecutionProvider"
python scripts\tts_build.py
```

Run the script from a generated project using its documented Python environment.
The toolkit's English-only narration and approval gates remain in force. Do not
send narration to Edge as an automatic fallback when local inference fails.

## Applying package upgrades

Refresh the actual wheel snapshots, not just dependency version strings. Multiple
fork builds currently share package versions, so record release tags, source
commits, and wheel SHA-256 hashes. Update the template and existing projects'
locks together, and remove the old overlapping phonemizer distribution.

Version-aware cache keys should prevent old narration audio from masking a new
runtime's behavior. Validate finite, non-empty audio before caching or converting
it to PCM. Keep resampling at the application's output sample rate; changing
container metadata alone does not resample audio.

## Validation without overwriting approved deliveries

Run the existing pipeline checks, TypeScript checks, and production bundle build.
Use separate scratch paths for synthesis and QC. Preserve approved narration,
finished MP4 files, storyboards, research, and existing uncommitted work.
Rendering a bundle is not rendering a complete movie.
