# Claude Code System Prompt Changelog

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
