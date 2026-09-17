---
title: Gradio 6 demo
---

```powershell
uv run examples\app.py
```

Read the model and voice requirements in
[the example](https://github.com/dayour/kokoro-onnx/blob/main/examples/app.py)
before launching. The script installs its declared Gradio 6.27+ dependencies.

The demo provides text input, generated phonemes, audio playback/download, voice
selection, and optional equal-weight blending. Select **None** to disable blending.
Blank input produces a user-facing error rather than an empty audio result.

## Embedding the UI

`create_app(kokoro)` accepts an existing model object. Importing the module does
not load model weights or launch a server. Gradio 6 theme configuration belongs
in `launch()`, not `Blocks()`.

The `/create` API name is preserved. Obtain the current schema from the running
Gradio API documentation instead of assuming component order in a remote client.

Bind locally during development. Authentication, TLS, rate limiting, request
limits, and access to model files are deployment responsibilities. GitHub Pages
cannot host the Python Gradio process; it hosts only this static documentation.
