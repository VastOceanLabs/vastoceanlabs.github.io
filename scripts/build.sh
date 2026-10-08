#!/bin/sh
# Build the site locally the way GitHub Pages does (github-pages gem, its
# default plugins and theme). Output goes to _site/ unless a path is given.
#
#   scripts/build.sh            # build into _site/
#   scripts/build.sh serve      # build and serve on http://127.0.0.1:4000
#
# First run: `bundle config set --local path vendor && bundle install`.
set -e
cd "$(dirname "$0")/.."
export LANG=C.UTF-8 LC_ALL=C.UTF-8 JEKYLL_ENV=production
# jekyll-github-metadata calls the GitHub API; point it at nothing so local
# builds work offline. Only affects site.github values, which the site doesn't use.
export PAGES_REPO_NWO=VastOceanLabs/vastoceanlabs.github.io
export PAGES_API_URL=http://127.0.0.1:9 NO_PROXY=127.0.0.1 no_proxy=127.0.0.1
if [ "$1" = "serve" ]; then
  exec bundle exec jekyll serve --host 127.0.0.1
fi
bundle exec jekyll build -d "${1:-_site}"
