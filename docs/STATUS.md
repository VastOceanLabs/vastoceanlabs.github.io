# Status

## Now

- **Milestone:** B — Brand and content. Done (S3 + S4); PR 2 open into `main`.
- **Last session:** S4 — Content and app page (done)
- **Next session:** S5 — Quality pass. See [PLAN.md](PLAN.md#s5--quality-pass).
- **Start S5 from:** `main` once PR 2 is merged. If it isn't merged yet, ask
  the user; don't stack S5 on `claude/busy-meitner-o4j18j` without asking.
- **Open PRs:** PR 2 — Milestone B (S3 + S4), from `claude/busy-meitner-o4j18j`.

## Handoff to S5

- S5 needs D-08 (link-check CI). Ask at the start.
- New in S4: `/re-direct/` (`re-direct/index.html`, `_layouts/app.html`),
  `_includes/store-button.html`, screenshots in `assets/img/apps/re-direct/`,
  About section and nav link on the home page, contact email
  `vastoceanlabs@gmail.com` (D-05). Store button shows "Coming soon" while
  `store.live: false` (D-13).
- How to verify: as in S4. `scripts/build.sh`, serve `_site/`
  (`python3 -m http.server`), screenshot `/`, `/re-direct/` and
  `/re-direct/privacy-policy.html` at 1280 and 390px in light and dark, check
  `scrollWidth == clientWidth`, and compare the protected URLs with a build
  of the starting branch (`cmp` for `assetlinks.json`, `/r/index.html`,
  `/r/og.png`; text inside `<main>` for the policy pages).

## Facts learned (keep)

- GitHub Pages applies its default plugins (optional front matter, default
  layout, titles from headings, relative links) and the Primer theme. A plain
  `jekyll build` does not, which is why `scripts/build.sh` runs through the
  `github-pages` gem. The policy `.md` files rely on those plugins.
- The policy pages now use our `page` layout. Their text was diffed against
  the Primer-rendered baseline in S2 and is identical.
- Pages also publishes the raw `re-direct/*.md` next to the `.html`. That was
  already the case; harmless.

## Noted for later sessions

- **When re-direct goes public on Google Play:** set `store.live: true` in
  `_data/apps.yml` (D-13). Small content-only PR, outside the milestone rhythm.
- **re-direct icon (still open from S3):** the redrawn icon is on branch
  `claude/keen-edison-jpo2qa` of `VastOceanLabs/re-direct`, still not merged
  into its `main` at S4. Once it lands, replace `assets/img/apps/re-direct.png`
  with `branding/store_listing/app_icon/out/app_icon_512.png` (the current file
  is byte-identical to that file on the app repo's `main`). `/r/og.png` could
  follow, but `/r/` is protected: content-only change, same path, re-check.
- **S5:** `twitter:card` tags and per-page share images (the `/re-direct/` page
  uses `og-default.png`; it can set `og_image`). Contrast: audit `--muted` on
  `--surface`, the dark-mode cards, and `.soon` text. Font preload on every
  page is fine at 39 KB.
- **S5:** no `404.html`, sitemap or `robots.txt` yet.
- **S5 (performance):** screenshots are 540×1200 WebP, 10–33 KB each, first
  two eager, rest lazy. Made from the app repo's
  `branding/store_listing/phone_screenshots/out/*.png` with Pillow (quality 82).
- **App repo (not this repo):**
  - Contact email (D-05): change `docs/PRIVACY_POLICY.md`,
    `docs/ACCESSIBILITY_DISCLOSURE.md` and `docs/PLAY_CONSOLE_SUBMISSION.md` to
    `vastoceanlabs@gmail.com`, re-run `scripts/sync_web_docs.js`, copy the
    generated `re-direct/*.md` here. Until then the policy pages show the old
    address. Also update the Play Console developer email.
  - Naming: the store listing and privacy policy say "Analytics screen"; the
    shipped app (screenshots) calls it "Insights". The site uses "Insights".
  - Policy header block renders as one run-on line (no hard breaks in the
    Markdown). Fix in the app repo, then re-sync. Pre-existing.
- The Apps intro "One app so far, built carefully." is hard-coded in
  `index.html`; change it when a second app arrives.

## Facts learned in S3 (keep)

- Rebuild the brand files with `NODE_PATH=$(npm root -g) scripts/brand/build.sh`
  (needs `pip install fonttools brotli uharfbuzz pillow` and Playwright). In
  the cloud sessions the globally installed Playwright works with the
  preinstalled Chromium.
- Chromium screenshots drop the alpha channel of fully opaque images, so
  `apple-touch-icon.png` and `og-default.png` are RGB. That's what those
  formats want.

## Session log

| Session | Date | Branch | Summary | PR |
|---|---|---|---|---|
| S1 | 2026-10-08 | `claude/gifted-galileo-lof422` | Home page first draft; build plan, decision log, status docs, CLAUDE.md; README fixed for this repo | PR 1 |
| S2 | 2026-10-08 | `claude/gifted-galileo-lof422` | Jekyll structure: layouts, includes, `site.css` tokens, `apps.yml`/`navigation.yml`; policy pages on the site layout; mobile tables; local build script. Home page pixel-identical to S1; protected URLs byte-identical | [PR 1](https://github.com/VastOceanLabs/vastoceanlabs.github.io/pull/1) |
| S3 | 2026-10-08 | `claude/keen-edison-jpo2qa` (from PR 1 branch) | Studio brand: user's sunset-over-sea mark, traced and recoloured, + Nunito wordmark (D-03; replaced the first drawn mark the same day), self-hosted Nunito headings (D-04), deeper ocean palette (D-12, fixes AA contrast), type and spacing tokens, favicons, apple-touch icon, 1200×630 share image as `og:image`; `scripts/brand/` generator. Protected URLs identical to S2; no horizontal scroll at 1280/390 light/dark | — (PR 2 after S4). PR 1 merged after S3; `main` merged into this branch |
| S4 | 2026-10-09 | `claude/busy-meitner-o4j18j` (from S3) | Copy signed off (D-02: three principles reworded, card point "no tracking"); About section on home, no name (D-06); contact `vastoceanlabs@gmail.com` (D-05); "Coming soon to Google Play" until the listing is public (D-13); `/re-direct/` app page from the store listing and privacy policy, with five screenshots; card links to it. Protected URLs identical to S3; no horizontal scroll at 1280/390 light/dark | PR 2 (S3 + S4) |
