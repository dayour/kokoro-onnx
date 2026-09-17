---
title: Compatibility and release gates
---

## Python platform matrix

| Target | Package support | Important qualification |
| --- | --- | --- |
| Windows x64, Python 3.14 | Native ONNX / NumPy wheels | PyPI PyTorch builds are CPU-only |
| Linux x64, Python 3.14 | CPU and NVIDIA runtime packages | GPU requires compatible driver and libraries |
| Linux ARM64, Python 3.14 | CPU ONNX wheels | The ONNX GPU extra excludes this architecture |
| Apple Silicon macOS 14+, Python 3.14 | CPU ONNX wheels | An INT8 inference regression remains under investigation |
| Intel macOS | Not supported by this fork's native-wheel matrix | No Python 3.14 ONNX Runtime wheels |
| Python 3.13 or older / 3.15+ | Rejected by the manifests | Use a different supported environment |
| Free-threaded Python 3.14 | Not validated | Use the standard GIL-enabled interpreter |

## Important package lines

The manifests and committed lockfiles are authoritative. The upgrade baseline
includes NumPy 2.5, ONNX Runtime 1.30, PyTorch 2.14, Transformers 5.17,
Hugging Face Hub 1.31, Gradio 6.27, and TypeScript 7.0.2.
Misaki's stable spaCy 3.8 / Thinc 8 combination does not support `trf=True`.

The Kokoro web demo now pins stable React 19.3 and Vite 8.3, replacing the
earlier canary/beta versions. The documentation site and a2swe use stable
React 19.3 as well. Remotion packages must remain on the same stable version.

## Do not erase known limitations at release time

The Kokoro repository documents two existing CustomSTFT numerical failures:
reconstruction amplitude and non-hop-aligned output length. These are distinct
from its standard PyTorch inference path. A clean build does not establish that
the entire test suite is green.

Release notes must identify the tested platform, source SHA, model/provider
coverage, skipped checks, and remaining limitations. Use prerelease labeling
when the intended production gates are not met.
