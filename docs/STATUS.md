# Status

## Now

- **Milestone:** A — Foundations, complete. PR 1 (S1 + S2) is open into `main`.
- **Last session:** S2 — Site structure (Jekyll) (done)
- **Next session:** S3 — Brand identity. See [PLAN.md](PLAN.md#milestone-b--brand-and-content---pr-2).
- **Start S3 from:** `main`, once PR 1 is merged. If PR 1 is still open,
  ask the user to merge it first (or, if they prefer, start from
  `claude/gifted-galileo-lof422`; the milestone B PR then also carries A).
- **Open PRs:** PR 1 — Milestone A (see session log for the link).

## Handoff to S3

- S3 needs D-03 (logo) and D-04 (typeface) from the user before building.
  Ask both at the start. D-09 (reuse the re-direct palette) may be revisited
  at the same time if the user wants a separate studio identity.
- Where things go: logo/favicons in `assets/img/`, linked from
  `_includes/head.html` (the favicon currently points at the re-direct icon)
  and the wordmark in `_includes/header.html`. Colour/type tokens are at the
  top of `assets/css/site.css`. If a web font is chosen, self-host it under
  `assets/fonts/` (no third-party requests; fits the privacy stance).
- Share image (1200×630) goes in `assets/img/`; wire it into `head.html` as
  `og:image` with a front-matter override (`page.og_image`). Full SEO is S5.
- How to verify: `scripts/build.sh` (README → Building locally), then
  screenshot `/` and `/re-direct/privacy-policy.html` at 1280 and 390px, light
  and dark. Playwright needs a version matching the preinstalled Chromium
  (`/opt/pw-browsers/chromium-1194` → `playwright@1.56.1`), installed in the
  scratchpad, not the repo.

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

## Session log

| Session | Date | Branch | Summary | PR |
|---|---|---|---|---|
| S1 | 2026-10-08 | `claude/gifted-galileo-lof422` | Home page first draft; build plan, decision log, status docs, CLAUDE.md; README fixed for this repo | PR 1 |
| S2 | 2026-10-08 | `claude/gifted-galileo-lof422` | Jekyll structure: layouts, includes, `site.css` tokens, `apps.yml`/`navigation.yml`; policy pages on the site layout; mobile tables; local build script. Home page pixel-identical to S1; protected URLs byte-identical | PR 1 |
