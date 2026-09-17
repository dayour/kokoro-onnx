---
title: Start from reproducible checkouts
---

Install Git, uv, and standard CPython 3.14. These Python forks deliberately
require `>=3.14,<3.15`. Use Node.js 24 for the JavaScript projects and this wiki.

Clone the repositories as siblings so existing uv source mappings resolve:

```powershell
git clone https://github.com/dayour/misaki.git
git clone https://github.com/dayour/kokoro.git
git clone https://github.com/dayour/kokoro-onnx.git
cd kokoro-onnx
uv sync --locked
```

The ONNX package itself does not require the other two repositories. They are
needed by the exporter and the language examples that use Misaki.

## First audio

Download a compatible ONNX model and voice bank using the commands in
[ONNX installation](onnx/installation.md), then run `uv run examples\save.py`.
For PyTorch inference, follow [Kokoro Python](kokoro/python.md).
Do not substitute the upstream PyPI release when a command specifies this fork.

## Existing environments

If both `phonemizer-fork` and `phonemizer` were installed, they may have
overwritten the same import package. The current forks share upstream
`phonemizer>=3.4.0`. In the relevant checkout:

```powershell
uv sync --locked --reinstall-package phonemizer
```

Include the extras or groups you need, such as `--extra en` in Misaki.
Prefer separate virtual environments for CPU/GPU ONNX and for model export.
Do not repair a project environment by replacing the global Python installation.
