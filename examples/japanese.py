# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = ["kokoro-onnx", "soundfile", "misaki[ja]==0.9.4+py314.1"]
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
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.1-zh.onnx
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.1-zh.bin
    https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh/raw/main/config.json
4. Run
    uv run examples/japanese.py
"""

import soundfile as sf
from misaki import ja

from kokoro_onnx import Kokoro

# Misaki G2P with espeak-ng fallback
g2p = ja.JAG2P()

text = "「人生を夢見るな。夢を生きろ。」"
voice = "jf_alpha"
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin", vocab_config="config.json")
phonemes, _ = g2p(text)
samples, sample_rate = kokoro.create(phonemes, voice=voice, speed=1.0, is_phonemes=True)
sf.write("audio.wav", samples, sample_rate)
print("Created audio.wav")
