"""Build checksummed release artifacts from a committed Git snapshot."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile
import tomllib


def run(*command, cwd):
    subprocess.run(command, cwd=cwd, check=True)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--javascript", action="store_true")
    parser.add_argument("--index-url", help="Optional build-dependency mirror")
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to reuse an existing release directory: {output}")
    output.mkdir(parents=True)
    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    uv = shutil.which("uv")
    if not uv:
        raise FileNotFoundError("uv is required")
    with tempfile.TemporaryDirectory(prefix="kokoro-release-") as temporary:
        scratch = Path(temporary)
        archive = scratch / "source.tar"
        source = scratch / "source"
        source.mkdir()
        run("git", "-C", str(repo), "archive", "--format=tar", "-o", str(archive), commit, cwd=repo)
        with tarfile.open(archive) as stream:
            stream.extractall(source, filter="data")
        manifest = tomllib.loads((source / "pyproject.toml").read_text(encoding="utf-8"))
        command = [uv, "build", "--project", str(source), "--out-dir", str(output)]
        if args.index_url:
            command.extend(["--default-index", args.index_url])
        run(*command, cwd=source)
        if args.javascript:
            npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
            if not npm:
                raise FileNotFoundError("npm is required for JavaScript release artifacts")
            library = source / "kokoro.js"
            run(npm, "ci", "--no-audit", "--no-fund", cwd=library)
            run(npm, "run", "build", cwd=library)
            run(npm, "test", cwd=library)
            run(npm, "pack", "--pack-destination", str(output), cwd=library)
            demo = library / "demo"
            run(npm, "ci", "--no-audit", "--no-fund", cwd=demo)
            run(npm, "run", "lint", cwd=demo)
            run(npm, "run", "build", cwd=demo)
            shutil.make_archive(str(output / "kokoro-web-production"), "zip", demo / "dist")
        provenance = {
            "repository": manifest["project"]["urls"]["Repository"],
            "commit": commit,
            "package": manifest["project"]["name"],
            "version": manifest["project"]["version"],
            "python": platform.python_version(),
            "build_platform": platform.platform(),
            "source": "git archive of committed HEAD; uncommitted files excluded",
            "artifacts": {
                path.name: digest(path) for path in sorted(output.iterdir())
                if path.is_file() and not path.name.startswith(".")
            },
        }
        (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
        checksums = [
            f"{digest(path)}  {path.name}" for path in sorted(output.iterdir())
            if path.is_file() and not path.name.startswith(".")
        ]
        (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
        print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
