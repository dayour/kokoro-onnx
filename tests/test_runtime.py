import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np

from kokoro_onnx import SAMPLE_RATE, Kokoro
from kokoro_onnx.chunker import split_phonemes
from kokoro_onnx.config import DEFAULT_VOCAB
from kokoro_onnx.session import create_session, input_dtypes, resolve_providers
from kokoro_onnx.sliding import timings, token_edges
from kokoro_onnx.tokenizer import Tokenizer
from kokoro_onnx.trim import trim


class RuntimeTests(unittest.TestCase):
    def test_native_phonemizer_and_bundled_vocabulary(self):
        tokenizer = Tokenizer()
        phonemes = tokenizer.phonemize("Hello, world!")
        self.assertTrue(phonemes)
        self.assertTrue(tokenizer.tokenize(phonemes))
        self.assertTrue(all(p in DEFAULT_VOCAB for p in phonemes))

    def test_long_text_preserves_phonemes(self):
        text = "Hello world. " * 200
        chunks = split_phonemes(text)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(0 < len(chunk) <= 510 for chunk in chunks))
        self.assertEqual(" ".join(chunks), text.strip())

    def test_numpy_audio_trimming(self):
        audio = np.concatenate([np.zeros(4096), np.ones(8192), np.zeros(4096)]).astype(
            np.float32
        )
        trimmed, (start, end) = trim(audio)
        self.assertGreater(start, 0)
        self.assertLess(end, len(audio))
        self.assertEqual(trimmed.dtype, np.float32)
        np.testing.assert_array_equal(trimmed, audio[start:end])

    def test_duration_timing(self):
        edges = token_edges(np.array([1, 2, 3], dtype=np.int64), 3600)
        np.testing.assert_array_equal(edges, [0, 600, 1800, 3600])
        spoken = timings("ab", edges[1:], SAMPLE_RATE)
        self.assertEqual([item.phoneme for item in spoken], ["a", "b"])
        self.assertEqual(spoken[-1].end, 3600 / SAMPLE_RATE)

    def test_native_input_types(self):
        session = Mock()
        session.get_inputs.return_value = [
            SimpleNamespace(name="input_ids", type="tensor(int64)"),
            SimpleNamespace(name="style", type="tensor(float)"),
            SimpleNamespace(name="speed", type="tensor(int32)"),
        ]
        self.assertEqual(
            input_dtypes(session),
            {
                "input_ids": np.dtype(np.int64),
                "style": np.dtype(np.float32),
                "speed": np.dtype(np.int32),
            },
        )

    def test_accelerated_distribution_selects_available_providers(self):
        available = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "kokoro_onnx.session.rt.get_available_providers", return_value=available
            ),
            patch(
                "kokoro_onnx.session._installed",
                side_effect=lambda name: name == "onnxruntime-gpu",
            ),
        ):
            self.assertEqual(resolve_providers(), available)

    def test_cuda_does_not_assume_tensorrt_is_installed(self):
        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "kokoro_onnx.session.rt.get_available_providers",
                return_value=[
                    "TensorrtExecutionProvider",
                    "CUDAExecutionProvider",
                    "CPUExecutionProvider",
                ],
            ),
            patch(
                "kokoro_onnx.session._installed",
                side_effect=lambda name: name == "onnxruntime-gpu",
            ),
        ):
            self.assertEqual(
                resolve_providers(), ["CUDAExecutionProvider", "CPUExecutionProvider"]
            )

    def test_cpu_wheel_overwriting_gpu_is_reported(self):
        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "kokoro_onnx.session.rt.get_available_providers",
                return_value=["CPUExecutionProvider"],
            ),
            patch(
                "kokoro_onnx.session._installed",
                side_effect=lambda name: name == "onnxruntime-gpu",
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "share files"):
                resolve_providers()

    def test_unavailable_explicit_provider_is_rejected(self):
        with (
            patch.dict("os.environ", {"ONNX_PROVIDER": "CUDAExecutionProvider"}),
            patch(
                "kokoro_onnx.session.rt.get_available_providers",
                return_value=["CPUExecutionProvider"],
            ),
        ):
            with self.assertRaisesRegex(ValueError, "not available"):
                resolve_providers()

    def test_cuda_libraries_are_loaded_before_session_creation(self):
        calls = []
        session = Mock()
        session.get_providers.return_value = ["CUDAExecutionProvider"]
        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "kokoro_onnx.session.resolve_providers",
                return_value=["CUDAExecutionProvider", "CPUExecutionProvider"],
            ),
            patch(
                "kokoro_onnx.session.rt.preload_dlls",
                side_effect=lambda: calls.append("preload"),
            ),
            patch(
                "kokoro_onnx.session.rt.InferenceSession",
                side_effect=lambda *args, **kwargs: calls.append("session") or session,
            ),
        ):
            self.assertIs(create_session("model.onnx"), session)
        self.assertEqual(calls, ["preload", "session"])

    def test_cuda_failure_does_not_masquerade_as_gpu_success(self):
        session = Mock()
        session.get_providers.return_value = ["CPUExecutionProvider"]
        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "kokoro_onnx.session.resolve_providers",
                return_value=["CUDAExecutionProvider", "CPUExecutionProvider"],
            ),
            patch("kokoro_onnx.session.rt.preload_dlls"),
            patch("kokoro_onnx.session.rt.InferenceSession", return_value=session),
        ):
            with self.assertRaisesRegex(RuntimeError, "implicit CPU fallback"):
                create_session("model.onnx")

    def test_explicit_cpu_does_not_load_cuda_libraries(self):
        session = Mock()
        session.get_providers.return_value = ["CPUExecutionProvider"]
        with (
            patch.dict("os.environ", {"ONNX_PROVIDER": "CPUExecutionProvider"}),
            patch(
                "kokoro_onnx.session.resolve_providers",
                return_value=["CPUExecutionProvider"],
            ),
            patch("kokoro_onnx.session.rt.preload_dlls") as preload,
            patch("kokoro_onnx.session.rt.InferenceSession", return_value=session),
        ):
            self.assertIs(create_session("model.onnx"), session)
            preload.assert_not_called()


class StreamTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.kokoro = Kokoro.__new__(Kokoro)
        self.kokoro._prepare = Mock(
            return_value=(
                np.zeros((1, 256), dtype=np.float32),
                "ab",
                [("a", 0), ("b", 0)],
            )
        )
        self.audio = np.ones(2400, dtype=np.float32)
        self.kokoro._create_batch = Mock(return_value=(self.audio, None))

    async def test_stream_runs_without_implicit_event_loop(self):
        chunks = [chunk async for chunk in self.kokoro.create_stream("hello", "test")]
        self.assertEqual(len(chunks), 2)
        for audio, rate in chunks:
            np.testing.assert_array_equal(audio, self.audio)
            self.assertEqual(rate, SAMPLE_RATE)

    async def test_worker_error_reaches_consumer(self):
        self.kokoro._create_batch.side_effect = RuntimeError("inference failed")
        stream = self.kokoro.create_stream("hello", "test")
        try:
            with self.assertRaisesRegex(RuntimeError, "inference failed"):
                await asyncio.wait_for(anext(stream), timeout=5)
        finally:
            await stream.aclose()

    async def test_closing_stream_cleans_up_producer(self):
        before = asyncio.all_tasks()
        stream = self.kokoro.create_stream("hello", "test")
        await anext(stream)
        await stream.aclose()
        self.assertEqual(asyncio.all_tasks(), before)
