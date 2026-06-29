# Claude "Hi" Cron Job

[![claude-hi](https://github.com/Uddhav-Mishra/claude-cron/actions/workflows/claude-hi.yml/badge.svg)](https://github.com/Uddhav-Mishra/claude-cron/actions/workflows/claude-hi.yml)

A free GitHub Actions workflow that says **"hi"** to Claude Code on a daily
schedule, using your Claude **subscription** (Pro/Max), not API credits.

It calls the Messages API directly (via `send_hi.py`, Python standard library
only — no CLI, no Node) on GitHub's servers, so nothing needs to stay running on
your machine. Default schedule: **6 AM, 11 AM, 4 PM & 9 PM IST**.

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

## Alternative: deploy on Cloudflare Workers

GitHub's scheduled cron is best-effort and often drops runs. For reliable,
on-time triggering, there's a Cloudflare Worker version in [`cloudflare/`](cloudflare/)
that calls the same subscription-billed API path — see
[`cloudflare/README.md`](cloudflare/README.md) for the deploy steps.

The two are independent and can run in parallel: keep the GitHub workflow as a
backstop while the Cloudflare Worker handles reliable scheduling (you'll just get
a duplicate "hi" when both fire at the same slot). Disable whichever you don't
want — the GitHub workflow via the repo's **Actions** tab, the Worker via
`npx wrangler delete`.

## Set your own times & timezone (no YAML editing)

GitHub Actions cron is UTC-only and can't read variables, so this workflow runs
**hourly** and a gate step decides whether the current hour matches *your* local
time. Configure it with repo **Variables** (not secrets):

**repo → Settings → Secrets and variables → Actions → Variables → New variable**

| Variable    | Example        | Meaning                                      |
|-------------|----------------|----------------------------------------------|
| `TZ`        | `Asia/Kolkata` | Any IANA timezone (DST handled automatically)|
| `RUN_HOURS` | `6,11,16,21`   | Local hours to run, comma-separated (0–23)   |

Defaults (if you set nothing): `TZ=Asia/Kolkata`, `RUN_HOURS=6,11,16,21` → 6 AM, 11 AM, 4 PM & 9 PM IST.
Examples: New York at 9am & 6pm → `TZ=America/New_York`, `RUN_HOURS=9,18`.

<details>
<summary>Common <code>TZ</code> values</summary>

**Americas**
| Region            | `TZ`                  |
|-------------------|-----------------------|
| US Eastern        | `America/New_York`    |
| US Central        | `America/Chicago`     |
| US Mountain       | `America/Denver`      |
| US Pacific        | `America/Los_Angeles` |
| Toronto           | `America/Toronto`     |
| Mexico City       | `America/Mexico_City` |
| São Paulo         | `America/Sao_Paulo`   |

**Europe / Africa**
| Region            | `TZ`                  |
|-------------------|-----------------------|
| UK                | `Europe/London`       |
| Central Europe    | `Europe/Paris` / `Europe/Berlin` |
| Madrid            | `Europe/Madrid`       |
| Moscow            | `Europe/Moscow`       |
| Johannesburg      | `Africa/Johannesburg` |

**Asia / Pacific**
| Region            | `TZ`                  |
|-------------------|-----------------------|
| India             | `Asia/Kolkata`        |
| UAE               | `Asia/Dubai`          |
| Singapore         | `Asia/Singapore`      |
| Japan             | `Asia/Tokyo`          |
| China             | `Asia/Shanghai`       |
| Sydney            | `Australia/Sydney`    |
| Auckland          | `Pacific/Auckland`    |

Full list: [IANA tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
</details>

The gate matches on the **hour**, so the run lands at the minute set by the cron
line (`30 * * * *`): `local_minute = (cron_minute + your_tz_offset) mod 60`.
IST is +5:30, so minute 30 → **:00 IST** (on the hour). If your timezone is a
whole-hour offset and you want on-the-hour runs, change the cron minute to `0`.

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

## License

[MIT](LICENSE)
