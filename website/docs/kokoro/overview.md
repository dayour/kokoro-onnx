---
title: Kokoro repository overview
---

[dayour/kokoro](https://github.com/dayour/kokoro) contains two distinct toolchains:

| Directory | Runtime | Role |
| --- | --- | --- |
| `kokoro` | Python 3.14 / PyTorch | Model and text-to-speech pipeline |
| `demo` | Python / Gradio | PyTorch-backed interactive demo |
| `examples` | Python | Export and usage examples |
| `kokoro.js` | Node.js / browser | Transformers.js library |
| `kokoro.js/demo` | React / Vite | Browser speech application |

The Python package requires the matching Misaki fork. The JavaScript library
has its own package manifests and lockfiles; installing the Python wheel does
not install or build JavaScript.

The default Python model path and the optional convolutional CustomSTFT export
path have different validation histories. Consult [compatibility](../compatibility.md)
before treating a successful standard inference run as proof of export parity.
