#!/bin/sh
# Rebuild every logo and icon file from source (decisions D-03, D-04).
#   pip install fonttools brotli uharfbuzz pillow
#   npm install playwright   (anywhere on NODE_PATH; needs a Chromium)
set -e
cd "$(dirname "$0")/../.."
tmp=$(mktemp -d)
python3 scripts/brand/make_logo.py
node scripts/brand/render.js "$tmp"
python3 scripts/brand/make_ico.py "$tmp"
rm -rf "$tmp"
echo "Brand assets written to assets/img/ and favicon.ico"
