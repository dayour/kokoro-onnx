import unittest
from unittest.mock import Mock

import numpy as np

from kokoro_onnx import Kokoro
from kokoro_onnx.pauses import insert
from kokoro_onnx.sliding import Timing, token_edges


class AudioValidationTests(unittest.TestCase):
    def engine(self, outputs, *, timings=False):
        kokoro = Kokoro.__new__(Kokoro)
        kokoro.sess = Mock()
        kokoro.sess.run.return_value = outputs
        kokoro.sess.get_providers.return_value = ["CPUExecutionProvider"]
        kokoro.has_timings = timings
        kokoro._tokens_input = "tokens"
        kokoro._input_dtypes = {
            "tokens": np.dtype(np.int64),
            "style": np.dtype(np.float32),
            "speed": np.dtype(np.float32),
        }
        return kokoro

    def test_invalid_audio_is_rejected_before_trimming(self):
        for audio in (
            np.array([], dtype=np.float32),
            np.array([np.nan], dtype=np.float32),
            np.array([np.inf], dtype=np.float32),
            np.array([-np.inf], dtype=np.float32),
        ):
            with self.subTest(audio=audio):
                kokoro = self.engine([audio])
                with self.assertRaisesRegex(RuntimeError, "empty or non-finite audio"):
                    kokoro._infer([1], np.zeros((1, 256), dtype=np.float32), 1.0)

    def test_missing_outputs_have_an_actionable_error(self):
        for outputs, timings in (([], False), ([np.ones(10)], True)):
            with self.subTest(timings=timings):
                with self.assertRaisesRegex(RuntimeError, "expected audio outputs"):
                    self.engine(outputs, timings=timings)._infer(
                        [1], np.zeros((1, 256), dtype=np.float32), 1.0
                    )

    def test_half_precision_audio_has_a_float32_public_interface(self):
        original = np.array([0.25, -0.5, 0.75], dtype=np.float16)
        audio, duration = self.engine([original])._infer(
            [1], np.zeros((1, 256), dtype=np.float32), 1.0
        )
        self.assertEqual(audio.dtype, np.float32)
        np.testing.assert_array_equal(audio, original)
        self.assertIsNone(duration)

    def test_pause_insertion_preserves_audio_shorter_than_one_frame(self):
        for length in (0, 1, 239):
            with self.subTest(length=length):
                audio = np.ones(length, dtype=np.float32)
                spoken = [Timing(".", 0.0, length / 24000)]
                result, moved = insert(audio, spoken, 24000, 0.25, 0.1)
                np.testing.assert_array_equal(result, audio)
                self.assertEqual(moved, spoken)

    def test_invalid_durations_are_rejected(self):
        for values in ([], [0, 0], [-1, 2], [np.nan], [np.inf], [[1, 2]]):
            with self.subTest(values=values):
                with self.assertRaisesRegex(ValueError, "Token durations"):
                    token_edges(np.asarray(values), 2400)
        with self.assertRaisesRegex(ValueError, "sample count"):
            token_edges(np.array([1, 2]), -1)

    def test_zero_length_tokens_are_allowed_when_total_duration_is_positive(self):
        np.testing.assert_array_equal(
            token_edges(np.array([0, 1, 0, 2]), 300), [0, 0, 100, 100, 300]
        )
