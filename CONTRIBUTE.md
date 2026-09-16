# Contributing to kokoro-onnx

Thanks for thinking about contributing! 🎉

## What We Focus On

This repo is for the kokoro-onnx package and examples. Our focus is on improving the package, adding examples, fixing bugs, and keeping things minimal and simple. We aim to prevent unnecessary complexity and ensure the project stays straightforward.

Before contributing, **please open a [new issue](https://github.com/thewh1teagle/kokoro-onnx/issues)** to discuss your idea. This helps make sure it's a good fit and relevant. We're here to help!

## Development Recommendations

We strongly recommend using [uv](https://docs.astral.sh/uv/getting-started/installation) for development, along with the Visual Studio Code extension suggested in the repository's recommendations.

The default interpreter is Python 3.14. Install the locked environment and run
the model-free tests with:

```console
uv sync --locked
uv run --locked python -m unittest discover -s tests -v
```

Python 3.14 is the minimum and default interpreter. CI covers Python 3.14
on Linux x64/ARM64, Windows x64, and Apple Silicon macOS.

The integration tests run when `KOKORO_TEST_MODEL` and `KOKORO_TEST_VOICES`
point to a downloaded ONNX model and voices file. Without both files they are
skipped; no network downloads or audio device are required for unit tests.
Voice-fetch tests additionally require the script's NumPy, requests, PyTorch,
and tqdm dependencies.

Before submitting a pull request, please ensure your code meets the project's formatting and linting standards by running:

```console
uv run ruff format
uv run ruff check
```

If you want to use ruff for quick [safety fixes](https://docs.astral.sh/ruff/linter/#fix-safety),
you can run the following command:

```console
uv run ruff check --fix
```

## Pull Request Guidelines

Do not create a pull request from your main branch. This ensures we can collaborate and edit the PR if needed.
Thank you for contributing and helping improve kokoro-onnx! 🚀
