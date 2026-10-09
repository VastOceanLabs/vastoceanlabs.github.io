# Decisions

One entry per decision. Status is **Decided** or **Open**. Open items name the
session that needs them; that session asks the user before building on them.
Don't re-open a decided item unless the user asks — add a new entry that
supersedes it instead.

| ID | Decision | Status | Needed by |
|---|---|---|---|
| D-01 | Site tooling: Jekyll on GitHub Pages | Decided (S2, user confirmed) | — |
| D-02 | Home page copy: S1 copy with three principles reworded | Decided (S4, user) | — |
| D-03 | Studio logo / wordmark: user's sunset-over-the-sea mark + Nunito wordmark | Decided (S3, user) | — |
| D-04 | Typeface: Nunito (self-hosted) for headings, system fonts for text | Decided (S3, user) | — |
| D-05 | Public contact email: vastoceanlabs@gmail.com | Decided (S4, user) | — |
| D-06 | About: short home page section, no personal name | Decided (S4, user) | — |
| D-13 | Play button shows "Coming soon" until the listing is public | Decided (S4, user) | — |
| D-07 | Custom domain or stay on vastoceanlabs.github.io | Open | S6 |
| D-08 | Link-check CI on PRs | Open | S5 |
| D-09 | Visual direction: reuse re-direct palette (cream/teal) for the studio | Superseded by D-12 | — |
| D-10 | One PR per milestone; sessions stack branches | Decided (S1, user) | — |
| D-11 | Keep GitHub Pages' default theme enabled (don't set `theme`) | Decided (S2) | — |
| D-12 | Studio palette: re-direct's cream with the studio's own deeper ocean blues | Decided (S3, user) | — |

## D-01 — Jekyll on GitHub Pages
**Proposed in S1; confirmed by the user at the start of S2.**
GitHub Pages already runs Jekyll on this repo (`_config.yml` exists), so
layouts, includes and data files cost no build step, no CI and no hosting
change. It gives shared header/footer, one data file per app, and a blog path
later. Alternatives (Astro, Eleventy, plain HTML) either need a CI deploy
workflow or repeat markup on every page.
Constraint: only GitHub Pages' whitelisted plugins (e.g. `jekyll-sitemap`,
`jekyll-seo-tag`).

## D-02 — Home page copy
**Decided by the user in S4.** The S1 draft (written by Claude) was checked
against the app. Hero, lede, Apps intro and "Local-first" stay as they were.
Three principles were reworded so they stay true of re-direct, which has an
in-app Insights (store listing: "Analytics") screen and a bounded
"Scroll & return" reset:
- No tracking: "No ads, no tracking, and nothing about you sent anywhere: no
  analytics or third-party SDKs phoning home."
- Calm by design: "Optional reminders that back off when you ignore them,
  gentle defaults, and nothing built to keep you scrolling."
- Plain-language policies: "Privacy policies with a plain-English summary up
  top, and updated before anything changes."
The re-direct card point "No account, no ads, no analytics" became "…no
tracking" for the same reason.

## D-03 — Studio logo
**Decided by the user in S3.** The mark is the user's own artwork: a disc
split at the horizon, with a pale sky and the sun cut out of it above, and a
deep sea with two wave lines cut out of it below. It is recoloured to the
D-12 palette: sky `#8EBFD6`, sea `#0B3A52` (`#24597A` on dark backgrounds),
cut-outs cream `#FAF6F0`. Next to it is the Nunito wordmark.
History: a drawn wave mark was chosen first (other options offered were a
ChatGPT-generated symbol, or a wordmark only). Later in S3 the user supplied
this artwork and asked to use it instead.
Files: `assets/img/logo-mark.svg` (also `favicon.svg`), `logo.svg` (lockup
for light backgrounds), `logo-dark.svg` (for dark backgrounds),
`/favicon.ico`, `apple-touch-icon.png`, `og-default.png`. The header
includes `_includes/logo-mark.svg`, which is coloured by CSS so it follows
the colour scheme.
Source: `scripts/brand/source/mark-source.webp`. `trace_mark.py` turns it
into `source/mark-paths.json`, and `scripts/brand/build.sh` rebuilds every
logo and icon file from those paths (colours live in `make_logo.py` and the
`--mark-*` tokens).

## D-04 — Typeface
**Decided by the user in S3.** Nunito (SIL OFL) for headings and the wordmark,
weight 800; system font stack for body text. Self-hosted as one variable
woff2, Latin subset only, about 39 KB (`assets/fonts/`, licence alongside), so
there are no third-party requests. It is the same rounded face as the re-direct
feature graphic, which ties studio and app together. Options offered were:
this; system fonts only; Inter for headings. The logo files use Nunito
converted to outlines, so they need no font.

## D-05 — Contact email
**Decided by the user in S4:** `vastoceanlabs@gmail.com` (set as `email` in
`_config.yml`; the home page Contact section uses it). Options offered were
keeping the personal address or a dedicated one.
Follow-up in the app repo (not this repo): the policy pages still show the
old address until `docs/PRIVACY_POLICY.md` (header and Contact),
`docs/ACCESSIBILITY_DISCLOSURE.md` (Contact) and
`docs/PLAY_CONSOLE_SUBMISSION.md` are changed, `scripts/sync_web_docs.js` is
re-run and the generated `re-direct/*.md` are copied here. The Play Console
developer contact email should change too.

## D-06 — About
**Decided by the user in S4:** a short "About" section on the home page
(`#about`, in the header nav), not a separate page, and it does not name the
founder. It says Vast Ocean Labs is a one-person studio, which the Play
listing already says ("Built by one person"). Options offered were: this; the
same section naming the user; a separate `/about/` page.

## D-13 — Store button before launch
**Decided by the user in S4:** re-direct isn't publicly on Google Play yet
(testing), so the site shows "Coming soon to Google Play" as text, not a
link. `_data/apps.yml` keeps the store URL with `store.live: false`; set
`live: true` when the listing is public and the cards and app page switch
to the "Get it on Google Play" button. The protected `/r/` page still links
to Google Play; left untouched.

## D-07 — Custom domain
App Links only work from the domain root and the app's `promptHost` is
`vastoceanlabs.github.io`. Moving to a custom domain needs an app rebuild, and
links already sent will only reach the fallback page. Decide before launch.

## D-08 — Link-check CI
A GitHub Action that builds the site and checks links/protected URLs on every
PR. Cheap insurance as the site grows; decide in S5.

## D-09 — Visual direction
The studio site reuses the re-direct palette (cream `#FAF6F0`, teal
`#5E8B87`, deep `#0D474C`) and ocean waves. Revisit in S3 if the studio wants
its own identity separate from its first app.

## D-12 — Studio palette (supersedes D-09)
**Decided by the user in S3**, when asked whether D-09 should be revisited.
Keep re-direct's cream background, but give the studio its own deeper ocean
blues so later apps can bring their own colours without clashing:

| Token | Light | Dark |
|---|---|---|
| `--bg` | `#FAF6F0` | `#121A1E` |
| `--surface` | `#FFFFFF` | `#1A242A` |
| `--ink` / `--muted` | `#263238` / `#56616A` | `#E6E8E6` / `#A3AFB5` |
| `--brand` (links, buttons) | `#2B6A88` | `#8EBFD6` |
| `--deep` (headings, logo) | `#0B3A52` | `#D3E6EF` |
| `--wave-1` / `--wave-2` | `#D9E8EE` / `#B5D3E0` | `#172328` / `#1D3440` |

The old brand teal `#5E8B87` failed WCAG AA for links and white button text
(3.5:1 and 3.8:1); `#2B6A88` passes (5.5:1 on the background, 6.0:1 under
white text). The standalone `/r/` page keeps re-direct's own colours; it is
the app's page, not the studio's.

## D-10 — Build process
Decided by the user in S1: work through planned sessions in order, update the
docs at the end of each session, and open PRs occasionally (one per
milestone).

## D-11 — GitHub Pages default theme
**Decided in S2.** With no `theme` in `_config.yml`, GitHub Pages applies its
Primer theme. Our own `_layouts/default.html` and `page.html` override the
theme's layouts, so Primer no longer styles anything; it only still writes an
unused `/assets/css/style.css`. Setting `theme: null` would remove that file,
but how Pages treats it can't be checked locally, so it is left alone to keep
the live build predictable. Don't name our stylesheet `style.css` (it would
clash); ours is `site.css`.
