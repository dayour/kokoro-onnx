# kokoro-onnx

![Python Version](https://img.shields.io/badge/python-3.14-blue)
[![PyPI Release](https://img.shields.io/pypi/v/kokoro-onnx.svg)](https://pypi.org/project/kokoro-onnx/)
[![Github Model Releases](https://img.shields.io/github/v/release/thewh1teagle/kokoro-onnx)](https://github.com/thewh1teagle/kokoro-onnx/releases)
[![License](https://img.shields.io/github/license/thewh1teagle/kokoro-onnx)](https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/thewh1teagle/kokoro-onnx?style=social)](https://github.com/thewh1teagle/kokoro-onnx/stargazers)
[![PyPI Downloads](https://img.shields.io/pypi/dm/kokoro-onnx?style=plastic)](https://pypi.org/project/kokoro-onnx/)

[![ONNX Runtime](https://img.shields.io/badge/ONNX%20Runtime-%E2%89%A51.30.0-blue)](https://github.com/microsoft/onnxruntime)
![CPU](https://img.shields.io/badge/CPU-supported-brightgreen)
![GPU](https://img.shields.io/badge/GPU-supported-brightgreen)

TTS with onnx runtime based on [Kokoro-TTS](https://huggingface.co/spaces/hexgrad/Kokoro-TTS)

🚀 Version 1.0 models are out now! 🎉

<https://github.com/user-attachments/assets/00ca06e8-bbbd-4e08-bfb7-23c0acb10ef9>

## Features

- Supports multiple languages
- Fast performance near real-time on macOS M1
- Offer multiple voices
- Lightweight: ~300MB (quantized: ~80MB)

## Setup

Use this Python 3.14 fork rather than the older published release:

```console
git clone https://github.com/dayour/kokoro-onnx.git
cd kokoro-onnx
uv sync --locked
```

The commands below describe upstream package installation; they do not install
this fork until a corresponding package release is published.

```console
pip install -U kokoro-onnx
```

<details>

<summary>Instructions</summary>

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation) for isolated Python (Recommend).

```console
pip install uv
```

2. Create new project folder (you name it)
3. Run in the project folder

```console
uv init -p 3.14
uv add kokoro-onnx soundfile
```

4. Paste the contents of [`examples/save.py`](https://github.com/thewh1teagle/kokoro-onnx/blob/main/examples/save.py) in `hello.py`
5. Download the files [`kokoro-v1.0.onnx`](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx), and [`voices-v1.0.bin`](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin) and place them in the same directory.
6. Run

```console
uv run hello.py
```

You can edit the text in `hello.py`

That's it! `audio.wav` should be created.

</details>

## Examples

See [examples](examples)

### Python compatibility

The package requires CPython 3.14, NumPy 2.5.3+, and ONNX Runtime 1.30.0+; pip and uv
select these automatically. Standard (GIL-enabled) Python 3.14 is supported;
free-threaded builds are not currently tested.

Python 3.14 native wheels are available for Windows x64, Linux x64/ARM64, and
Apple Silicon macOS 14+. ONNX Runtime does not provide Python 3.14 wheels for
Intel macOS, which is not supported by this Python 3.14 release.
The `gpu` extra supports Windows/Linux x64 and installs ONNX Runtime GPU with
its CUDA 13.x and cuDNN 9.x runtime dependencies. The lock selects CUDA runtime
13.3.29 and cuDNN 9.25.1.1; native wheels are checked against the supported
platforms, so Windows does not receive a Linux-only cuBLAS release.

```powershell
uv sync --locked --extra gpu
uv run --no-sync python examples\with_cuda.py
```

An NVIDIA driver compatible with CUDA 13 is required. Runtime DLLs are preloaded
automatically, TensorRT is opt-in through `ONNX_PROVIDER`, and unavailable
requested providers fail explicitly rather than appearing to succeed on CPU.
Set `ONNX_PROVIDER=CPUExecutionProvider` to select CPU intentionally.
The CPU and GPU ONNX distributions share module files: if a CPU reinstall
overwrites the GPU module, reinstall `onnxruntime-gpu` last. This condition is
detected and reported instead of silently losing CUDA support.

The core eSpeak-based examples (including `save.py` and streaming) work on 3.14.
The exporter uses the Python 3.14 build in the sibling `..\kokoro` checkout
through its inline uv source configuration, rather than the incompatible
published `kokoro` release. Run `uv run scripts/export.py ...` after that
checkout's Python 3.14 build is ready. The exporter and Misaki language examples
use the sibling `..\misaki` Python 3.14 build through inline uv sources;
run them from this repository, for example `uv run examples/english.py`.
They do not install the incompatible published `misaki-fork` package.
These sibling sources are development tools only, not dependencies of the
published ONNX runtime package. The voice-fetch script uses PyTorch 2.14+.

The web demo uses Gradio 6.27+ and keeps text input, phoneme output, audio
playback/download, and optional 50/50 voice blending:

```console
uv run examples/app.py
```

See [BUILDING.md](BUILDING.md) for the current exporter and build-tool requirements.

## Voices

See the latest voices and languages in [Kokoro-82M/VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)

Note: It's recommend to use misaki g2p package from v1.0, see [examples](examples)

## Contribute

See [CONTRIBUTE.md](CONTRIBUTE.md)

## License

- kokoro-onnx: MIT
- kokoro model: Apache 2.0
