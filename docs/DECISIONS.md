# Decisions

One entry per decision. Status is **Decided** or **Open**. Open items name the
session that needs them; that session asks the user before building on them.
Don't re-open a decided item unless the user asks — add a new entry that
supersedes it instead.

| ID | Decision | Status | Needed by |
|---|---|---|---|
| D-01 | Site tooling: Jekyll on GitHub Pages | Decided (S1, proposed; user can override) | S2 |
| D-02 | Home page copy sign-off | Open | S4 |
| D-03 | Studio logo / wordmark | Open | S3 |
| D-04 | Typeface | Open | S3 |
| D-05 | Public contact email | Open | S4 |
| D-06 | About: section on home page or separate page; what it says | Open | S4 |
| D-07 | Custom domain or stay on vastoceanlabs.github.io | Open | S6 |
| D-08 | Link-check CI on PRs | Open | S5 |
| D-09 | Visual direction: reuse re-direct palette (cream/teal) for the studio | Decided (S1, proposed) | — |
| D-10 | One PR per milestone; sessions stack branches | Decided (S1, user) | — |

## D-01 — Jekyll on GitHub Pages
**Decided in S1 (proposed by Claude; user may override before S2).**
GitHub Pages already runs Jekyll on this repo (`_config.yml` exists), so
layouts, includes and data files cost no build step, no CI and no hosting
change. It gives shared header/footer, one data file per app, and a blog path
later. Alternatives (Astro, Eleventy, plain HTML) either need a CI deploy
workflow or repeat markup on every page.
Constraint: only GitHub Pages' whitelisted plugins (e.g. `jekyll-sitemap`,
`jekyll-seo-tag`).

## D-02 — Home page copy
The S1 draft copy ("Calm software for a noisy world", the four principles) was
written by Claude. The principles are promises about the whole studio; the user
must confirm they are happy to make them.

## D-03 — Studio logo
The site currently uses the re-direct icon as its favicon. Options: text
wordmark only; a simple mark (e.g. wave) + wordmark; commission/own design.

## D-04 — Typeface
Currently the system font stack (fast, no external requests — fits the
privacy stance). Alternative: one self-hosted web font for headings.

## D-05 — Contact email
The S1 draft shows the personal address already published in the privacy
policy. Option: a dedicated address (e.g. hello@ on a custom domain, or a
separate Gmail). If it changes, the app repo's privacy policy should change
too.

## D-06 — About
Section on the home page vs `/about/`; whether it names the founder.

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

## D-10 — Build process
Decided by the user in S1: work through planned sessions in order, update the
docs at the end of each session, and open PRs occasionally (one per
milestone).
