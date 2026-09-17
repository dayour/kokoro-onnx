---
title: React browser demo
---

Build the sibling library first, then run:

```powershell
cd kokoro.js\demo
npm ci
npm run typecheck
npm run lint
npm run build
npm run dev
```

The project pins TypeScript 7.0.2, stable React/React DOM `19.3.0`,
and stable Vite `8.3.0`. The earlier canary/beta pins and the demo's
prerelease peer overrides have been removed. Do not disable peer validation
globally when upgrading.

## Worker lifecycle

The UI and worker use a typed message contract. Model loading and inference run
outside the UI thread. A successful result transfers an audio Blob to the UI,
which owns the object URL. Workers, listeners, and audio URLs must be cleaned up
when the component unmounts, including React Strict Mode's development remount.

Synthesis failures should restore retry capability and expose the error.
Model-loading or worker failures must not leave an enabled Generate button
pointing at an unusable worker. Do not silently change to a remote speech API.

## Static hosting

The production bundle is static, but model and voice downloads still need network
access on first use. Browser GPU availability, storage limits, content-security
policy, and download CORS behavior affect deployment. This wiki is a separate
static site and does not automatically deploy the speech demo.

Source: [web demo](https://github.com/dayour/kokoro/tree/main/kokoro.js/demo).
