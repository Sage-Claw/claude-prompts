# Cowork System Prompt Changelog

---

## 2026-03-19 — v0.2.2 — Initial capture

**Commit:** `b1e1405`
**Prompt hash:** `13143ab16902caca`
**Model:** `claude-sonnet-4-6`
**Cowork plugin version:** `0.2.2`

### Summary

First capture of the Cowork system prompt. The prompt is a template (~480 lines of XML) with runtime placeholders (`{{accountName}}`, `{{cwd}}`, `{{workspaceFolder}}`, `{{skillsDir}}`, `{{currentDateTime}}`, `{{modelName}}`, `{{folderSelected}}`). It is structurally identical across all four observed sessions.

### Structure

The prompt is organized into four top-level XML sections:

- **`<application_details>`** — Identity framing: Cowork is built on Claude Code + Agent SDK but Claude must not disclose this. Runs in a lightweight Linux VM sandbox.

- **`<claude_behavior>`** — Core behavioral rules with sub-sections: `<product_information>`, `<refusal_handling>`, `<legal_and_financial_advice>`, `<tone_and_formatting>` (notably anti-bullet-point), `<user_wellbeing>`, `<anthropic_reminders>`, `<evenhandedness>`, `<responding_to_mistakes_and_criticism>`, `<knowledge_cutoff>` (stated as end of May 2025).

- **`<ask_user_question_tool>`** — Instructs Claude to always use the `AskUserQuestion` tool before starting any multi-step work. Extensive list of "underspecified request" examples.

- **`<todo_list_tool>`** — Instructs Claude to use `TodoWrite` for virtually all tool-using tasks, with a `<verification_step>` requirement.

- **`<computer_use>`** — The largest section, covering: skills system (read SKILL.md files before creating docs), file creation triggers, web content restrictions (no curl/wget bypass), Linux VM details (Ubuntu 22), MCP registry search behavior, file handling rules (workspace vs temp cwd), uploaded file handling, output production strategy, file sharing format, artifact rendering rules (supported: .md, .html, .jsx, .mermaid, .svg, .pdf), package management (`pip --break-system-packages`).

---
