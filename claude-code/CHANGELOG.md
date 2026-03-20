# Claude Code System Prompt Changelog

---

## 2026-03-19 — v1.0.0 — Historical backfill

**Published:** `2025-05-22T16:57:18.061Z`
**Git head:** `7313027bbf`
**Format:** JavaScript bundle (`cli.js`) — not a binary SEA
**Prompt hash:** `36f812d8a82673b7`

### Summary

Retroactive capture of the Claude Code 1.0.0 prompt. This was the initial GA release on npm. Unlike later versions (2.x+) which ship as Node.js SEA binaries, 1.0.0 is a plain JavaScript bundle. The system prompt lives in two named functions: `j70` (identity) and `WS` (main instructions), plus `y70` (environment template).

### Sections captured

- **Identity** — "You are {{...}}, Anthropic's official CLI for Claude."
- **System Prompt** — Monolithic instructions block covering: security refusals, tone/conciseness, proactiveness, code conventions, task workflow, tool usage policy
- **Environment (template)** — Runtime env block with working dir, git status, platform, date, model

### Notable content in v1.0.0

- Explicit security refusals for malicious code baked into the main prompt (later moved to model training)
- Hard limit: "answer concisely with fewer than 4 lines" — very strict verbosity cap
- `# Code style` section: "DO NOT ADD ***ANY*** COMMENTS unless asked"
- No separate "Executing Actions with Care" or "Output Efficiency" sections — these were added later
- Tool usage policy: batch parallel tool calls in a single message

---

## 2026-03-19 — v2.1.80 — Initial capture

**Commit:** `7442ee9`
**Build time:** `2026-03-19T21:00:45Z`
**Prompt hash:** `e862465fb00399ac`
**Settings hash:** `07f6e4397224a016`
**Plugins hash:** `c85fbdfca9691bf3`

### Summary

First capture of the Claude Code system prompt. Extracted from the Node.js SEA binary (`~/.local/share/claude/versions/2.1.80`). The prompt is constructed at runtime from static sections embedded in the binary; dynamic sections (env info, CLAUDE.md content, MCP server instructions) are injected per-session and not captured here.

### Static sections captured

- **Identity & Behavior** — Intro framing, URL policy, interactive behavior description
- **System** — Tool use rules, tag handling, prompt injection warnings, context compression notice
- **Coding Instructions** — Over-engineering avoidance, task approach, safety/git protocol, PR workflow
- **Executing Actions with Care** — Reversibility guidelines, risky action examples, destructive op warnings
- **Tone and Style** — Emoji policy, conciseness, code reference format
- **Output Efficiency** — Brevity rules, lead with action, response focus guidance
- **Environment (template)** — Template for env block with runtime placeholders (`{{...}}`)

### Settings (v2.1.80)

- Model: `opusplan`
- Plugins enabled: `claude-md-management`, `frontend-design`, `skill-creator`
- Hooks: SessionStart, UserPromptSubmit, Stop, Notification, PermissionRequest

### Installed plugins

3 plugins from `claude-plugins-official`: `claude-md-management`, `frontend-design`, `skill-creator`

---
