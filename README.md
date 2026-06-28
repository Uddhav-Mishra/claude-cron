# Claude Code "Hi" Cron Job (Render)

Runs `claude -p "hi"` against **Claude Code** twice a day — **11:00 AM IST** and
**4:00 PM IST** — using your **subscription** (Pro/Max), not API credits.

## How it works

- `send_hi.py` shells out to the `claude` CLI in non-interactive print mode.
- Auth is headless via the `CLAUDE_CODE_OAUTH_TOKEN` env var.
- The `Dockerfile` builds a Node + Python image with the Claude Code CLI installed.

## Schedule

Render cron schedules run in **UTC**. IST is UTC+5:30, so:

| IST time | UTC time | Cron field |
|----------|----------|------------|
| 11:00 AM | 05:30    | minute 30, hour 5  |
| 4:00 PM  | 10:30    | minute 30, hour 10 |

Both are combined in `render.yaml`: `30 5,10 * * *`

## 1. Generate a subscription token

On your machine (already logged into Claude Code):

```bash
claude setup-token
```

Copy the printed token (`sk-ant-oat...`). This requires a Pro/Max subscription.

## 2. Deploy on Render

1. Push this repo to GitHub/GitLab.
2. In Render: **New → Blueprint**, point it at the repo (`render.yaml` is auto-detected).
3. When prompted, set `CLAUDE_CODE_OAUTH_TOKEN` to the token from step 1
   (it is `sync: false`, so it is never stored in the repo).
4. Create the resources. Render runs `python3 send_hi.py` on the schedule above.

## Run locally

```bash
export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat...
python3 send_hi.py
```

(If you are already logged in via `claude login`, the CLI works locally without the
token — the token is what makes it work in the headless Render container.)

## Notes

- This uses your Claude Code **subscription usage limits**, not API billing.
- Render cron jobs require a paid instance type (`plan: starter`).
