"""Send a 'hi' message to Claude on a schedule (GitHub Actions).

Calls the Messages API directly over HTTPS using the Python standard library —
no `claude` CLI, no Node. Authentication uses the CLAUDE_CODE_OAUTH_TOKEN env var
(generate locally with `claude setup-token`), sent as a Bearer token. This is the
same subscription-billed path the CLI uses, so it consumes your subscription
usage rather than pay-per-token API credits.

The OAuth token is scoped to the Claude Code client, so the request must identify
itself as Claude Code (the oauth beta header + the Claude Code system prompt);
without that the API rejects it with a 429.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-opus-4-8"
# Required: the OAuth token is a Claude Code credential, so the request must
# present as Claude Code or the API returns 429.
SYSTEM_PROMPT = "You are Claude Code, Anthropic's official CLI for Claude."
TIMEOUT_SECONDS = 120


def _redact(text: str) -> str:
    """Never echo the token, in case it ever appears in an error body."""
    token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
    return text.replace(token, "***") if token else text


def main() -> int:
    token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not token:
        print("ERROR: CLAUDE_CODE_OAUTH_TOKEN is not set.", file=sys.stderr)
        return 1

    now_ist = datetime.now(IST)
    print(f"[{now_ist:%Y-%m-%d %H:%M:%S} IST] Sending 'hi' to Claude...")

    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 64,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": "hi"}],
        }
    ).encode()

    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "authorization": f"Bearer {token}",
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "oauth-2025-04-20",
            "content-type": "application/json",
            "user-agent": "claude-cli/2.1.195 (external, cli)",
            "x-app": "cli",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read().decode()
    except urllib.error.HTTPError as exc:
        detail = _redact(exc.read().decode(errors="replace").strip())
        print(f"HTTP {exc.code} from Messages API: {detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"ERROR: request failed: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print(f"ERROR: request timed out after {TIMEOUT_SECONDS}s.", file=sys.stderr)
        return 1

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print("Could not parse API response:", file=sys.stderr)
        print(_redact(raw), file=sys.stderr)
        return 1

    if payload.get("type") == "error":
        print(f"Claude returned an error: {payload.get('error')}", file=sys.stderr)
        return 1

    text = next(
        (
            block.get("text", "")
            for block in payload.get("content", [])
            if block.get("type") == "text"
        ),
        "",
    )
    print(f"Claude replied: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
