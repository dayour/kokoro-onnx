import tomllib
import unittest
from pathlib import Path

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

ROOT = Path(__file__).resolve().parents[1]


class ConfigurationTests(unittest.TestCase):
    def test_package_requires_python_314(self):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        supported = SpecifierSet(project["project"]["requires-python"])
        self.assertIn("3.14.0", supported)
        self.assertIn("3.14.7", supported)
        self.assertNotIn("3.13.9", supported)
        self.assertNotIn("3.15.0", supported)
        self.assertEqual((ROOT / ".python-version").read_text().strip(), "3.14")

    def test_gpu_extra_selects_windows_and_linux_x64_only(self):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        dependencies = project["project"]["optional-dependencies"]["gpu"]
        for platform, machine, expected in [
            ("win32", "AMD64", True),
            ("linux", "x86_64", True),
            ("darwin", "x86_64", False),
            ("linux", "aarch64", False),
            ("win32", "ARM64", False),
        ]:
            with self.subTest(platform=platform, machine=machine):
                environment = default_environment()
                environment.update(sys_platform=platform, platform_machine=machine)
                selected = [
                    dependency
                    for dependency in dependencies
                    if Requirement(dependency).marker.evaluate(environment)
                ]
                self.assertEqual(bool(selected), expected)

    def test_inline_scripts_require_python_314(self):
        scripts = [
            *(ROOT / "scripts").glob("*.py"),
            *(ROOT / "examples").glob("*.py"),
        ]
        for script in scripts:
            content = script.read_text(encoding="utf-8")
            if not content.startswith("# /// script\n"):
                continue
            with self.subTest(script=script.name):
                block = content.split("# ///", 2)[1].splitlines()[1:]
                metadata = tomllib.loads("\n".join(line[2:] for line in block))
                supported = SpecifierSet(metadata["requires-python"])
                self.assertIn("3.14.0", supported)
                self.assertNotIn("3.13.9", supported)
