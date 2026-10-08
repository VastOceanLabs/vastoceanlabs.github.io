# Build plan

The site is built in **sessions** grouped into **milestones**. Each session has
one scope and a definition of done. Each milestone ends with one PR into
`main`, so every PR is a reviewable, working step and `main` is never left
half-built.

Decisions referenced as `D-nn` live in [DECISIONS.md](DECISIONS.md). Current
progress lives in [STATUS.md](STATUS.md).

## How the build runs

**Order of work.** Structure before content, content before polish, polish
before launch. Each session only depends on sessions before it, so nothing is
built twice: e.g. the shared layout (S2) exists before new pages are added
(S4), and the brand assets (S3) exist before SEO and share images are wired up
(S5).

**Decisions first.** Each session lists the decisions it needs. If one is
still open when the session starts, the session asks the user before building
anything that depends on it.

**Branches.** Each session works on its own branch, started from the previous
session's branch (named in STATUS.md). Commits stack up across a milestone;
the last session of the milestone opens the PR from its branch, which carries
the whole milestone. After that PR merges, the next milestone starts from
`main`.

**PR cadence.** One PR per milestone (about one PR every 2 sessions). A PR is
opened outside that rhythm only if the user asks, or if something must go live
sooner (e.g. a fix to a policy page or `/r/`).

**Handoff.** Every session ends by updating STATUS.md (see `CLAUDE.md`), so
the next session can start without this conversation.

## Site architecture (set up in S2)

Built for growth without a rewrite. GitHub Pages builds Jekyll natively, so
there is no build step or CI to maintain (D-01).

```
_config.yml              site settings (title, url, contact email), exclusions,
                         default "page" layout for Markdown pages
_data/apps.yml           one entry per app -> home page cards + footer links
_data/navigation.yml     header navigation
_layouts/default.html    shared shell: head, header, <main>, footer
_layouts/page.html       Markdown/text pages (the policies); wraps in .prose
_layouts/app.html        app detail page (added in S4)
_includes/head.html      <head>: title, description, canonical, Open Graph
_includes/header.html    skip link, wordmark, nav
_includes/footer.html    copyright + footer links from apps.yml
_includes/app-card.html  one app card, rendered from apps.yml
assets/css/site.css      design tokens at the top, then components
assets/img/              logo SVGs, favicon.svg, apple-touch icon, og-default.png (S3)
assets/img/apps/         app icons (512px PNG)
assets/fonts/            self-hosted Nunito (D-04)
favicon.ico              root, so browsers' automatic /favicon.ico request works
index.html               home page content (front matter: layout default)
<app-slug>/              one folder per app: its policy pages (+ index.html, S4)
r/                       re-direct prompt fallback (standalone, untouched)
.well-known/             App Links (untouched)
docs/, scripts/          planning docs, the local build script and scripts/brand/
                         (logo/icon generator) — not published
```
Adding a second app later = one `_data/apps.yml` entry + one folder. Adding a
blog later = a `_posts/` folder. Neither needs layout changes.

**Building locally:** `scripts/build.sh` (see README). It mirrors GitHub
Pages, including its default plugins and theme, and works offline.

## Milestone A — Foundations  → PR 1

### S1 — First draft and plan ✅
- Home page first draft (`index.html`): hero, re-direct card, principles,
  contact, footer. Light/dark, mobile.
- Planning docs: `CLAUDE.md`, `docs/PLAN.md`, `docs/DECISIONS.md`,
  `docs/STATUS.md`. README corrected for this repo.

### S2 — Site structure (Jekyll) ✅
Needs: D-01.
- Move shared CSS to `assets/css/site.css` with the design tokens.
- Create `_layouts/default.html` and `_includes/` (head, header, footer).
- Create `_data/apps.yml` with re-direct; render the home page app cards from it.
- Give the policy pages the shared layout (check how GitHub Pages renders the
  front-matter-less `re-direct/*.md` — they must stay hand-edit-free, see
  CLAUDE.md).
- Exclude `docs/`, `CLAUDE.md` etc. from the build; keep `.well-known` included.
- Build locally with the `github-pages` gem and check: all protected URLs
  exist in `_site/`, `assetlinks.json` is byte-identical, `/r/` unchanged,
  pages look the same as S1 in all four views.

Done when: the built site matches S1 visually, protected URLs pass, docs
updated. **Open PR 1** (S1 + S2) into `main`.

## Milestone B — Brand and content  → PR 2

### S3 — Brand identity ✅
Needs: D-03 (studio logo), D-04 (typeface). Also settled D-12 (palette).
- Studio logo/wordmark (SVG), favicon set, apple-touch icon.
- Finalise design tokens (colour, type scale, spacing) in `site.css`.
- Social share image for the home page (1200×630), wired up as `og:image`
  with a `page.og_image` front-matter override.
- `scripts/brand/build.sh` regenerates every logo and icon file.

### S4 — Content and app page
Needs: D-02 (copy sign-off), D-05 (contact email), D-06 (about content).
- Final home page copy, signed off by the user.
- About section (or page, per D-06).
- re-direct app page at `/re-direct/` using `_layouts/app.html`: description,
  screenshots, features, policy links, Play button. Home card links to it.
- Contact details per D-05.

Done when: content approved by the user. **Open PR 2** (S3 + S4).

## Milestone C — Quality and launch  → PR 3

### S5 — Quality pass
- SEO: titles/descriptions per page, canonical URLs, Open Graph/Twitter tags
  from data, `jekyll-sitemap`, `robots.txt` (keep `/r/` noindex).
- Custom `404.html`.
- Accessibility audit (contrast, headings, focus, alt text) and fixes.
- Performance check (image sizes, no unused CSS).
- Optional: GitHub Action that builds the site and checks links on every PR,
  so later PRs can't break protected URLs (D-08).

### S6 — Launch
Needs: D-07 (custom domain or not).
- Merge PR 3; confirm Pages settings (branch `main`, root).
- Verify live: home, app page, policies, `/r/`, `assetlinks.json` JSON.
- If a custom domain is chosen: this changes App Links — the app's
  `promptHost` must change too (see README). Plan that with the app release.
- Write a short "how to add an app / page" guide in README.

Done when: live site verified. PR 3 = S5 (+ any S6 fixes).

## Milestone D — Growth (as needed, one PR each)

Not scheduled; picked up when wanted. Each is self-contained on the S2
structure.
- Second app: data entry + folder + policy pages.
- News/blog via `_posts/`.
- Press kit page (logos, screenshots, short bio).
- Newsletter or contact form (needs a third-party service — decide first).
