import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

HAS_TOOLS = all(
    importlib.util.find_spec(name) is not None for name in ("torch", "requests", "tqdm")
)


@unittest.skipUnless(HAS_TOOLS, "Install voice-fetch script dependencies")
class VoiceFetchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "scripts" / "fetch_voices.py"
        spec = importlib.util.spec_from_file_location("fetch_voices", path)
        cls.fetch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.fetch)

    def test_pytorch_voice_converts_to_numpy_archive(self):
        expected = np.ones((3, 1, 256), dtype=np.float32)
        buffer = io.BytesIO()
        self.fetch.torch.save(self.fetch.torch.from_numpy(expected), buffer)
        response = Mock(content=buffer.getvalue())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "voices.bin"
            with patch.object(self.fetch.requests, "get", return_value=response):
                self.fetch.download_voices(
                    "https://example.invalid/{name}", ["test"], path
                )
            response.raise_for_status.assert_called_once()
            with np.load(path) as voices:
                np.testing.assert_array_equal(voices["test"], expected)

    def test_config_is_written_as_binary(self):
        content = b'{"vocab": {"a": 1}}'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            destination = root / "src" / "kokoro_onnx"
            destination.mkdir(parents=True)
            with (
                patch.object(
                    self.fetch, "__file__", str(root / "scripts" / "fetch_voices.py")
                ),
                patch.object(
                    self.fetch.requests, "get", return_value=Mock(content=content)
                ),
            ):
                self.fetch.download_config()
            self.assertEqual((destination / "config.json").read_bytes(), content)
