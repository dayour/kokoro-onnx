---
title: Releases, downloads, and checksums
---

Use the fork release pages, not similarly named upstream PyPI/npm packages:

| Fork | Release page | Typical Python artifact |
| --- | --- | --- |
| Kokoro ONNX | [Downloads](https://github.com/dayour/kokoro-onnx/releases) | `kokoro_onnx-0.6.1-py3-none-any.whl` |
| Kokoro | [Downloads](https://github.com/dayour/kokoro/releases) | `kokoro-0.9.4-py3-none-any.whl` |
| Misaki | [Downloads](https://github.com/dayour/misaki/releases) | `misaki-0.9.4+py314.1-py3-none-any.whl` |

Release tags distinguish fork builds even when the Python package version is
unchanged. Record both the source commit and asset checksum. A prerelease label
means production acceptance remains incomplete; do not infer stability from the
wheel filename.

## Verify and install

Download the wheel, source distribution if needed, and `SHA256SUMS.txt`.
Compare each downloaded artifact against the checksum manifest:

```powershell
Get-FileHash .\kokoro_onnx-0.6.1-py3-none-any.whl -Algorithm SHA256
```

Install the paired Python artifacts together in a Python 3.14 environment:

```powershell
python -m pip install ".\misaki-0.9.4+py314.1-py3-none-any.whl" ".\kokoro-0.9.4-py3-none-any.whl" ".\kokoro_onnx-0.6.1-py3-none-any.whl"
```

A `py3-none-any` wrapper wheel does not make its native dependencies universal.
Consult the [platform matrix](compatibility.md). Model weights, voice banks,
spaCy models, and dictionaries remain separate downloads.

## Clean-build policy

Build from the tagged source in an isolated directory, not a stale `dist` folder.
Publish only explicitly selected artifacts and checksums. Do not overwrite an
existing release asset without an intentional correction process. Release notes
must disclose known STFT and model/provider limitations.
