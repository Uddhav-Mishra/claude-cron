"""Send a 'hi' message to Claude Code (subscription auth). Run on a schedule via Render Cron Job.

Shells out to the `claude` CLI in non-interactive print mode. Authentication comes
from the CLAUDE_CODE_OAUTH_TOKEN env var (generate locally with `claude setup-token`).
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))


def main() -> int:
    if not os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        print("ERROR: CLAUDE_CODE_OAUTH_TOKEN is not set.", file=sys.stderr)
        return 1

    now_ist = datetime.now(IST)
    print(f"[{now_ist:%Y-%m-%d %H:%M:%S} IST] Sending 'hi' to Claude Code...")

    result = subprocess.run(
        ["claude", "-p", "hi", "--output-format", "json"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"claude exited with code {result.returncode}", file=sys.stderr)
        print(result.stderr.strip(), file=sys.stderr)
        return result.returncode

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Could not parse claude output:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return 1

    if payload.get("is_error"):
        print(f"Claude returned an error: {payload.get('result')}", file=sys.stderr)
        return 1

    print(f"Claude replied: {payload.get('result')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
