# Status

## Now

- **Milestone:** B — Brand and content. S3 done; S4 next.
- **Last session:** S3 — Brand identity (done)
- **Next session:** S4 — Content and app page. See [PLAN.md](PLAN.md#s4--content-and-app-page).
- **Start S4 from:** `claude/keen-edison-jpo2qa` (S3's branch). It is built on
  PR 1's branch because PR 1 was still open when S3 started. If PR 1 has been
  merged by then, still start from `claude/keen-edison-jpo2qa`; PR 2 then
  shows only milestone B.
- **Open PRs:** [PR 1 — Milestone A](https://github.com/VastOceanLabs/vastoceanlabs.github.io/pull/1)
  (not merged at the end of S3). If it is still open when S4 ends, PR 2 also
  carries milestone A; say so in its description, or ask the user to merge
  PR 1 first.

## Handoff to S4

- S4 needs D-02 (copy sign-off), D-05 (contact email) and D-06 (about). Ask at
  the start, before writing copy.
- Brand is settled: D-03 (logo), D-04 (Nunito headings), D-12 (palette).
  Use the tokens at the top of `assets/css/site.css` (colour, `--text-*` type
  scale, `--space-*` spacing) rather than new literal values.
- The app page (`_layouts/app.html`) can set `og_image` in front matter for
  its own share image (see `_includes/head.html`); otherwise it gets
  `assets/img/og-default.png`.
- How to verify: as in S3. `scripts/build.sh`, serve `_site/`
  (`python3 -m http.server`), screenshot `/`, `/re-direct/privacy-policy.html`
  and the new `/re-direct/` page at 1280 and 390px in light and dark, check
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

- **S4 (re-direct icon):** the re-direct app icon has been redrawn in the app
  repo (branch `claude/keen-edison-jpo2qa` of `VastOceanLabs/re-direct`, not
  merged at the end of S3). Once it lands, replace
  `assets/img/apps/re-direct.png` with the app repo's
  `branding/store_listing/app_icon/out/app_icon_512.png`. `/r/og.png` could
  follow, but `/r/` is protected: a content-only change, same path, and
  check it still renders. Not done in S3 (studio brand only).
- **S5:** `twitter:card` tags and per-page share images are still to do (only
  `og:image` exists). Contrast: the new palette passes AA for text, links and
  buttons; still audit `--muted` on `--surface` and the dark-mode cards.
- **S5:** the font is preloaded on every page, including policy pages that only
  use it for headings. That's fine at 39 KB; revisit if more weights are added.

- **App repo (not this repo):** the policy header block (Effective date /
  Publisher / Contact / App) renders as one run-on line because the Markdown
  lines have no hard breaks. Fix in the app repo's `docs/PRIVACY_POLICY.md`
  and `ACCESSIBILITY_DISCLOSURE.md` (end lines with two spaces or a
  backslash, or make it a list), then re-sync. Pre-existing; not a site bug.
- S4: the re-direct card copy (now in `_data/apps.yml`) was written from the
  privacy policy; check it against the real app. The Apps intro "One app so
  far, built carefully." is hard-coded in `index.html`; change it when a
  second app arrives.
- S5: no `404.html`, sitemap or share image yet. Canonical and basic Open
  Graph tags exist in `head.html`.

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
| S3 | 2026-10-08 | `claude/keen-edison-jpo2qa` (from PR 1 branch) | Studio brand: wave mark + Nunito wordmark (D-03), self-hosted Nunito headings (D-04), deeper ocean palette (D-12, fixes AA contrast), type and spacing tokens, favicons, apple-touch icon, 1200×630 share image as `og:image`; `scripts/brand/` generator. Protected URLs identical to S2; no horizontal scroll at 1280/390 light/dark | — (PR 2 after S4) |
