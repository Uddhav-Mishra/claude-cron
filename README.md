# Claude "Hi" Cron Job

A free GitHub Actions workflow that says **"hi"** to Claude Code on a daily
schedule, using your Claude **subscription** (Pro/Max), not API credits.

It runs `claude -p "hi"` (via `send_hi.py`) on GitHub's servers, so nothing needs
to stay running on your machine. Default schedule: **11:00 AM and 4:00 PM IST**.

## Setup (2 steps)

### 1. Generate a login token
On your machine, with Claude Code installed and logged in:
```bash
claude setup-token
```
Copy the printed `sk-ant-oat...` value. (Requires a Pro/Max subscription.)

### 2. Add it as a repo secret
```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN
# paste the token when prompted
```
Or in the browser: **repo → Settings → Secrets and variables → Actions → New
repository secret**, name `CLAUDE_CODE_OAUTH_TOKEN`.

That's it. The schedule runs automatically.

## Set your own times & timezone (no YAML editing)

GitHub Actions cron is UTC-only and can't read variables, so this workflow runs
**hourly** and a gate step decides whether the current hour matches *your* local
time. Configure it with repo **Variables** (not secrets):

**repo → Settings → Secrets and variables → Actions → Variables → New variable**

| Variable    | Example        | Meaning                                      |
|-------------|----------------|----------------------------------------------|
| `TZ`        | `Asia/Kolkata` | Any IANA timezone (DST handled automatically)|
| `RUN_HOURS` | `11,16`        | Local hours to run, comma-separated (0–23)   |

Defaults (if you set nothing): `TZ=Asia/Kolkata`, `RUN_HOURS=11,16` → 11 AM & 4 PM IST.
Examples: New York at 9am & 6pm → `TZ=America/New_York`, `RUN_HOURS=9,18`.

## Test it now
**repo → Actions → claude-hi → Run workflow** (a manual run skips the time gate).
Check the logs for `Claude replied: Hi! How can I help you today?`

## Run locally
```bash
CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat... python3 send_hi.py
```
(If already logged in via `claude login`, the CLI works locally without the token.)

## Notes
- Uses your Claude Code **subscription limits**, not API billing.
- The CLI version and `actions/checkout` are pinned for supply-chain safety; bump
  them deliberately in `.github/workflows/claude-hi.yml`.
- GitHub may pause scheduled workflows after ~60 days of repo inactivity (any push
  re-enables them), and scheduled runs can be delayed a few minutes under load.
