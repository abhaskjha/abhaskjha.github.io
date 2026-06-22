# Website Update Checklist

Use this for future `update` requests on `abhaskjha.github.io`.

## Scope

Assume `update` means:

1. Refresh `data/latest-writing.json`
2. Publish it if changed
3. Verify the live feed

Do not reread or redesign the full site unless the user asks.

## Read Only

- `WEBSITE_UPDATE_HANDOVER.md`
- `README.md`
- `data/latest-writing.json`
- `scripts/update_writing_feeds.py`
- `.github/workflows/update-writing-feeds.yml`

## Fast Path

1. Check repo state:
   - `git status --short --branch`
   - `git log --oneline --decorate -n 5 --all`
2. If repo looks healthy, run:
   - `python3 scripts/update_writing_feeds.py`
3. Sanity-check:
   - `sed -n '1,120p' data/latest-writing.json`
4. If no diff, stop:
   - `git diff -- data/latest-writing.json`
5. If changed, publish:
   - `git add data/latest-writing.json`
   - `git -c user.name='Abhas Jha' -c user.email='39115121+abhaskjha@users.noreply.github.com' commit -m 'Refresh writing feeds'`
   - `git push`

## Verify

Check in this order:

1. Repo file is current
2. `curl -L https://abhaskjha.github.io/data/latest-writing.json`
3. `curl -L 'https://abhaskjha.github.io/data/latest-writing.json?ts=YYYYMMDD-check'`

Trust the cache-busted URL over the plain URL.

## Expected Current Signals

As of June 21, 2026:

- Substack should start with `The ESRI Trap`, `Mogadishu and the Invisible City`, `Why Buildings Fall Down`
- India Decoded should start with `How China's EV Industry Grew, and What India Can Draw From It`

## If Repo Is Sick

If you see any of these:

- `HEAD (no branch)`
- rebase in progress
- `.git/index.lock` errors
- `.git` write failures

Do not spend tokens debugging local Git. Use the fallback publish path.

## Fallback Publish Path

1. Refresh `data/latest-writing.json` in the workspace
2. `git fetch origin` if possible
3. `git clone --no-checkout /Users/abhasjha/Documents/Codex/2026-04-18-i-want-you-to-create-a /private/tmp/abhaskjha-github-site-refresh-local`
4. `git branch -a --verbose --no-abbrev`
5. `git checkout -b main <latest-origin-main-sha>`
6. `cp /Users/abhasjha/Documents/Codex/2026-04-18-i-want-you-to-create-a/data/latest-writing.json /private/tmp/abhaskjha-github-site-refresh-local/data/latest-writing.json`
7. `git add data/latest-writing.json`
8. `git -c user.name='Abhas Jha' -c user.email='39115121+abhaskjha@users.noreply.github.com' commit -m 'Refresh writing feeds'`
9. `git remote add github git@github.com:abhaskjha/abhaskjha.github.io.git`
10. `git push github main`

## Known Pitfalls

- Scheduled GitHub Action can race your push with `Update writing feeds`
- GitHub connector writes may fail with `403 Resource not accessible by integration`
- Local tracking refs may be stale

## Automation

- Workflow: `.github/workflows/update-writing-feeds.yml`
- Schedule: `17 11 * * *` UTC
- Sources:
  - `https://abhaskjha.substack.com/feed`
  - `https://www.linkedin.com/newsletters/india-decoded-7226815406265577473/`
