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
npm install -g wrangler          # or prefix each command with `npx`
wrangler login                   # links your Cloudflare account
wrangler secret put CLAUDE_CODE_OAUTH_TOKEN   # paste the sk-ant-oat01... token
wrangler deploy
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
