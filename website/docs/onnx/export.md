---
title: Export and model provenance
---

Run export from the ONNX checkout with sibling Kokoro and Misaki forks available.
The script's inline uv metadata selects those local sources and Python 3.14.

```powershell
uv run scripts\export.py --help
uv run scripts\export.py -c checkpoints\config.json -p checkpoints\kokoro-v1_0.pth -o kokoro-v1.0.onnx --fp16 --int8
```

Obtain configuration and checkpoint files from the same model release. The
script documents the separate v1.0 English and v1.1 Chinese sources.

## Graph requirements

The exporter uses the legacy TorchScript path intentionally, emits waveform and
duration outputs, preserves floating-point speed, and embeds model configuration
under `kokoro_config`. Legacy integer-speed graphs round fractional requests.
Duration frames correspond to 600 audio samples in this export contract.

FP16 conversion uses ONNX IR to order nested graph dependencies before ONNX
validation. INT8 and FP16 artifacts must each be exercised with real inference;
file creation or ONNX structural validation alone is insufficient.

## Weight compatibility

Recent PyTorch checkpoints can use parametrized weight-normalization keys.
The export script includes modernization for these keys. Loading mismatched keys
with `strict=False` can otherwise leave layers uninitialized and produce noise.
Inspect export diagnostics and preserve the original checkpoint.

Archive source commit, model/config hashes, voice used for parity, runtime
versions, active provider, and model precision. Do not claim waveform equivalence
between quantized and full-precision output without a suitable evaluation.

Source and exact flags: [scripts/export.py](https://github.com/dayour/kokoro-onnx/blob/main/scripts/export.py).
