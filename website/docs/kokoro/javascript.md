---
title: JavaScript and TypeScript 7
---

From `kokoro.js`, use the committed npm lock:

```powershell
npm ci
npm run build
npm test
```

The library uses Transformers.js 4, Rollup, and TypeScript 7.0.2. TypeScript
checks the JavaScript/JSDoc source and emits declarations into `types`.
Build output includes Node ESM/CommonJS and a browser bundle.

```javascript
import { KokoroTTS } from "kokoro-js";

const tts = await KokoroTTS.from_pretrained(
  "onnx-community/Kokoro-82M-v1.0-ONNX",
  { dtype: "q8", device: "wasm" },
);
const audio = await tts.generate("Hello from JavaScript.", { voice: "af_heart" });
```

`RawAudio` exposes helpers such as `save` in Node and `toBlob` for the browser.
Browser WebGPU generally uses `fp32`; the demo chooses quantized WebAssembly
when WebGPU is unavailable. Validate device/precision combinations in the actual
target browser.

## Streaming

`tts.stream` yields objects containing text, phonemes, and audio. Use
`TextSplitterStream` for incremental text; close the splitter after the last
input so consumers can finish. Do not conflate this stream with the Python
ONNX async generator, which yields audio/sample-rate tuples.

The npm package name is shared with upstream. To use this fork, build the local
checkout or install its release package artifact rather than assuming an npm
registry install contains the fork's changes.

Source: [library README](https://github.com/dayour/kokoro/blob/main/kokoro.js/README.md).
