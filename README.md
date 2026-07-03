# Claude "Hi" Cron (Cloudflare Worker)

A tiny [Cloudflare Worker](https://workers.cloudflare.com/) that says **"hi"** to
Claude on a daily schedule, using your Claude **subscription** (Pro/Max) — not
pay-per-token API credits.

It runs entirely on Cloudflare's **free** plan. Nothing needs to stay running on
your machine, and Cloudflare's Cron Triggers fire reliably and on time.

Default schedule: **6 AM, 11 AM, 4 PM & 9 PM IST** (easy to change — see below).

> ⚠️ **Use at your own risk.** This sends automated requests that present as the
> Claude Code CLI in order to draw on your **subscription** quota. That may
> conflict with Anthropic's Terms of Service, and the automated, fingerprintable
> traffic could get your Claude account rate-limited or suspended. You are
> responsible for how you use it. See [Account safety](#account-safety--terms-of-service).

## What you need first

- A **Claude Pro or Max** subscription (this is what gets billed).
- [**Claude Code**](https://docs.claude.com/en/docs/claude-code) installed and
  logged in — used once to mint a token.
- [**Node.js**](https://nodejs.org) installed (for `npm` / `npx`).

## Setup — step by step

### 1. Fork this repo
Click **Fork** at the top-right of this page to create your own copy.

### 2. Clone your fork
```bash
git clone https://github.com/YOUR-USERNAME/claude-cron.git
cd claude-cron
```

### 3. Install dependencies
```bash
npm install
```
This installs [Wrangler](https://developers.cloudflare.com/workers/wrangler/),
Cloudflare's CLI (version pinned in `package.json`).

### 4. Generate your Claude token
```bash
claude setup-token
```
Copy the printed `sk-ant-oat...` value. (Requires a Pro/Max subscription.)

### 5. Create a free Cloudflare account
Go to **[dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up)**, sign
up, and verify your email. No credit card required — the free plan covers this.

### 6. Log in to Cloudflare
```bash
npx wrangler login
```
This opens your browser — click **Allow** to authorize Wrangler.

### 7. Deploy the Worker
```bash
npx wrangler deploy
```

### 8. Add your token as a secret
```bash
npx wrangler secret put CLAUDE_CODE_OAUTH_TOKEN
```
Paste the `sk-ant-oat...` token from step 4 when prompted. It's stored encrypted
on Cloudflare — never in your repo.

**That's it.** The Worker now runs on the schedule automatically.

## Verify it works

Run the scheduled handler locally on demand:
```bash
npx wrangler dev --test-scheduled
# then, in another terminal:
curl "http://localhost:8787/__scheduled?cron=30+0,5,10,15+*+*+*"
```
Look for `Claude replied: Hi! How can I help you today?` in the logs.

To confirm a real run, watch live logs after a scheduled fire:
```bash
npx wrangler tail
```
Or check the Cloudflare dashboard under **Workers → claude-hi → Cron Events**.

## Change the schedule

Cron Triggers are **UTC only**. Edit `crons` in `wrangler.toml`, then redeploy
(`npx wrangler deploy`). The default `30 0,5,10,15 * * *` maps to:

| IST   | UTC   |
| ----- | ----- |
| 06:00 | 00:30 |
| 11:00 | 05:30 |
| 16:00 | 10:30 |
| 21:00 | 15:30 |

Convert your local times to UTC and set the cron fields accordingly. Cron format
is `minute hour day-of-month month day-of-week`. For example, 9 AM & 6 PM US
Eastern (UTC−5, no DST handling) → `0 14,23 * * *`.

## Notes

- Billed against your Claude **subscription** limits, not API credits.
- The OAuth token does **not** auto-refresh. If it expires, mint a new one
  (`claude setup-token`) and re-run `npx wrangler secret put CLAUDE_CODE_OAUTH_TOKEN`.
- This is a **cron-only** Worker — it has no public HTTP endpoint, so nobody can
  trigger it anonymously to spend your quota.
- The free Cloudflare plan covers this easily (4 sends/day).

## Account safety / Terms of Service

Read this before deploying:

- The Worker authenticates with your **subscription** OAuth token and presents
  as the Claude Code CLI (spoofed user-agent, the `oauth-2025-04-20` beta header,
  and the Claude Code system prompt) so the request bills against your
  subscription rather than API credits. This is **not** an officially supported
  use of the token.
- Doing this on an automated schedule may violate Anthropic's Terms of Service.
- The traffic is easy to fingerprint (a fixed daily cadence and an identical
  `"hi"` prompt), so Anthropic could rate-limit or **suspend your account**.
- You use this entirely at your own risk. Point it at your own account only, and
  keep the send frequency modest.

## How it works

The Worker's `scheduled` handler (`src/index.js`) fires on the cron schedule and
sends a single `POST` to the Anthropic Messages API
(`https://api.anthropic.com/v1/messages`). It authenticates with your
`CLAUDE_CODE_OAUTH_TOKEN` as a Bearer token and presents as Claude Code (the
`oauth-2025-04-20` beta header + Claude Code system prompt), so the request draws
from your subscription instead of API billing.

## License

[MIT](LICENSE)
