---
title: NVIDIA CUDA runtime
---

The `gpu` extra is for Windows and Linux x64. It selects ONNX Runtime GPU with
CUDA 13.x and cuDNN 9.x runtime dependencies. It does not update the system driver.

```powershell
uv sync --locked --extra gpu
$env:ONNX_PROVIDER = "CUDAExecutionProvider"
uv run --no-sync python examples\with_cuda.py
```

Use a driver compatible with the locked CUDA runtime. The CUDA number printed by
`nvidia-smi` describes driver capability, not proof that every required library is
installed or discoverable.

## Provider selection

The runtime preloads CUDA libraries. TensorRT is not selected automatically.
An explicit unavailable provider or a CUDA session that falls back to CPU is an
error. Set `ONNX_PROVIDER=CPUExecutionProvider` only when CPU is intentional.

The CPU and GPU ONNX distributions install overlapping `onnxruntime` module
files. If a CPU reinstall overwrites the GPU module, reinstall
`onnxruntime-gpu` last in that environment. Do not delete DLLs from system folders
or disable provider validation to make a diagnostic look green.

## Evidence to retain

Record driver version, runtime package versions, model hash, requested provider,
active session providers, sample count, finite-output check, and inference time.
Test the production precision format; CPU FP32 success does not certify GPU INT8.

Source: [session creation](https://github.com/dayour/kokoro-onnx/blob/main/src/kokoro_onnx/session.py).
