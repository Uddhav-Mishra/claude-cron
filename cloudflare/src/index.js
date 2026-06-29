// Sends a single "hi" to Claude via the Messages API.
//
// Auth uses the CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`) as a Bearer
// token — the same subscription-billed path the Claude Code CLI uses, so it
// consumes subscription usage rather than pay-per-token API credits. The OAuth
// token is scoped to Claude Code, so the request must present as Claude Code
// (the oauth beta header + the Claude Code system prompt) or the API returns 429.

const API_URL = "https://api.anthropic.com/v1/messages";
const MODEL = "claude-opus-4-8";
const SYSTEM_PROMPT = "You are Claude Code, Anthropic's official CLI for Claude.";

async function sendHi(env) {
  const token = env.CLAUDE_CODE_OAUTH_TOKEN;
  if (!token) throw new Error("CLAUDE_CODE_OAUTH_TOKEN is not set");

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "anthropic-version": "2023-06-01",
      "anthropic-beta": "oauth-2025-04-20",
      "content-type": "application/json",
      "user-agent": "claude-cli/2.1.195 (external, cli)",
      "x-app": "cli",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 64,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: "hi" }],
    }),
  });

  const text = await res.text();
  if (!res.ok) throw new Error(`HTTP ${res.status} from Messages API: ${text}`);

  const data = JSON.parse(text);
  const reply = (data.content || []).find((b) => b.type === "text")?.text ?? "";
  console.log("Claude replied:", reply);
  return reply;
}

export default {
  // Fires on the cron schedule in wrangler.toml.
  async scheduled(event, env, ctx) {
    ctx.waitUntil(sendHi(env));
  },

  // Optional: open the Worker's URL to trigger a manual test send.
  async fetch(request, env) {
    try {
      const reply = await sendHi(env);
      return new Response(`Claude replied: ${reply}\n`);
    } catch (err) {
      return new Response(`Error: ${err.message}\n`, { status: 500 });
    }
  },
};
