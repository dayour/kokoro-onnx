---
slug: /
title: Kokoro speech stack wiki
description: Installation, APIs, production operations, and integration guidance for the dayour Python 3.14 Kokoro forks.
---

This wiki covers the **dayour** forks of Kokoro ONNX, Kokoro, and Misaki. It is
maintained alongside the ONNX runtime and describes the fork behavior, not an
assumption that the upstream PyPI packages contain these changes.

## Choose your entry point

| Goal | Start here |
| --- | --- |
| Generate a WAV with a lightweight ONNX runtime | [ONNX installation](onnx/installation.md) |
| Use PyTorch inference and language-aware pipelines | [Kokoro Python](kokoro/python.md) |
| Run speech synthesis in the browser | [JavaScript library](kokoro/javascript.md) |
| Control pronunciation and phoneme generation | [Misaki English](misaki/english.md) |
| Integrate narration into Remotion videos | [a2swe integration](integration/a2swe.md) |
| Download build artifacts | [Releases and checksums](releases.md) |
| Diagnose environment, model, or GPU failures | [Troubleshooting](operations/troubleshooting.md) |

## What this site does not promise

Native package availability is not a certification of every model/provider
combination. Read the [compatibility matrix](compatibility.md) before deployment.
Model weights and dictionaries are separate downloads with their own licenses.
The browser demo now uses stable React 19.3 and Vite 8.3; this documentation
site uses stable React 19.3 and Docusaurus 3.10.2.

Use the sidebar or local search to browse the full wiki. Search runs in your
browser; this site does not send documentation queries to an external AI service.

Source repositories: [kokoro-onnx](https://github.com/dayour/kokoro-onnx),
[kokoro](https://github.com/dayour/kokoro), and
[misaki](https://github.com/dayour/misaki).
