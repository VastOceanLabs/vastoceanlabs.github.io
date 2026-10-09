# Status

## Now

- **Milestone:** C (Quality and launch). S6 is in progress.
- **S6 so far:**
  - D-07 decided: stay on `vastoceanlabs.github.io`.
  - README has the "Adding an app or a page" guide.
  - PR 3 (S5 + S6) is open from `claude/funny-hypatia-ad36l3`.
- **Waiting on:** the "Site check" result on PR 3, then the user's merge,
  then the live checks.
- **Open PRs:** PR 3.

## Handoff (S6 in progress)

If this session stops before PR 3 is merged:
1. Check that "Site check" is green on PR 3.
2. Ask the user to merge it.
3. Run the live checks in [PLAN.md](PLAN.md#s6--launch):
   - home page, `/re-direct/` and both policy pages
   - `/r/#f=Test`
   - `assetlinks.json` is valid JSON
   - a missing path shows the custom 404
   - `robots.txt` and `sitemap.xml` load, and `/r/` is not in the sitemap
   - Pages settings are branch `main`, folder `/ (root)`

## What S5 changed

- **SEO.**
  - Every page now has a title and a description.
  - Indexable pages have a canonical URL. The 404 page has none and is
    `noindex` instead.
  - Share tags on every page: Open Graph, `og:site_name`, `og:locale` and
    `twitter:card` (`summary_large_image`).
  - The front-matter keys are listed at the top of `_includes/head.html`.
  - The policy pages get their meta descriptions from `_config.yml` defaults,
    so the synced `.md` files stay untouched. Those two descriptions are new
    text, written from the policies' own TL;DR and summary.
  - `jekyll-sitemap` is on, and `robots.txt` points to the sitemap.
  - `/r/` is unchanged and stays out of the sitemap (D-15).
- **404.** `404.html` uses the site layout. It is `noindex` and links to the
  home page and each app page.
- **Accessibility.**
  - Contrast: every text token passes AA on `--bg` and `--surface` in both
    themes. Light / dark:
    - `--muted` on `--surface`: 6.3 / 7.0
    - `.soon` (`--muted` on `--bg`): 5.9 / 7.9
    - `--brand`: at least 5.5
    - button text: 6.0 / 8.9

    The dark-mode cards use the same tokens on `--surface`.
  - Heading order is h1 → h2 → h3 on every page.
  - Alt text was already present. The inline SVGs are `aria-hidden`.
  - Screenshot row: at 390px it scrolls sideways, so it now takes keyboard
    focus (`tabindex="0"`, labelled). Arrow keys scroll it, and it shows an
    inset focus ring.
  - axe-core (WCAG 2.1 AA + best practice): no violations on any of the 16
    views.
- **Performance.** Nothing needed changing:
  - Images: icon 13 KB, og image 29 KB, screenshots 10–33 KB WebP (lazy
    after the first two).
  - No unused classes in `site.css`.
  - The Nunito preload is used on every page, by the headings.
- **CI (D-08).** `.github/workflows/site-check.yml` + `scripts/check-site.sh`.

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
- **App icon size:** `assets/img/apps/re-direct.png` is 512px (13 KB), shown
  at 120px. It stays full size so it can be swapped byte-for-byte with the
  app repo's icon (see the re-direct icon note). A smaller copy would save about 8 KB; not worth it
  yet.
- **Screenshots:** 540×1200 WebP, made from the app repo's
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
| S5 | 2026-10-09 | `claude/gracious-darwin-8mtg74` (from `main` after PR 2) | PR 2 merged (user). SEO: descriptions for every page, canonical, OG + `twitter:card`, `jekyll-sitemap`, `robots.txt`, `/r/` kept out of the sitemap without editing it (D-15). Custom `404.html`. Accessibility: contrast measured (all AA), keyboard-scrollable screenshot row, axe clean. Performance: no changes needed. CI: build + protected-URL check (D-08). `/re-direct/` keeps `og-default.png` (D-14). Protected URLs identical to `main`; no horizontal scroll at 1280/390 light/dark | — (PR 3 after S6) |
