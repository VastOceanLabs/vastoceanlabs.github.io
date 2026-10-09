# vastoceanlabs.github.io

The Vast Ocean Labs website, served by GitHub Pages from `main`.

**Building the site?** Start with [`CLAUDE.md`](CLAUDE.md), then
[`docs/STATUS.md`](docs/STATUS.md) (where things stand),
[`docs/PLAN.md`](docs/PLAN.md) (the session-by-session plan) and
[`docs/DECISIONS.md`](docs/DECISIONS.md) (what's been decided).

Besides the studio home page (`/`), the site serves four things for the
re-direct Android app. Their paths must not change:

| Path | What it's for |
|---|---|
| `/r/` | Fallback page for "Send a prompt" links (`https://<host>/r/#f=Mum`). Shown only when the link can't open the app directly. Has an "Open re-direct" button and a Play Store link. |
| `/.well-known/assetlinks.json` | Android App Links verification. Once valid, tapping a prompt link in WhatsApp / Messenger / SMS opens re-direct directly, with no browser step. |
| `/re-direct/privacy-policy.html` | Privacy policy URL for the Play Console (rendered from the `.md`). |
| `/re-direct/accessibility.html` | Accessibility-service disclosure URL for the Play Console. |

## Building locally

GitHub Pages builds the site from `main` with Jekyll; there is no build step
to run before pushing. To preview or check a change locally (Ruby required):

```
bundle config set --local path vendor && bundle install   # first time
scripts/build.sh          # build into _site/
scripts/build.sh serve    # serve on http://127.0.0.1:4000
```

The script mirrors GitHub Pages (same gem, default plugins and theme) and works
offline. `scripts/check-site.sh _site [<base-build>]` checks the protected
paths above (they exist, `assetlinks.json` is valid JSON, `/r/` stays noindex
and out of the sitemap, and, given a build of the base branch, that
`assetlinks.json`, `/r/index.html` and `/r/og.png` haven't changed). The
"Site check" GitHub Action runs it on every PR. A PR that changes one of those
files on purpose (e.g. a new fingerprint) needs the `protected-change` label.
Layout of the source: see "Site architecture" in
[`docs/PLAN.md`](docs/PLAN.md).

## Adding an app or a page

### A new app

1. **`_data/apps.yml`**: add an entry, using the `re-direct` entry as the
   model. The comment at the top of the file lists the keys. The entry
   drives the home page card, the footer links (`footer: true` on a link)
   and the links on the 404 page. Its `slug` is the app's folder name. Keep
   `store.live: false` until the store listing is public. Everything in the
   entry must be true of the shipped app.
2. **Icon and screenshots**: put a 512×512 PNG at
   `assets/img/apps/<slug>.png`. Phone screenshots go in
   `assets/img/apps/<slug>/` as 540×1200 WebP, listed under `screenshots`
   with alt text.
3. **The app folder `<slug>/`**:
   - `index.html` with front matter `layout: app`, `app: <slug>`, `title`,
     `tagline` and `description`. The layout draws the hero, store button,
     policy links and screenshots from `apps.yml`. The file itself holds
     only the app's own sections (see `re-direct/index.html`).
   - Policy pages: Markdown files (e.g. `privacy-policy.md`) get the `page`
     layout automatically and are served as `.html`. If they are synced from
     the app's repo without front matter, give them a meta description with
     a `defaults` entry in `_config.yml`, as the re-direct policies have.
     Then add them under `links` in `apps.yml`.
4. The home page "Apps" intro ("One app so far…") is written in
   `index.html`. Update it by hand.

### A new page

- An HTML or Markdown page with front matter gets the site layout
  (`layout: default`, or `page` for text pages; Markdown gets `page` by
  default).
- Set `title` and `description`. Every page needs both, for search results
  and share cards.
- To add it to the header, add an entry to `_data/navigation.yml`.

### Share images

Every page uses `assets/img/og-default.png` as its share image unless its
front matter sets `og_image: /path/to/image.png` (1200×630) and
`og_image_alt`. The keys `_includes/head.html` reads are listed at the top
of that file.

### The sitemap

- Every page is in `sitemap.xml` by default (`jekyll-sitemap`).
- To keep a page out of search, set `sitemap: false` and `noindex: true` in
  its front matter. That is how `404.html` is set up.
- A file without front matter (copied as is, like `/r/`) is kept out with
  a `defaults` entry in `_config.yml` instead.

### Checking the change

```
scripts/build.sh                                   # build into _site/
git fetch origin main
git worktree add --force --detach ../base origin/main   # or, if ../base exists:
                                                   # git -C ../base checkout --detach origin/main
BUNDLE_GEMFILE="$PWD/Gemfile" ../base/scripts/build.sh "$PWD/../base_site"
scripts/check-site.sh _site ../base_site           # same check as CI
```

Then preview with `scripts/build.sh serve`. Look at the new pages at desktop
width and at 390px, in light and dark mode, with no horizontal scroll. The
"Site check" workflow runs the same build and check on the PR.

## Brand files

Logo, favicons and the share image are generated, not hand-drawn:
`scripts/brand/build.sh` (requirements at the top of the script). The mark is
traced from `scripts/brand/source/mark-source.webp` by
`scripts/brand/trace_mark.py`; colours are in `scripts/brand/make_logo.py`.

## The host must match the app

The app is built for **`vastoceanlabs.github.io`**. That value lives in one
place: `promptHost` in [`app/build.gradle.kts`](../app/build.gradle.kts).
App Links only work from a domain **root**, so for a `github.io` host the
site has to be the organisation's root Pages repo.

## Publishing

Repo → Settings → Pages → Source: *Deploy from a branch*, `main`, `/ (root)`.
After a merge to `main`, check that
`https://vastoceanlabs.github.io/.well-known/assetlinks.json` loads as JSON.

If you would rather use your own domain (e.g. `redirect.vastoceanlabs.com`),
point it at the same repo, change `promptHost` in `app/build.gradle.kts`, and
rebuild. Links already sent with the old host will then only reach the
fallback page.

## Fill in `assetlinks.json` fingerprints

Replace the two `REPLACE_WITH_…` values with SHA-256 fingerprints
(colon-separated, uppercase):

- **Play app signing key**: Play Console → your app → Setup → App signing →
  "App signing key certificate" → SHA-256.
- **Upload key**: same page, "Upload key certificate". Or run
  `keytool -list -v -keystore <your.jks> -alias <alias>`.

The `.debug` entry already holds this machine's debug-key fingerprint, so
debug builds verify too.

After publishing, check verification on a phone with the release build installed:

```
adb shell pm verify-app-links --re-verify com.finepointrehab.redirect
adb shell pm get-app-links com.finepointrehab.redirect
```

`vastoceanlabs.github.io: verified` means links open the app directly.

## Keep the policy copies in sync

`re-direct/*.md` are generated from `docs/PRIVACY_POLICY.md` and
`docs/ACCESSIBILITY_DISCLOSURE.md` by `node scripts/sync_web_docs.js`, which also
rewrites repo-relative links. Re-run it whenever either doc changes, then copy
the app repo's `web/re-direct/*.md` into `re-direct/` here and push. Don't
edit the policy text in this repo.
