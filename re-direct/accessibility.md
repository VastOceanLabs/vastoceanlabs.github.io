# Accessibility Service Disclosure — re-direct

**App:** re-direct (Android, `com.finepointrehab.redirect`)
**Service class:** `com.finepointrehab.redirect.service.RedirectAccessibilityService`
**Permission declared:** `android.permission.BIND_ACCESSIBILITY_SERVICE`
**Configured at:** `app/src/main/res/xml/accessibility_service_config.xml`

This document is the public justification for re-direct's use of the Android
AccessibilityService API. It is referenced from the Play Console
**Permissions declaration → Accessibility** form and is intended to satisfy
Google Play's policy requirement that apps using accessibility APIs for
non-disability purposes disclose that use clearly.

It mirrors the in-app honest-disclosure copy shown on
`AccessibilityPermissionScreen` and the
`accessibility_service_description` string surfaced in the system
Accessibility settings list. All three sources tell the same story.

## What the service does

re-direct uses the AccessibilityService API for two narrow purposes that
together form the app's blocking and Scroll & return features. Both are
foreground-package observations — the service does **not** read on-screen
text, type into other apps, or perform actions on the user's behalf.

### Purpose 1 — App blocking ("Take a break instead")

When the user enables app blocking and adds an app to their block list, the
accessibility service detects when that app comes to the foreground and
surfaces a redirect overlay offering a short break. The overlay is drawn by
re-direct (using `SYSTEM_ALERT_WINDOW`); the accessibility service's only
role is detecting *which app reached the foreground*. The user can dismiss
the overlay and continue to the app at any time — re-direct does not, and
cannot, prevent app launches at the OS level.

### Purpose 2 — Scroll & return blocking-suppression

The Scroll & return recipe is an explicit, time-boxed scrolling session
chosen by the user. While such a session is active, re-direct's blocking
overlay must **not** fire on the chosen scroll-target app, because the user
just told us they want to scroll that app for a bounded window. The
accessibility service is the natural place to coordinate this: if the
foreground package matches the active scroll-target and a scroll session
is in flight, the overlay-trigger is suppressed for that package only,
for the duration of that session. When the timer expires, a sticky
overlay demanding "Return now" or "+2 minutes" appears on top of the
target app (locked decision §10 #8 in `REDIRECT_PROJECT_MAP.md`).

## What the service does not do

These restrictions are encoded directly in the service configuration; they
are not just policy commitments.

- **It does not read window content.** The service is configured with
  `android:canRetrieveWindowContent="false"`. The Android system will not
  deliver window content to the service even if a bug tried to ask for it.
  Text shown on screen — messages, posts, form input, passwords — is never
  visible to re-direct.
- **It does not perform actions.** The service does not call
  `performGlobalAction`, `performAction`, or any other method that injects
  taps, keystrokes, or navigation events into other apps.
- **It does not record keystrokes or input events.** Only
  `accessibilityEventTypes="typeWindowStateChanged"` is declared — a single
  event class that fires when a window comes to the foreground. Keystroke
  and text-change event classes are not declared.
- **It does not run when blocking is off.** The service can only be enabled
  by the user, in system Settings → Accessibility, and only after they have
  read re-direct's pre-permission rationale screen. Disabling app blocking
  in re-direct's own settings turns the overlay-trigger off but does not
  silently re-purpose the service.
- **It does not transmit anything.** re-direct does not declare the
  `INTERNET` permission. There is no off-device destination for the
  package-name signal to be sent to. See
  [PRIVACY_POLICY.md](PRIVACY_POLICY.md).

## Why an accessibility service rather than something narrower

Google Play asks apps using accessibility APIs for non-disability purposes to
justify why no alternative API would work. For re-direct:

- **`UsageStatsManager` is too slow.** Usage stats are aggregated and
  delivered with multi-second latency — unsuitable for a "redirect overlay
  before the user sees the blocked app" experience. We do request
  `PACKAGE_USAGE_STATS` for analytics ("most-opened apps today"), but it
  cannot do real-time foreground detection.
- **`UsageEvents` polling is wasteful.** Polling foreground state requires a
  constantly-running background process and still has 1–5 s latency. The
  user-experience cost is high (drains battery; misses fast foregrounds)
  and the privacy story is identical (we'd still be observing foreground
  packages).
- **No public API surfaces foreground-app transitions** with low latency.
  `AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED` is the only mechanism that
  delivers the signal we need in real time.

The locked decisions in `REDIRECT_PROJECT_MAP.md` §10 documents this
trade-off: accessibility is the *minimum-privilege* path to detect blocked-app
foregrounds, not a free pass to inspect on-screen content.

## How users control the service

- **Granting**: The first time a user enables app blocking, re-direct shows
  a pre-permission rationale screen explaining exactly what the service
  reads and what it ignores, then deep-links into system Settings →
  Accessibility for the user to flip the switch. There is no silent enable.
- **Revoking**: System Settings → Accessibility → re-direct → Off. The
  service stops receiving events immediately. re-direct's blocking and
  Scroll & return suppression features stop working; nothing else is
  affected.
- **Verifying**: System Settings → Accessibility shows re-direct in the
  installed-services list with the disclosure summary
  ("Detects when a blocked app comes to the foreground") and the full
  description ("re-direct uses this access to notice when a blocked app
  moves to the foreground so it can offer you a short reset. It only reads
  the package name of the app on screen — never message contents, what
  you type, or any UI text."). These strings are sourced from
  `res/values/strings.xml` and are the same strings the in-app rationale
  screen shows.

## Where to verify the claims in this document

| Claim | File | What to check |
|---|---|---|
| Window content is not read | `res/xml/accessibility_service_config.xml` | `canRetrieveWindowContent="false"` |
| Only window-state events are consumed | `res/xml/accessibility_service_config.xml` | `accessibilityEventTypes="typeWindowStateChanged"` |
| No `performGlobalAction` / synthetic input | `service/RedirectAccessibilityService.kt` | No call sites for `performGlobalAction`, `dispatchGesture`, or `setGestureDetectionEnabled` |
| No network egress | `AndroidManifest.xml` | No `<uses-permission android:name="android.permission.INTERNET" />` |
| Honest in-app disclosure | `ui/permissions/AccessibilityPermissionScreen.kt` | Pre-permission rationale screen body |
| System-settings disclosure | `res/values/strings.xml` | `accessibility_service_summary`, `accessibility_service_description` |

## Contact

Questions about this disclosure: **e.joyce01@gmail.com** (Vast Ocean Labs).
