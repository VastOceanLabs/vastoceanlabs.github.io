# web/ — the public site behind prompt links and the privacy policy

This folder is the full content of a GitHub Pages site. It is **not** part of
the app build. It serves four things:

| Path | What it's for |
|---|---|
| `/r/` | Fallback page for "Send a prompt" links (`https://<host>/r/#f=Mum`). Shown only when the link can't open the app directly. Has an "Open re-direct" button and a Play Store link. |
| `/.well-known/assetlinks.json` | Android App Links verification. Once valid, tapping a prompt link in WhatsApp / Messenger / SMS opens re-direct directly, with no browser step. |
| `/re-direct/privacy-policy.html` | Privacy policy URL for the Play Console (rendered from the `.md`). |
| `/re-direct/accessibility.html` | Accessibility-service disclosure URL for the Play Console. |

## The host must match the app

The app is built for **`vastoceanlabs.github.io`**. That value lives in one
place: `promptHost` in [`app/build.gradle.kts`](../app/build.gradle.kts).
App Links only work from a domain **root**, so for a `github.io` host the
site has to be the organisation's root Pages repo.

## Publish (one time)

1. On GitHub, under the **VastOceanLabs** account, create a **public**
   repo named exactly `vastoceanlabs.github.io`.
2. Copy everything in this folder (including the hidden `.well-known/`) into
   that repo and push.
3. Repo → Settings → Pages → Source: *Deploy from a branch*, `main`, `/ (root)`.
4. Check that `https://vastoceanlabs.github.io/.well-known/assetlinks.json`
   loads as JSON.

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
`web/` into the `vastoceanlabs.github.io` repo and push.
