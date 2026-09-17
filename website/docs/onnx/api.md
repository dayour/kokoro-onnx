---
title: ONNX Python API
---

Source: [`Kokoro`](https://github.com/dayour/kokoro-onnx/blob/main/src/kokoro_onnx/__init__.py).

## Construction

```python
Kokoro(model_path, voices_path, espeak_config=None, vocab_config=None)
Kokoro.from_session(session, voices_path, espeak_config=None, vocab_config=None)
```

`vocab_config` accepts a dictionary containing `vocab` or a JSON configuration
path. `EspeakConfig` provides optional `lib_path` and `data_path` fields.
An injected session must still match the runtime's model I/O contract.

## Synthesis

```python
audio, sample_rate = tts.create(
    text, voice, speed=1.0, lang="en-us", is_phonemes=False,
    trim=True, sentence_pause=0.25, clause_pause=0.1, continuous=False,
)
```

| Parameter | Contract |
| --- | --- |
| `voice` | Available voice name or a NumPy voice-style array |
| `speed` | Between 0.5 and 2.0 |
| `lang` | eSpeak language code when converting text |
| `is_phonemes` | Treat text as phonemes instead of running eSpeak |
| `trim` | Trim edge silence and reinsert configured inter-batch pauses |
| `sentence_pause`, `clause_pause` | Pause durations in seconds |
| `continuous` | Request overlapping-window synthesis; see timing guide |

Use `tts.get_voices()` to enumerate names and `tts.get_voice_style(name)` for
voice blending. The Gradio example blends two style arrays with equal weights.

`create_timed` accepts the same arguments and returns
`(audio, sample_rate, timings)`. `create_stream` is an async generator; it does
not accept `continuous`. Keep these return shapes distinct.

## Errors are part of the contract

Missing model/voice files, unavailable requested providers, unsupported voice
names, out-of-range speed, unusable phonemes, invalid durations, and empty or
non-finite model output are errors. Applications should display or log them
instead of writing a success-shaped silent WAV.

Integer-speed legacy graphs cannot faithfully represent fractional speeds;
the runtime warns when rounding is necessary. Re-export with a floating-point
speed input when exact fractional control is required.
