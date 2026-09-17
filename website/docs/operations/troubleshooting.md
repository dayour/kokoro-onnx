---
title: Troubleshooting
---

| Symptom | Likely cause | Next action |
| --- | --- | --- |
| Python requirement rejection | Wrong interpreter | Use standard CPython 3.14 |
| Missing Misaki local version | Upstream package substituted | Install the paired fork wheel or sibling checkout |
| eSpeak API/import inconsistency | Overlapping phonemizer distributions | Sync current locks and reinstall upstream phonemizer |
| CUDA requested but unavailable | Wrong ORT distribution, driver, or DLLs | Inspect providers and follow the GPU guide |
| CPU used unexpectedly | Provider fallback or overwritten GPU module | Keep explicit-provider validation enabled |
| Empty / NaN audio | Model/runtime/precision incompatibility | Capture diagnostics; do not normalize into a silent WAV |
| Missing timestamps | Graph has no duration output | Use a duration-capable export |
| Speed 0.9 rounded | Legacy integer speed input | Re-export using float speed |
| `trf=True` rejected | Unsupported spaCy transformer stack | Use documented `trf=False` path |
| Browser stuck loading | Model download, GPU, CORS, or worker error | Inspect visible error and browser console |
| Package download TLS error | Network or certificate path | Use an approved mirror; never disable TLS validation |
| Static site 404 after deploy | Pages/base URL mismatch | Confirm Actions-based Pages and `/kokoro-onnx/` base URL |

## A useful bug report

Include the fork commit, Python/Node versions, dependency lock, OS/architecture,
model and voice hashes, device/provider, precision, short non-sensitive input,
full error, and whether a fresh uncached run reproduces it.

Do not attach credentials, proprietary narration, or entire environment dumps.
For the known macOS INT8 regression and CustomSTFT failures, see
[compatibility](../compatibility.md).
