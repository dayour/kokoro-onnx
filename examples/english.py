# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = ["kokoro-onnx", "soundfile", "misaki[en]==0.9.4+py314.1"]
# [tool.uv.sources]
# kokoro-onnx = { path = "../" }
# misaki = { path = "../../misaki", editable = true }
# ///
"""
Usage:
1.
    Install uv from https://docs.astral.sh/uv/getting-started/installation
2.
    Use this repository beside the Python 3.14 kokoro and misaki checkouts.
3.
    Download these files
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
4. Run
    uv run examples/english.py

For other languages read https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
"""

import soundfile as sf
from misaki import en, espeak

from kokoro_onnx import Kokoro

# Misaki G2P with espeak-ng fallback
fallback = espeak.EspeakFallback(british=False)
g2p = en.G2P(trf=False, british=False, fallback=fallback)

# Kokoro
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

# Phonemize
text = "[Misaki](/misˈɑki/) is a G2P engine designed for [Kokoro](/kˈOkəɹO/) models."
phonemes, _ = g2p(text)

# Create
samples, sample_rate = kokoro.create(phonemes, "af_heart", is_phonemes=True)

# Save
sf.write("audio.wav", samples, sample_rate)
print("Created audio.wav")
