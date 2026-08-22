# MyFreeGenerator — QR Code Generator

## Project structure

```
myfreegenerator/
├── src/
│   ├── css/input.css        # Tailwind entry point (compiled to dist/assets/styles.css)
│   └── js/qr-generator.js   # QR generator app logic (copied to dist/assets/)
├── pages/                   # Page templates / source HTML
│   ├── index.html                       → /
│   ├── qr-code-for-url.html             → /qr-code-for-url.html
│   ├── qr-code-for-text.html            → /qr-code-for-text.html
│   ├── faq.html                         → /faq.html
│   ├── guide/qr-code-best-practices.html→ /guide/qr-code-best-practices.html
│   ├── sitemap.xml
│   └── robots.txt
├── dist/                    # Production build output (generated, deploy this folder)
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

Note: pages currently duplicate the nav/footer markup by hand, since there's no
templating engine wired in yet. If the team adopts a static site generator
(Astro, 11ty, Next.js static export, etc.), the nav/footer should become a
shared partial/component — that's the natural next refactor once page count grows
beyond what's comfortable to hand-maintain.

## Setup

```bash
npm install
```

## Build for production

```bash
npm run build
```

This:
1. Cleans `dist/`
2. Compiles Tailwind from `src/css/input.css` into a minified, tree-shaken
   `dist/assets/styles.css` (only the utility classes actually used in
   `pages/**/*.html` are included — no CDN runtime, no unused CSS)
3. Copies the QR generator JS to `dist/assets/qr-generator.js`
4. Copies all HTML pages, `sitemap.xml`, and `robots.txt` into `dist/`

## Preview the production build locally

```bash
npm run serve
```

## Deploying

Deploy the contents of `dist/` as-is to any static host (Netlify, Vercel,
Cloudflare Pages, S3+CloudFront, etc.). Update the canonical/OG URLs in each
page's `<head>` and in `sitemap.xml` / `robots.txt` if the production domain
differs from `https://www.myfreegenerator.com`.

## Remaining third-party dependency

The QRCode.js library is still loaded from a CDN
(`cdnjs.cloudflare.com/.../qrcode.min.js`) with `defer`, so it never blocks
initial render. For full control over caching and to remove the external
request entirely, vendor it into `src/js/vendor/qrcode.min.js` and update the
`<script>` tag in each page to point at `/assets/qrcode.min.js` instead.

## After deployment

1. Verify each page in `dist/` returns `200 OK` and matches its canonical URL.
2. Submit `sitemap.xml` in Google Search Console (Sitemaps → Add a new sitemap).
3. Use the URL Inspection tool to request indexing for each new page.
4. Monitor Coverage/Indexing, Impressions, Clicks, CTR, and average position in
   Search Console weekly for the first month, then monthly.
5. Run Lighthouse / PageSpeed Insights on `dist/index.html` post-deploy to
   confirm Core Web Vitals after removing the Tailwind CDN script.
