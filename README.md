# Claude Code "Hi" Cron Job

Runs `claude -p "hi"` against **Claude Code** twice a day — **11:00 AM IST** and
**4:00 PM IST** — using your **subscription** (Pro/Max), not API credits.

`send_hi.py` shells out to the `claude` CLI in non-interactive print mode and
authenticates headlessly via the `CLAUDE_CODE_OAUTH_TOKEN` env var.

## Schedule

Cron schedules run in **UTC**. IST is UTC+5:30, so:

| IST time | UTC time | Cron field |
|----------|----------|------------|
| 11:00 AM | 05:30    | minute 30, hour 5  |
| 4:00 PM  | 10:30    | minute 30, hour 10 |

Combined: `30 5,10 * * *`

## Get a subscription token

On your machine (already logged into Claude Code):

```bash
claude setup-token
```

Copy the printed token (`sk-ant-oat...`). Requires a Pro/Max subscription.

## Deploy (free) — GitHub Actions

The workflow lives at `.github/workflows/claude-hi.yml`.

1. Add the token as a repo secret:
   ```bash
   gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo Uddhav-Mishra/claude-cron
   # paste the sk-ant-oat... value when prompted
   ```
   (Or: GitHub repo → Settings → Secrets and variables → Actions → New repository secret.)
2. Push to GitHub. The schedule runs automatically.
3. Test now: GitHub repo → **Actions** → **claude-hi** → **Run workflow** (manual
   `workflow_dispatch`), then check the run logs for
   `Claude replied: Hi! How can I help you today?`

> Note: GitHub may pause scheduled workflows after ~60 days of repo inactivity, and
> scheduled runs can be delayed a few minutes under load.

## Deploy (paid alternative) — Render

`render.yaml` + `Dockerfile` define a Render **cron job** (a paid Render type).
Create a Blueprint from this repo, set `CLAUDE_CODE_OAUTH_TOKEN` when prompted.

## Run locally

```bash
export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat...
python3 send_hi.py
```

(If already logged in via `claude login`, the CLI works locally without the token.)

## Notes

- This uses your Claude Code **subscription usage limits**, not API billing.
