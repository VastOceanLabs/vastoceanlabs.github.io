# Status

## Now

- **Milestone:** A — Foundations
- **Last session:** S1 — First draft and plan (done)
- **Next session:** S2 — Site structure (Jekyll). See [PLAN.md](PLAN.md#s2--site-structure-jekyll).
- **Start S2 from branch:** `claude/gifted-galileo-lof422`
- **Open PRs:** none. PR 1 opens at the end of S2.

## Handoff to S2

- `index.html` is a single self-contained page with inline CSS. S2 splits it
  into layout, includes, `assets/css/site.css` and `_data/apps.yml` without
  changing how it looks. The S1 screenshots are the reference (desktop, 390px
  mobile, dark).
- D-01 (Jekyll) is proposed; confirm with the user at the start of S2 if they
  haven't commented on it.
- `ruby` and `bundle` are available in the cloud container; install the
  `github-pages` gem to build locally. Playwright + the preinstalled Chromium
  work for screenshots (needs a Playwright version matching
  `/opt/pw-browsers/chromium-1194`, e.g. `playwright@1.56.1`, installed in a
  scratch directory, not the repo).
- Watch: GitHub Pages renders `re-direct/*.md` without front matter. Check
  whether the `default` layout gets applied to them automatically and that
  their URLs stay `.html`.

## Noted for later sessions

- S3: the favicon is currently `r/og.png` (the re-direct icon).
- S4: the re-direct card copy was written from the privacy policy; check it
  against the real app (break types, "nudge" feature naming).
- S5: no `404.html`, sitemap or share image yet.

## Session log

| Session | Date | Branch | Summary | PR |
|---|---|---|---|---|
| S1 | 2026-10-08 | `claude/gifted-galileo-lof422` | Home page first draft; build plan, decision log, status docs, CLAUDE.md; README fixed for this repo | — |
