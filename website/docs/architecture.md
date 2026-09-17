---
title: Architecture and repository boundaries
---

| Component | Responsibility | Input | Output |
| --- | --- | --- | --- |
| Misaki | Language-specific grapheme-to-phoneme conversion | Text and language settings | Phonemes, language-dependent metadata |
| Kokoro Python | PyTorch model and language pipeline | Text, voice, speed | Pipeline results with audio |
| Kokoro ONNX | Runtime inference, chunking, pauses, optional timings | Text or phonemes, model, voice bank | Float32 audio at 24 kHz |
| Kokoro JS | Transformers.js model execution | Text, voice, device | RawAudio or streamed results |
| a2swe | Narration, resampling, timeline, Remotion rendering | Approved narration and project configuration | Video assets and timing |

The ONNX runtime normally phonemizes through eSpeak. Misaki-backed examples
generate phonemes separately and call `create(..., is_phonemes=True)`.
PyTorch export writes the model graph; it is not required on the target ONNX
inference machine.

## Model contracts

ONNX imports accept legacy `tokens` or newer `input_ids` inputs. The runtime
inspects input dtypes rather than assuming every model uses the same speed type.
An explicit vocabulary overrides embedded model metadata, which overrides the
packaged vocabulary.

Duration-aware graphs enable phoneme timestamps and continuous synthesis.
Legacy waveform-only graphs still synthesize speech, but cannot supply genuine
model-derived phoneme timings.

## Ownership boundaries

Application code owns worker lifetime, generated audio URLs, model paths, caching,
and user-facing error reporting. A successful package import does not prove that a
model was loaded, the selected provider initialized, or the returned audio is valid.
Keep these checks distinct in production logs.

Implementation: [ONNX package](https://github.com/dayour/kokoro-onnx/tree/main/src/kokoro_onnx),
[Kokoro pipeline](https://github.com/dayour/kokoro/blob/main/kokoro/pipeline.py),
[Misaki language modules](https://github.com/dayour/misaki/tree/main/misaki).
