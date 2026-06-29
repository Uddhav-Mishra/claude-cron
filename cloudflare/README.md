# Cloudflare Worker deploy

An alternative to the GitHub Actions workflow. Cloudflare Cron Triggers fire
reliably and on time (GitHub's scheduled cron is best-effort and frequently
dropped), so this version needs no catch-up/dedupe logic — it just sends at the
four scheduled times.

It calls the same Messages API path as `../send_hi.py`, billed to your Claude
subscription via the `CLAUDE_CODE_OAUTH_TOKEN`.

## Deploy

```bash
cd cloudflare
npm install              # installs the pinned wrangler (package.json)
```

Authenticate with Cloudflare, then deploy. Two auth options:

**Option A — API token (recommended; non-interactive).** Create a token at
dash.cloudflare.com → My Profile → API Tokens → **Edit Cloudflare Workers**
template, then put it in the repo's `.env` (gitignored):

```bash
# .env
CLOUDFLARE_API_TOKEN=...
```

```bash
set -a; source ../.env; set +a     # loads CLOUDFLARE_API_TOKEN + CLAUDE_CODE_OAUTH_TOKEN
npx wrangler deploy
printf '%s' "$CLAUDE_CODE_OAUTH_TOKEN" | npx wrangler secret put CLAUDE_CODE_OAUTH_TOKEN
```

**Option B — interactive browser login.** Run in a real terminal (not a wrapped
shell, which can't complete the OAuth callback):

```bash
npx wrangler login
npx wrangler deploy
npx wrangler secret put CLAUDE_CODE_OAUTH_TOKEN   # paste the sk-ant-oat01... token
```

## Test

```bash
# Local: run the scheduled handler on demand
wrangler dev --test-scheduled
# then, in another terminal:
curl "http://localhost:8787/__scheduled?cron=30+0,5,10,15+*+*+*"
```

Or open the deployed `*.workers.dev` URL in a browser — the `fetch` handler sends
one "hi" immediately and prints Claude's reply. Watch live logs with
`wrangler tail`; see fired schedules in the dashboard under **Workers → your
Worker → Cron Events**.

## Schedule

Cron Triggers are **UTC only**. The default `30 0,5,10,15 * * *` maps to the same
IST send-times as the GitHub workflow (IST has no DST):

| IST   | UTC   |
| ----- | ----- |
| 06:00 | 00:30 |
| 11:00 | 05:30 |
| 16:00 | 10:30 |
| 21:00 | 15:30 |

Edit `crons` in `wrangler.toml` to change it.

## Notes

- The OAuth token does not auto-refresh; if it expires, re-run
  `wrangler secret put CLAUDE_CODE_OAUTH_TOKEN`.
- Free plan covers this easily (Cron Triggers included; 4 sends/day).
- During cutover you can leave the GitHub workflow running as a backstop, then
  disable it once the Worker's Cron Events confirm it's firing.
