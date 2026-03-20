# Cowork System Prompt

Claude Cowork is a desktop app feature (currently research preview) that runs an agentic Claude session in a lightweight Linux VM sandbox on the user's computer.

## Key facts

- Built on Claude Code + Claude Agent SDK (but Claude is instructed not to disclose this)
- Runs Ubuntu 22 VM locally; workspace folder persists, working dir resets between tasks
- Observed models: `claude-sonnet-4-6`, `claude-opus-4-6`
- Knowledge cutoff stated in prompt: **end of May 2025**

## Template variables

The prompt is a template. These placeholders are substituted at session start:

| Variable | Description |
|---|---|
| `{{accountName}}` | User's account name |
| `{{emailAddress}}` | User's email |
| `{{cwd}}` | VM working directory (temporary, resets) |
| `{{workspaceFolder}}` | Persistent workspace folder on host |
| `{{skillsDir}}` | Path to skills directory |
| `{{workspaceContext}}` | Context about whether user selected a folder |
| `{{currentDateTime}}` | Current date/time |
| `{{modelName}}` | Model being used |
| `{{folderSelected}}` | Boolean — whether user mounted a folder |

## Files

- [`system-prompt.md`](./system-prompt.md) — Full system prompt (as-captured, with template vars intact)
