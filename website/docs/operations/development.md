---
title: Development and upgrade workflow
---

## Existing validation commands

ONNX:

```powershell
uv sync --locked
uv run --locked python -m unittest discover -s tests -v
uv build
```

Kokoro:

```powershell
uv run --no-sync python -m pytest tests\test_python_compatibility.py tests\test_optional_dependencies.py
uv run --no-sync python -m pytest tests\test_python_compatibility.py -m integration
```

Misaki:

```powershell
uv sync --locked --all-extras
uv run --no-sync python -m pytest
```

JavaScript library: `npm ci`, `npm run build`, `npm test`.
Browser demo: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run build`.

## Upgrade discipline

Inspect current manifests and lockfiles before selecting versions. Preserve
Python 3.14 constraints and platform markers. Do not force stable-only peers to
accept prereleases without documenting and validating the deviation.

Use the package manager to regenerate locks. Temporary registry metadata or
mirror settings must not silently replace the intended public package source.
Keep shared language, CUDA, and dictionary dependencies intact.

Commit reviewable groups of changes. Do not stage unrelated work in a dirty
checkout. Record validation gaps plainly; a successful package build is not a
substitute for inference or browser checks.
