import asyncio
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import soundfile as sf

from kokoro_onnx import SAMPLE_RATE, Kokoro


@unittest.skipUnless(
    os.environ.get("KOKORO_TEST_MODEL") and os.environ.get("KOKORO_TEST_VOICES"),
    "Set KOKORO_TEST_MODEL and KOKORO_TEST_VOICES to run real inference",
)
class InferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kokoro = Kokoro(
            os.environ["KOKORO_TEST_MODEL"], os.environ["KOKORO_TEST_VOICES"]
        )

    @classmethod
    def tearDownClass(cls):
        cls.kokoro.voices.close()

    def assert_audio(self, audio, sample_rate):
        self.assertEqual(sample_rate, SAMPLE_RATE)
        self.assertEqual(audio.ndim, 1)
        self.assertEqual(audio.dtype, np.float32)
        self.assertGreater(audio.size, SAMPLE_RATE // 10)
        self.assertTrue(np.isfinite(audio).all())
        self.assertGreater(float(np.max(np.abs(audio))), 0.001)

    def test_synthesis_and_wav_round_trip(self):
        audio, rate = self.kokoro.create("Hello, world!", "af_sarah")
        self.assert_audio(audio, rate)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "speech.wav"
            sf.write(path, audio, rate)
            restored, restored_rate = sf.read(path, dtype="float32")
            self.assert_audio(restored, restored_rate)
            np.testing.assert_allclose(restored, audio, atol=1 / 32768)

    def test_real_streaming(self):
        async def collect():
            return [
                chunk
                async for chunk in self.kokoro.create_stream(
                    "Hello, world!", "af_sarah"
                )
            ]

        chunks = asyncio.run(collect())
        self.assertTrue(chunks)
        for audio, rate in chunks:
            self.assert_audio(audio, rate)
