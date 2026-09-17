---
title: Language extras and resources
---

| Extra | Principal dependencies | Operational note |
| --- | --- | --- |
| `en` | spaCy, phonemizer, NumPy, PyTorch, Transformers | Stable spaCy small-model path; no transformer G2P |
| `ja` | fugashi, jaconv, UniDic, pyopenjtalk-plus | Default cutlet path needs a separate UniDic dictionary |
| `ko` | jamo, NLTK, MeCab, packaged Korean dictionary | MeCab and dictionary are installed across platforms |
| `zh` | jieba, pypinyin, cn2an, pypinyin-dict | Install Chinese extra before importing the engine |
| `vi` | English extra, underthesea, vietnam-number | Includes the required number-conversion dependency |

```powershell
uv sync --locked --extra ja
uv run --no-sync python -m unidic download
```

The Japanese `pyopenjtalk` backend does not require that separate UniDic
download, although it can download its own Open JTalk resources. NLTK CMU data
can also be downloaded by language checks.

Japanese width normalization uses jaconv rather than the older mojimoji native
extension. This removes a Python 3.14 compatibility obstacle without making
every Japanese backend resource-free.

Hebrew is not supported by this fork's dependency set. The old extra was removed
because its upstream package was unavailable and the replacement excluded
Python 3.14.

Source of truth: [optional dependencies](https://github.com/dayour/misaki/blob/main/pyproject.toml)
and [language examples](https://github.com/dayour/kokoro-onnx/tree/main/examples).
