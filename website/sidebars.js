export default {
  wiki: [
    "intro",
    "getting-started",
    "architecture",
    "compatibility",
    {
      type: "category", label: "Kokoro ONNX", items: [
        "onnx/overview", "onnx/installation", "onnx/api", "onnx/streaming",
        "onnx/timing", "onnx/cuda", "onnx/export", "onnx/gradio",
      ],
    },
    {
      type: "category", label: "Kokoro", items: [
        "kokoro/overview", "kokoro/python", "kokoro/javascript", "kokoro/web-demo",
      ],
    },
    {
      type: "category", label: "Misaki", items: [
        "misaki/overview", "misaki/english", "misaki/languages",
      ],
    },
    {
      type: "category", label: "Integration and operations", items: [
        "integration/a2swe", "operations/audio", "operations/troubleshooting",
        "operations/development", "operations/deployment", "operations/licenses",
      ],
    },
    "releases",
  ],
};
