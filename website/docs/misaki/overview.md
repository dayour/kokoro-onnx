---
title: Misaki pronunciation engine
---

[Misaki](https://github.com/dayour/misaki) converts graphemes to phonemes for
speech synthesis. It does not generate audio on its own. This fork identifies as
`0.9.4+py314.1` and requires Python 3.14.

```powershell
uv sync --locked --extra en
```

Supported extras are `en`, `ja`, `ko`, `zh`, and `vi`. Use `--all-extras` only
when you actually need the full language environment and its download/storage
requirements.

The English stack shares upstream phonemizer 3.4 with Kokoro ONNX. Do not
reintroduce `phonemizer-fork` into a combined environment: both distributions
write the same Python module directory.

Language modules have different return contracts. The English engine returns
phonemes and token metadata; check the module source when integrating another
language rather than applying the English token assumptions to every backend.
