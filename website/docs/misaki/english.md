---
title: English and eSpeak fallback
---

```python
from misaki import en, espeak

fallback = espeak.EspeakFallback(british=False)
g2p = en.G2P(trf=False, british=False, fallback=fallback)
phonemes, tokens = g2p("Hello from the pronunciation engine.")
print(phonemes)
```

Use `british=True` consistently for both the G2P engine and its eSpeak fallback
when targeting British English. Model/voice language choices should agree with
the pronunciation mode.

## spaCy and dictionary behavior

The fork uses stable spaCy 3.8. First use may require the English spaCy model.
The existing compatibility tests can exercise lexical behavior without a neural
model download; that is not a substitute for testing your application's actual
model and language resources.

`trf=True` is unavailable on this Python 3.14 stack and fails before downloading.
There is no silent fallback from a requested transformer pipeline to the small
model. Do not remove this guard without resolving spaCy/Thinc compatibility.

## Pronunciation overrides

Misaki supports explicit pronunciation notation, as documented in the repository:

```python
phonemes, tokens = g2p("[Misaki](/misaki/) is a pronunciation engine.")
```

Supply phonemes appropriate for the model vocabulary. For an ONNX integration,
pass the resulting phoneme string with `is_phonemes=True` so it is not phonemized
twice.

Source: [English engine](https://github.com/dayour/misaki/blob/main/misaki/en.py)
and [fallback](https://github.com/dayour/misaki/blob/main/misaki/espeak.py).
