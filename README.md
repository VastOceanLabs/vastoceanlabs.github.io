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
offline. Layout of the source: see "Site architecture" in
[`docs/PLAN.md`](docs/PLAN.md). To add an app, add an entry to
`_data/apps.yml` and a folder for its pages.

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
