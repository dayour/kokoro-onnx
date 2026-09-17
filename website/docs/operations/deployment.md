---
title: Documentation and Pages deployment
---

This wiki lives in `website` in the ONNX fork. It uses Docusaurus 3.10.2,
stable React 19.3, local search, and the ClippyFlow light/dark design tokens.

```powershell
cd website
npm ci
npm run build
npm run serve -- --host 127.0.0.1 --port 3000
```

Open `/kokoro-onnx/` on the local server. Production builds fail on broken
internal links. Search indexes are generated during the production build;
development-server search behavior is not the production acceptance check.

## GitHub Pages

The `Documentation Pages` workflow builds on documentation changes and manual
dispatch. Pull requests build without deployment permissions. Main-branch
deployments publish the static artifact through the protected `github-pages`
environment using OIDC and `pages: write`.

Repository Settings / Pages must select **GitHub Actions** as the build source.
The site address is `https://dayour.github.io/kokoro-onnx/`.

After deployment, verify the home page, a deep route, local search, sidebar/mobile
navigation, keyboard focus, and both color modes. Check the workflow result and
the public URL; neither a local build nor a commit alone proves deployment.

Pages cannot run Gradio, Python inference, or a Node server. Deploy those
services separately if needed.
