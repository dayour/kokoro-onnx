const config = {
  title: "Kokoro speech stack",
  tagline: "The Python 3.14 forks: runtime, synthesis, and pronunciation",
  url: "https://dayour.github.io",
  baseUrl: "/kokoro-onnx/",
  organizationName: "dayour",
  projectName: "kokoro-onnx",
  trailingSlash: true,
  onBrokenLinks: "throw",
  markdown: { hooks: { onBrokenMarkdownLinks: "throw" } },
  i18n: { defaultLocale: "en", locales: ["en"] },
  presets: [
    [
      "classic",
      {
        docs: {
          routeBasePath: "/",
          sidebarPath: "./sidebars.js",
          editUrl: "https://github.com/dayour/kokoro-onnx/edit/main/website/",
          showLastUpdateTime: true,
        },
        blog: false,
        theme: { customCss: "./src/css/custom.css" },
        sitemap: { changefreq: "weekly", priority: 0.5 },
      },
    ],
  ],
  themes: [
    [
      "@easyops-cn/docusaurus-search-local",
      { hashed: true, indexDocs: true, indexBlog: false, docsRouteBasePath: "/", language: ["en"], highlightSearchTermsOnTargetPage: true },
    ],
  ],
  themeConfig: {
    colorMode: { defaultMode: "light", respectPrefersColorScheme: true },
    navbar: {
      title: "Kokoro speech stack",
      items: [
        { type: "docSidebar", sidebarId: "wiki", label: "Wiki", position: "left" },
        { to: "/releases", label: "Downloads", position: "left" },
        { href: "https://github.com/dayour/kokoro-onnx", label: "GitHub", position: "right" },
      ],
    },
    footer: {
      links: [
        { title: "Runtime", items: [{ label: "Kokoro ONNX", to: "/onnx/overview" }, { label: "Kokoro Python / JS", to: "/kokoro/overview" }] },
        { title: "Pronunciation", items: [{ label: "Misaki", to: "/misaki/overview" }, { label: "Language guide", to: "/misaki/languages" }] },
        { title: "Operations", items: [{ label: "Troubleshooting", to: "/operations/troubleshooting" }, { label: "Licenses and privacy", to: "/operations/licenses" }] },
      ],
      copyright: "Community-maintained dayour forks. Upstream authors retain their copyrights. Not an official upstream documentation site.",
    },
    prism: { additionalLanguages: ["powershell", "python", "bash", "json", "typescript"] },
  },
};

export default config;
