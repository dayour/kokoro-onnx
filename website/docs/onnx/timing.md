---
title: Phoneme timings and continuous synthesis
---

```python
audio, sample_rate, timings = tts.create_timed(
    "Speech with model-derived phoneme timings.",
    voice="af_heart",
)
for timing in timings:
    print(timing.phoneme, timing.start, timing.end)
```

`Timing` records contain a phoneme and start/end times in seconds. They are
available only for graphs exposing a `duration` output. A legacy graph returns
an empty timing list; do not turn an empty result into guessed word alignment.

Duration vectors must be finite, non-negative, and have a positive total.
Invalid vectors are reported explicitly. These timings describe model phonemes,
not independently measured forced alignment or human-verified subtitle boundaries.

## Continuous mode

Passing `continuous=True` requests overlapping windows to retain prosody across
long text. The method documentation estimates approximately 1.4 times the
inference work. Treat that as an implementation estimate, not a hardware benchmark.
Use a duration-capable export and inspect the actual timings and audio.

For a2swe, retain its existing frame-timing contract unless intentionally migrating
it. Converting seconds to frames requires consistent rounding, frame rate, and
inclusive/exclusive boundary rules.

Source: [sliding synthesis and Timing](https://github.com/dayour/kokoro-onnx/blob/main/src/kokoro_onnx/sliding.py).
