---
title: Install ONNX and generate audio
---

From the fork checkout:

```powershell
uv sync --locked
curl.exe --fail --location --output kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
curl.exe --fail --location --output voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
```

These model downloads come from the upstream model release, not this fork's Python
package release. Keep a record of their SHA-256 hashes for reproducible deployment.

Save this as `hello.py`:

```python
import soundfile as sf
from kokoro_onnx import Kokoro

tts = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
try:
    audio, sample_rate = tts.create(
        "Hello from the Python 3.14 speech stack.",
        voice="af_heart", speed=1.0, lang="en-us",
    )
    sf.write("hello.wav", audio, sample_rate, subtype="PCM_16")
finally:
    tts.voices.close()
```

Run `uv run hello.py` from the checkout. SoundFile is in its development group.
Applications installing only the wheel should install SoundFile explicitly if
they use the example's WAV writer.

For wheel installation and checksum verification, see [releases](../releases.md).
For GPU setup, do not replace this procedure with an unverified CUDA toolkit
installer; use the [GPU extra](cuda.md).
