---
title: Kokoro ONNX overview
---

`kokoro-onnx` is the MIT-licensed inference wrapper in
[dayour/kokoro-onnx](https://github.com/dayour/kokoro-onnx). It loads a compatible
ONNX model and NumPy voice archive and produces mono float32 audio at 24 kHz.

The core package supports synchronous synthesis, asynchronous chunk streaming,
punctuation-aware pauses, and duration-based phoneme timestamps when the graph
supports them. It also exposes session injection for applications that configure
ONNX Runtime themselves.

## Files you need

| Artifact | Purpose |
| --- | --- |
| Python wheel | Runtime wrapper and packaged configuration |
| ONNX graph | Model weights and inference operations |
| `voices-v1.0.bin` or compatible archive | Voice style tensors |
| Optional vocabulary configuration | Override packaged/embedded model vocabulary |

Model assets are not included in the wheel. Match voice packs, vocabulary, and
model generation rather than selecting files by extension alone.

Continue with [installation](installation.md), [API reference](api.md),
[streaming](streaming.md), or [CUDA](cuda.md).
