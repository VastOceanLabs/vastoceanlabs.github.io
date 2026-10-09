# Status

## Now

- **Milestones A, B and C are done.** PR 3 (S5 + S6) was merged into `main`
  on 2026-10-09 at the user's request (merge commit `decd2b5`) and deployed
  by GitHub Pages.
- **Last session:** S7 (launch follow-up), branch
  `claude/cool-albattani-2xye8s`, started from S6's branch.
- **Open PRs:** PR 4 (S6 docs commit + S7) into `main`. Merging is the
  user's call.
- **Next:** once PR 4 is merged, no session is scheduled. Milestone D items
  are picked up when wanted
  ([PLAN.md](PLAN.md#milestone-d--growth-as-needed-one-pr-each)). Start each
  from `main`. If PR 4 is still open, start from its branch instead.

## Live checks still to do (from S6)

**S7 (2026-10-09): still blocked.** The S7 container couldn't reach the host
either: curl got a 403 from the egress proxy on CONNECT, and web fetch
reported the domain as blocked. None of the boxes below are ticked, and no
results were made up. To run them from a session, add
`vastoceanlabs.github.io` under the environment's Network access → Allowed
domains (or pick a broader level), then start a new session. Or check them
in a browser.

S7 did re-confirm, locally: `.well-known/assetlinks.json` in this branch is
byte-identical to `main`, and a build of this branch matches a build of
`main` for `assetlinks.json`, `/r/index.html` and `/r/og.png`.

The S6 session container couldn't reach `vastoceanlabs.github.io`: its
network policy blocked the host, for both curl and web fetch. What was
confirmed instead:
- The `pages build and deployment` run for `decd2b5` succeeded. It built
  from branch `main`, source `/github/workspace/.` (the repo root).
- The deployed artifact contains every protected path, plus `404.html`,
  `robots.txt` and `sitemap.xml`.
- A local build of `decd2b5` passes `check-site.sh`:
  - `assetlinks.json` is valid JSON.
  - The sitemap lists only `/`, `/re-direct/` and the two policy pages, so
    `/r/` is not in it.

Still to check in a browser, by the user or by a session whose environment
allows the host:
- [ ] `/`, `/re-direct/`, `/re-direct/privacy-policy.html` and
      `/re-direct/accessibility.html` load with the new layout.
- [ ] `/r/#f=Test` shows the fallback page (screenshot at 390px).
- [ ] `/.well-known/assetlinks.json` is served as valid JSON and is
      byte-identical to the file in `main`.
- [ ] A missing path, e.g. `/nope`, shows the custom 404 with HTTP status
      404.
- [ ] `/robots.txt` and `/sitemap.xml` load, and `/r/` is not in the
      sitemap.
- [ ] Live `/` and `/re-direct/` at 1280px and 390px, light and dark, with
      no horizontal scroll.
- [ ] Repo → Settings → Pages shows "Deploy from a branch", `main`,
      `/ (root)`. The deploy logs point to this, but the setting itself
      can't be read from the session.

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

- **`protected-change` label:** not created yet (the user didn't ask in S6).
  Create it the first time a PR changes `assetlinks.json` or `/r/` on
  purpose.
- **Actions on Node 20:** `site-check.yml` moved to `actions/checkout@v5`
  in S7. Pages' own `upload-artifact@v4` warning is GitHub's to fix.
- **`assetlinks.json` fingerprints (checked in S7, file not changed):** the
  release entry `com.finepointrehab.redirect` still has the placeholder
  `REPLACE_WITH_PLAY_APP_SIGNING_KEY_SHA256`. Its second value
  (`5C:15:…:32:F4`) is a real fingerprint, presumably the upload key. The
  debug entry has one real fingerprint. Until the Play app-signing SHA-256
  is in, App Links won't verify for builds installed from Google Play. When
  the user gives the value, it's a protected change: ask before creating the
  `protected-change` label. Then run the `adb` verification (README, "Fill
  in fingerprints") with a release build.
- **Custom domain (D-07):** deferred. See D-07 for what a move involves.

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
| S6 | 2026-10-09 | `claude/funny-hypatia-ad36l3` (from S5) | D-07: stay on github.io for now. README guide "Adding an app or a page". PR 3 opened; Site check green on its first GitHub run, no workflow changes. Protected URLs identical to `main`; 16 views with no horizontal scroll. PR 3 merged (user) and deployed by Pages from `main`/root. Live HTTP checks blocked by the container's network policy (listed above) | [PR 3](https://github.com/VastOceanLabs/vastoceanlabs.github.io/pull/3) |
| S7 | 2026-10-09 | `claude/cool-albattani-2xye8s` (from S6) | Launch follow-up. Live checks still blocked by the container's network policy (curl proxy 403, web fetch blocked); left unticked. `site-check.yml` → `actions/checkout@v5`, nothing else changed. `assetlinks.json` reviewed: Play app-signing fingerprint is still a placeholder; file not changed. `build.sh` + `check-site.sh _site <main build>` pass; `assetlinks.json`, `/r/index.html`, `/r/og.png` identical to `main` | PR 4 |
