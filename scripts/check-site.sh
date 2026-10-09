#!/bin/sh
# Check a built site for the URLs the re-direct app and Play Console rely on
# (CLAUDE.md, "Do not break these URLs"). Decision D-08. Run by CI on every PR;
# also handy locally after scripts/build.sh.
#
#   scripts/check-site.sh _site               # required files, valid JSON, /r/ noindex
#   scripts/check-site.sh _site base_site     # ...and protected files unchanged vs base
#
# A PR that changes a protected file on purpose (e.g. a new assetlinks
# fingerprint) sets ALLOW_PROTECTED_CHANGE=1; in CI that's the
# "protected-change" label.
set -u
site=${1:?usage: check-site.sh <site> [<base-site>]}
base=${2:-}
fail=0
bad() { echo "FAIL: $*"; fail=1; }

for f in index.html 404.html robots.txt sitemap.xml \
         r/index.html r/og.png .well-known/assetlinks.json \
         re-direct/index.html re-direct/privacy-policy.html re-direct/accessibility.html; do
  [ -s "$site/$f" ] || bad "missing or empty: /$f"
done

python3 -m json.tool "$site/.well-known/assetlinks.json" >/dev/null 2>&1 ||
  bad "/.well-known/assetlinks.json is not valid JSON"
grep -q 'name="robots" content="noindex"' "$site/r/index.html" 2>/dev/null ||
  bad "/r/ lost its robots noindex"
grep -q '/r/' "$site/sitemap.xml" 2>/dev/null && bad "/r/ is listed in sitemap.xml"
for f in re-direct/privacy-policy.html re-direct/accessibility.html; do
  grep -q '<main' "$site/$f" 2>/dev/null || bad "/$f has no <main>"
done

if [ -n "$base" ]; then
  for f in .well-known/assetlinks.json r/index.html r/og.png; do
    if ! cmp -s "$site/$f" "$base/$f"; then
      if [ "${ALLOW_PROTECTED_CHANGE:-0}" = 1 ]; then
        echo "note: /$f changed (allowed)"
      else
        bad "/$f differs from the base branch (if intended, add the protected-change label)"
      fi
    fi
  done
fi

[ "$fail" = 0 ] && echo "Site check passed: $site"
exit "$fail"
