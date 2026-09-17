---
title: Audio quality, storage, and caching
---

## Validate before encoding

Check non-empty sample arrays, finite values, expected channel count, and a
positive sample rate. Report a model/provider failure before normalization or
trimming can hide it. Silence, clipping, and invalid floating-point values are
different defects and should not share a generic success message.

Kokoro normally produces 24 kHz audio. a2swe uses a 48 kHz output timeline.
Use a real resampler for conversion, and verify saved WAV duration and sample
rate by reading the file back.

## Reproducible cache identity

Cache identity should include engine, text, voice, speed, model/voice fingerprints,
package build identity, and relevant provider settings. A cache hit must not
be used as evidence that an upgraded model executed successfully.
Write completed cache entries atomically so failures do not leave reusable
partial files.

## Timing and evaluation

Inspect perceptual quality, pronunciation, joins, duration, and clipping.
Quantized waveform correlation can be misleading because small phase or duration
changes shift samples. Use a quality evaluation appropriate to speech rather
than asserting that differently quantized waveforms must be numerically identical.

Keep generated media and model assets out of source commits unless deliberately
licensed and distributed. Record hashes and provenance in release/QC evidence.
