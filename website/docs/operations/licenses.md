---
title: Licenses, privacy, and distribution
---

| Component | License / authority |
| --- | --- |
| Kokoro ONNX wrapper | MIT; see its repository LICENSE |
| Kokoro model and associated upstream project | Apache-2.0; verify the exact model/repository license |
| Misaki | Apache-2.0; retain upstream notices |
| Downloaded dictionaries and third-party packages | Their individual licenses apply |
| a2swe video assets and research | Project-specific rights and approval records |

Retain upstream attribution when distributing fork wheels. Do not imply these
forks or this wiki are official upstream releases. Model weights are not included
in the Python package release assets described here.

Local inference keeps narration on the machine after model downloads, but
downloading models exposes requests to the model host. Edge TTS is a separate,
explicitly selected external service; disclose that narration is transmitted.
This static wiki uses local search and does not require an analytics service.

Public GitHub releases and Pages are public distribution surfaces. Check for
secrets, private narration, unlicensed images, and machine-specific paths before
publishing. Do not copy a2swe project media into this documentation site.
