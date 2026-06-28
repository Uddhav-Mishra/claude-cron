# Claude "Hi" Cron Job

A free GitHub Actions workflow that says **"hi"** to Claude Code twice a day —
**11:00 AM** and **4:00 PM IST** — using your Claude **subscription** (Pro/Max),
not API credits.

It runs `claude -p "hi"` (via `send_hi.py`) on GitHub's servers, so nothing needs
to stay running on your machine.

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

## Test it now
**repo → Actions → claude-hi → Run workflow.** Check the logs for
`Claude replied: Hi! How can I help you today?`

## Change the schedule
Edit the cron line in [`.github/workflows/claude-hi.yml`](.github/workflows/claude-hi.yml).
Times are **UTC** (IST is UTC+5:30):

| IST      | UTC   |
|----------|-------|
| 11:00 AM | 05:30 |
| 4:00 PM  | 10:30 |

Current value `30 5,10 * * *` = "minute 30 of hours 5 and 10, every day."

## Notes
- Uses your Claude Code **subscription limits**, not API billing.
- GitHub may pause scheduled workflows after ~60 days of repo inactivity (any push
  re-enables them), and scheduled runs can be delayed a few minutes under load.
- Run locally: `CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat... python3 send_hi.py`
