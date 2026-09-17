---
title: Python pipeline and CLI
---

Clone Misaki beside Kokoro, then:

```powershell
cd kokoro
uv sync --locked --python 3.14
uv run --no-sync kokoro --text "Hello world." --output-file hello.wav
```

For direct use, install SoundFile when you need WAV output:

```python
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code="a", device="cpu", repo_id="hexgrad/Kokoro-82M")
for index, result in enumerate(pipeline("Hello world.", voice="af_heart")):
    if result.audio is None:
        raise RuntimeError("The pipeline did not produce audio")
    sf.write(f"part-{index}.wav", result.audio.detach().cpu().numpy(), 24000)
```

The first run may download model weights, a voice, and a spaCy language model.
Pin the model source and preserve caches according to your deployment policy.

## Common controls

`lang_code="a"` selects American English and `"b"` British English. The pipeline
also supports language-specific modes; install the required Misaki extra rather
than assuming every language dependency is in the default environment.
`model=False` creates a phonemization-only pipeline without neural audio output.

For the demo/export tools:

```powershell
uv sync --locked --group demo --group export
uv run --no-sync python demo\app.py
```

For paired wheel installs, supply both fork wheels in the same pip command.
The pinned local-version Misaki requirement cannot be satisfied by substituting
an unrelated upstream release.

Source: [pipeline.py](https://github.com/dayour/kokoro/blob/main/kokoro/pipeline.py)
and [CLI](https://github.com/dayour/kokoro/blob/main/kokoro/__main__.py).
