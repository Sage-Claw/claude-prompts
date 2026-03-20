# Claude Prompts

Documentation of system prompts used by Claude products.

## Contents

- [`cowork/`](./cowork/) — Claude Cowork (desktop app agentic mode)
- [`claude-code/`](./claude-code/) — Claude Code (CLI)

## How these were obtained

**Cowork:** Session config files are stored locally at:
- macOS: `~/Library/Application Support/Claude/local-agent-mode-sessions/{uuid}/{uuid}/local_{uuid}.json`
- Windows: `~\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\{uuid}\{uuid}\local_{uuid}.json`

Each session JSON contains the full system prompt (roughly 80% of the file). The prompt is a template — placeholders like `{{accountName}}`, `{{cwd}}`, `{{workspaceFolder}}`, `{{currentDateTime}}` are substituted at runtime per session.

**Claude Code:** System prompt is injected at runtime and can be captured from the `CLAUDE_SYSTEM_PROMPT` env var or via debug logging.
