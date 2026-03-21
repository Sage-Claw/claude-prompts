# Cowork System Prompt Changelog

---

## 2026-03-21 — v0.2.2 (model: claude-sonnet-4-6) — app update only

**Commit:** `dcd2aa4`
**Changes:** metadata only (app version bump)
**Prompt hash:** `13143ab16902caca` (unchanged)

### Summary
No prompt content changes. The Claude for Mac app updated from `1.1.7464 (2809b60)` to `1.1.7714 (3bd6f69)`. The metadata headers in `slash-commands.md`, `mcp-tools.md`, and `egress-domains.md` were updated to reflect the new app version.

### Key changes
- App version: `1.1.7464 (2809b60)` → `1.1.7714 (3bd6f69)`
- System prompt, slash commands, MCP tools, egress domains: **no content changes**

---

## 2026-03-21 — v0.2.2 / 2026-03-21 re-capture

**Commit:** `e7b7c5b`
**Prompt hash:** `13143ab16902caca` (unchanged from 2026-03-15 capture)
**Cowork plugin version:** `0.2.2`
**Claude for Mac:** `1.1.7464 (2809b60)`

### Summary

Re-captured from a fresh session to establish clean version history. Prompt content identical to the 2026-03-15 capture. The `cowork/versions/` directory was created with snapshots for both historical dates.

---

## 2026-03-15 — v0.2.2 / Claude for Mac 1.1.7464

**Commit:** `6f8b26f` (was: `b1e1405`)
**Prompt hash:** `13143ab16902caca` (was: `bd536a03d4204e08`)
**Cowork plugin version:** `0.2.2`
**Claude for Mac:** `1.1.7464 (2809b6)` (released 2026-03-18)
**Slash commands:** 30 (was: 13)
**MCP tools:** 4 (was: 0)
**Egress domains added:** `registry.npmjs.org`, `npmjs.com`, `www.npmjs.com`

### Summary

Model references updated from Claude 4.5 to 4.6 (Opus, Sonnet). The `<suggesting_claude_actions>` section was rewritten to be more proactive — from "offer to help if you can" to "queries often require tools, just use them." MCP registry search examples expanded significantly. lucide-react bumped from 0.263.1 to 0.383.0. Slash command set more than doubled (13 → 30) and 4 MCP tools became active.

### Key changes

- **Model update**: `claude-opus-4-5-20251101` / `claude-sonnet-4-5-20250929` → `claude-opus-4-6` / `claude-sonnet-4-6`; "developer platform" renamed to "Claude Platform"
- **`<suggesting_claude_actions>` rewrite**: Removed the "offer to do it" framing. New behavior: treat queries as tool-use opportunities by default; call `search_mcp_registry` proactively even when the query sounds like a web task
- **New MCP registry examples**: Sprint/project management, team messaging (Slack/Teams), oncall rotation (PagerDuty) — all route through `search_mcp_registry` → `suggest_connectors` before falling back to browser
- **New analytics example**: "How many signups did we get yesterday?" now routes to `search_mcp_registry` for analytics/database connectors
- **`lucide-react` bump**: `0.263.1` → `0.383.0`
- **Slash commands**: Grew from 13 to 30 (new skills/tools added to Cowork)
- **MCP tools**: 0 → 4 active (`enabledMcpTools` newly populated)
- **Egress domains**: None → `registry.npmjs.org`, `npmjs.com`, `www.npmjs.com` added

---

## 2026-02-22 — v0.2.2 — Initial capture

**Prompt hash:** `bd536a03d4204e08`
**Cowork plugin version:** `0.2.2`
**Claude for Mac:** unknown (pre-4.6 model update, ~Feb 2026)
**Slash commands:** 13
**MCP tools:** 0
**Egress domains:** none

### Summary

Earliest captured Cowork system prompt. Observed across two sessions on 2026-02-22 and 2026-02-23. Uses Claude 4.5 model strings. The `<suggesting_claude_actions>` section is cautious — Claude is instructed to "consider whether it can help" and offer to do so, rather than proceeding proactively. MCP registry search is triggered only when asked about external apps without matching tools, and only after evaluation.

### Structure

The prompt is a ~480-line XML template with four top-level sections:

- **`<application_details>`** — Identity framing: Cowork is built on Claude Code + Agent SDK but Claude must not disclose this. Runs in a lightweight Linux VM sandbox.
- **`<claude_behavior>`** — Core behavioral rules: `<product_information>`, `<refusal_handling>`, `<legal_and_financial_advice>`, `<tone_and_formatting>` (anti-bullet-point), `<user_wellbeing>`, `<anthropic_reminders>`, `<evenhandedness>`, `<responding_to_mistakes_and_criticism>`, `<knowledge_cutoff>` (stated as end of May 2025).
- **`<ask_user_question_tool>`** — Always use `AskUserQuestion` before any multi-step work.
- **`<computer_use>`** — Skills system, file creation triggers, web restrictions, Linux VM details (Ubuntu 22), MCP registry behavior, workspace vs temp dir rules, artifact rendering (`.md`, `.html`, `.jsx`, `.mermaid`, `.svg`, `.pdf`).

---
