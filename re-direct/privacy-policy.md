# Privacy Policy — re-direct

**Effective date:** 2026-10-07
**Publisher:** Vast Ocean Labs
**Contact:** e.joyce01@gmail.com
**App:** re-direct (Android, package `com.finepointrehab.redirect`)

re-direct is built local-first. **No personal data leaves your device.** This
policy explains what re-direct stores, why it stores it, what it never collects,
and what the permissions it requests are used for.

If we ever change the model — even adding a single network call — this policy
changes first, and the change is announced in [CHANGELOG.md](CHANGELOG.md)
before the release that contains it ships.

## TL;DR

- re-direct does not have a backend. There is no account, no login, no sync.
- Every piece of data re-direct stores lives in your device's app sandbox.
- re-direct does not contain advertising, analytics, telemetry, crash
  reporters, or third-party SDKs that talk to the internet.
- re-direct does not request the `INTERNET` permission. The OS will not let
  re-direct open a network socket even if a bug tried to.
- You can export everything re-direct knows about you as a CSV from
  Settings → Data → Export sessions, or wipe it all from Settings → Data →
  Delete all data.

## What re-direct stores on your device

re-direct keeps three local stores. None of them are uploaded.

1. **Session history** (Room database, app-private storage). One row per break
   you take: timestamp, trigger reason (Tired / Distracted / Planned), recipe
   (Breathe / Stretch / Look away / Quiet / Nature / Scroll & return), duration,
   whether you returned to the task you anchored, and the package name of the
   app you anchored to (if any). Used by the in-app Analytics screen.
2. **Settings** (DataStore preferences, app-private storage). Theme, default
   break duration, default recipe, notification toggles, quiet hours, blocked
   app list, adaptive cadence opt-in, accessibility preferences, onboarding
   completion flag, and — only if you type one — the name you sign prompts
   with (see below).
3. **Crash funnel** (rolling local file, app-private storage). When re-direct
   catches a non-fatal error it writes a single line to a capped local log so
   the next debug build can show you what happened. This file is **never**
   sent off device. It is overwritten as it grows; deleting app data clears it.

CSV exports (Settings → Data → Export) are written to a private cache directory
and shared with apps **you choose** through the Android share sheet. re-direct
does not send them anywhere on its own.

## Sending and receiving prompts

"Send a prompt" lets you nudge someone else to take a re-direct. re-direct
builds a short message plus a link (for example
`https://vastoceanlabs.github.io/r/#f=Mum`) and hands it to the messaging app
**you pick** — WhatsApp, Messenger, your SMS app, or anything in the Android
share sheet. re-direct does not send it itself and never learns who you sent
it to; your messaging app's own privacy terms apply to the message.

The only personal detail in the link is the name you choose to sign with
(optional). It sits after the `#`, a part of a web address that browsers never
send to a server.

When someone taps a prompt link:

- **If they have re-direct**, the link opens the app directly. The sender's
  name is shown on the break screen and the session is marked "Prompted" in
  their local history. Nothing is stored about the sender beyond that label.
- **If they don't**, the link opens a static page on GitHub Pages explaining
  the app, with a Google Play link. Like any website, GitHub receives a normal
  page request (such as IP address and browser type) under
  [GitHub's privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement);
  the sender's name is not part of that request. The page sets no cookies and
  runs no analytics.

## What re-direct does not collect

- No name, email address, phone number, or account identifier.
- No advertising identifier, no Google Play Services advertising ID.
- No device identifiers (IMEI, MAC address, Android ID).
- No location data of any kind, coarse or fine.
- No contacts, calendars, photos, microphone, or camera data.
- No web-browsing history.
- No messages, keystrokes, or on-screen text content. The accessibility
  service is explicitly configured with `canRetrieveWindowContent="false"`
  and only reads the package name of the app currently in the foreground —
  see [ACCESSIBILITY_DISCLOSURE.md](ACCESSIBILITY_DISCLOSURE.md).
- No analytics events, no usage telemetry, no opt-in research panel.

## Permissions re-direct requests, and what each is used for

re-direct's design rule is that any permission ask should be obvious from the
feature you just tapped on. There is exactly one runtime permission prompt at
first run.

| Permission | Type | What it is used for |
|---|---|---|
| `POST_NOTIFICATIONS` | Runtime, asked once at first run | Active-break countdown notification, optional reminder nudges, scroll-expiry fallback. Skippable — re-direct works without it. |
| `FOREGROUND_SERVICE` + `FOREGROUND_SERVICE_SPECIAL_USE` | Install-time | Keeps the break-countdown timer accurate while the screen is off so you can put the phone face-down during a rest break. Subtype declared as `specialUse` because the timer — not media playback — is the primary purpose. |
| `WAKE_LOCK` | Install-time, normal | Held only while a break, sprint, or scroll session timer is ticking; released the instant all timers return to idle. Prevents the OS from throttling the timer during long screen-off windows. |
| `SYSTEM_ALERT_WINDOW` (Display over other apps) | Special, toggled in system Settings | Draws the redirect overlay on top of a blocked app the moment it reaches the foreground, and powers the Scroll & return sticky-overlay when a scroll session expires. |
| `PACKAGE_USAGE_STATS` (Usage access) | Special, toggled in system Settings | Powers the "most-opened apps today" tile in Analytics and feeds the recipe recommender's time-of-day signal. |
| `BIND_ACCESSIBILITY_SERVICE` | Special, toggled in system Accessibility settings | Detects when a blocked app comes to the foreground so re-direct can offer the redirect overlay, and suppresses block-redirect for your chosen scroll-target while a Scroll & return session is active. Reads **only** the foreground package name — see [ACCESSIBILITY_DISCLOSURE.md](ACCESSIBILITY_DISCLOSURE.md). |
| `BIND_QUICK_SETTINGS_TILE` | Signature, held by the system | Lets the OS bind the "Take a re-direct" Quick Settings tile. |
| Package visibility (`<queries>` for `ACTION_MAIN` / `CATEGORY_LAUNCHER`) | Install-time, narrow | Lets the anchor-screen "Returning to" picker and the block-list app picker list apps you can launch from your home screen. We deliberately do **not** request the broader `QUERY_ALL_PACKAGES` permission. |
| Package visibility for WhatsApp, WhatsApp Business, Messenger and the SMS app | Install-time, narrow | Lets "Send a prompt" show a button for each of those apps only when it is installed. Nothing is read from those apps. |

## Children

re-direct is not directed at children under 13. We do not knowingly collect
personal information from anyone, and we do not have a backend that *could*
collect it.

## Security

Because data never leaves the device, the relevant safeguards are the ones
Android already provides: app-sandboxed storage, Auto Backup with rules that
exclude sensitive caches (see `xml/backup_rules.xml` and
`xml/data_extraction_rules.xml`), and a `FileProvider` that grants temporary
read access to CSV exports only when you initiate a share.

re-direct does not encrypt the local Room database with a passphrase. Treat
device PIN/biometric lock as the trust boundary — anyone who can unlock your
phone can open any app on it, re-direct included.

## Your control

- **Export everything**: Settings → Data → Export sessions (CSV).
- **Delete everything**: Settings → Data → Delete all data wipes the Room
  database, settings, crash funnel, and cancels all scheduled reminders.
- **Uninstall** the app and Android removes the entire sandbox.

You do not need to contact us to delete your data — there is no copy of it
anywhere except on your device.

## Changes to this policy

If a future version of re-direct ever introduces a network call, a third-party
SDK, an account system, or any new data collection, this policy will be updated
**before** that release ships, and the change will be flagged in
[CHANGELOG.md](CHANGELOG.md) under a "Privacy" heading.

## Contact

Questions about this policy: **e.joyce01@gmail.com**.
