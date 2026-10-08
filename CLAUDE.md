# Vast Ocean Labs site — working rules

This repo is the GitHub Pages site at https://vastoceanlabs.github.io
(studio home page, plus the re-direct app's link fallback, App Links file and
policy pages). The build is run as a series of planned sessions.

## Start of every session

1. Read `docs/STATUS.md` — where the last session stopped, what this session
   should do, which branch to start from.
2. Read `docs/PLAN.md` — the session you are running, its scope and its
   definition of done. Do only that session's scope. If something belongs to a
   later session, note it in `docs/STATUS.md` instead of doing it.
3. Read `docs/DECISIONS.md` — never re-open a decided item without the user
   asking. If this session needs an open decision, ask the user before
   building anything that depends on it.
4. Start your branch from the branch `docs/STATUS.md` names (normally the
   previous session's branch, or `main` after a milestone PR is merged):
   `git fetch origin <branch> && git checkout -B <your-branch> origin/<branch>`.

## End of every session

1. Update `docs/STATUS.md`: current state, the handoff for the next session
   (what to read, what branch to start from), and add a row to the session log.
2. Record any decision made this session in `docs/DECISIONS.md`.
3. If the plan changed, update `docs/PLAN.md` (don't leave it stale).
4. Commit and push. Open a PR only when the session is the last one of a
   milestone (see "PR cadence" in `docs/PLAN.md`), or when the user asks.

## Do not break these URLs

They are used by the re-direct Android app and the Play Console. Their paths
must keep working on every commit:

- `/r/` — prompt-link fallback page (standalone page; keep it self-contained)
- `/.well-known/assetlinks.json` — Android App Links verification
- `/re-direct/privacy-policy.html`, `/re-direct/accessibility.html`

`re-direct/*.md` are generated in the app repo (`scripts/sync_web_docs.js`) and
copied here. Don't hand-edit their text; changes to wording belong in the app
repo. Layout/styling around them is fine.

## Conventions

- Planning docs (`docs/`, `CLAUDE.md`, `README.md`) are excluded from the
  published site in `_config.yml`. Keep it that way when adding new ones.
- Check every visual change at desktop and phone width (390px), in light and
  dark mode, with no horizontal scroll.
- Copy on the site must be true of the apps today. Don't invent features,
  numbers or claims; ask.
