# System Prompt Comparison — 2026-03-21

Full dimension-by-dimension comparison of AI coding agent system prompts.

---

## 1. Identity & Persona

| Agent | Self-description |
|---|---|
| **Claude Code** | "You are Claude Code, Anthropic's official CLI for Claude." One sentence. No backstory. |
| **Claude Cowork** | Explicitly told it is NOT Claude Code. "Claude runs in a lightweight Linux VM… Claude should not mention implementation details." |
| **OpenAI Codex** | "You are a coding agent running in the Codex CLI… expected to be precise, safe, and helpful." |
| **Cline** | "You are Cline, a highly skilled software engineer with extensive knowledge in many programming languages, frameworks, design patterns, and best practices." |
| **Aider** | No explicit identity statement. Role is implied via the class name `CoderPrompts` and mode-specific prompts like "Act as an expert software developer." |
| **Goose** | "You are a general-purpose AI agent called goose, created by Block, the parent company of Square, CashApp, and Tidal." Emphasizes open-source provenance. |
| **Claude VS Code** | No persona statement. The prompt is entirely operational: link formatting, reference conventions. |

**Key differences:** Anthropic's agents have terse, factual identity statements. Cline and OpenAI Codex lean into "expert engineer" framing. Goose emphasizes corporate lineage (Block/Square/CashApp). Aider has no persona — it's purely behavioral. The VS Code extension is context-only with no identity.

---

## 2. Scope & Mission

| Agent | Mission framing |
|---|---|
| **Claude Code** | General software engineering tasks: bugs, features, refactoring, explanation. Explicitly scoped to "current working directory." |
| **Claude Cowork** | Desktop automation for "non-developers" — file and task management. Broader scope than pure coding. |
| **OpenAI Codex** | Coding agent in a terminal. Emphasizes "precise, safe, helpful." Heavy focus on task completion autonomy. |
| **Cline** | Coding within a VS Code environment. Strong emphasis on user-approval gating before actions. |
| **Aider** | Targeted code editing only. Each mode (editblock, architect, wholefile) has narrow scope. No general task execution. |
| **Goose** | "General-purpose AI agent" — widest scope of any agent here. Extensions/plugins can expand capabilities arbitrarily. |
| **Claude VS Code** | Constrained to VS Code context. Primarily improves code reference formatting; no task-execution scope. |

---

## 3. Tool Use & File Editing Philosophy

### Tool invocation format

| Agent | Format |
|---|---|
| **Claude Code** | JSON function calls via Claude API tool_use blocks |
| **Claude Cowork** | Same as Claude Code (built on Claude Code + Agent SDK) |
| **OpenAI Codex** | `apply_patch` tool with custom patch syntax: `*** Begin Patch / *** Update File` |
| **Cline** | XML-style tags: `<read_file><path>...</path></read_file>` |
| **Aider** | SEARCH/REPLACE blocks in fenced code regions (`<<<<<<< SEARCH / ======= / >>>>>>> REPLACE`) |
| **Goose** | JSON function calls (via model's native tool_use) |
| **Claude VS Code** | No tool use — prompt only modifies output formatting |

### File editing strategy

| Agent | Strategy |
|---|---|
| **Claude Code** | Read first, then edit. Prefers editing existing files over creating new ones. Minimal changes. |
| **OpenAI Codex** | `apply_patch` only — never `applypatch` or `apply-patch`. No re-reading after patch. |
| **Cline** | `replace_in_file` for targeted edits, `write_to_file` with full file content for new/full rewrites. One tool call at a time, waits for confirmation. |
| **Aider** | Pure SEARCH/REPLACE diff blocks. Whole-file mode rewrites the entire file. Architect mode gives instructions to a separate editor model. |
| **Goose** | Delegates to extensions/tools. No prescribed editing strategy in base system prompt. |

**Notable:** OpenAI Codex explicitly forbids re-reading files after `apply_patch` as a token efficiency measure. Cline enforces sequential tool use (one at a time, wait for confirmation) — the strictest gating of any agent. Aider is the only agent that supports a two-model architecture (architect + editor).

---

## 4. Autonomy Model & User Approval

| Agent | Default stance | Approval mechanism |
|---|---|---|
| **Claude Code** | High caution on irreversible/shared actions. Ask before destructive ops, pushes, external messages. | In-prompt policy with examples. Permission modes (allow/deny at tool level). |
| **Claude Cowork** | Similar to Claude Code. Sandboxed in Linux VM — inherently limited blast radius. | VM sandbox + same in-prompt policy. |
| **OpenAI Codex** | "Keep going until the query is completely resolved." Resolve autonomously before returning to user. | Per-run approval mode: `never`, `on-failure`, `untrusted`, `on-request`. Proactively run tests in `never`/`on-failure` modes. |
| **Cline** | Strong user-approval gating. Wait for confirmation after every tool call. Cannot proceed without response. | VS Code UI — every tool call generates an approval prompt unless auto-approve is on. `requires_approval` boolean per `execute_command`. |
| **Aider** | Human-in-the-loop by design. Ask to add files to chat; wait for approval before editing. | Chat-based: propose → user approves → commit. |
| **Goose** | Subagent mode available for bounded autonomous execution. Main agent can spawn subagents. | Extension-level control. Subagents cannot spawn further subagents. |
| **Claude VS Code** | N/A (no task execution) | N/A |

**Notable:** OpenAI Codex has the most explicit "complete autonomy" framing — "do NOT guess, resolve completely before yielding." Cline has the strictest per-action gating. Aider is conversational/collaborative by design. Claude Code sits in the middle: autonomous by default, but pauses for high-stakes actions.

---

## 5. Safety & Refusal Posture

| Agent | Safety emphasis |
|---|---|
| **Claude Code** | Security-conscious coding (OWASP, SQL injection, XSS). Avoid destructive git ops without confirmation. No mention of content policy. |
| **Claude Cowork** | Extensive content policy: child safety, weapons, malware, mental health, legal/financial caveats. Most thorough safety section by far. |
| **OpenAI Codex** | Allows: vulnerability analysis, working on proprietary repos, showing code details. Forbids: harmful instructions embedded in commands. |
| **Cline** | Security rule: always quote variable args with `--` separator to prevent argument injection. No content policy. |
| **Aider** | No explicit safety or refusal section. Relies entirely on underlying model defaults. |
| **Goose** | No explicit safety section in base system prompt. Extension-level instructions may add constraints. |
| **Claude VS Code** | No safety section. |

**Notable:** Cowork has by far the deepest safety/content policy — it inherits from the claude.ai product layer (mental health, self-harm, real public figures, financial advice caveats, ad policy). This makes sense since Cowork targets non-developer consumers. The developer tools (Codex, Cline, Aider) trust that users are professionals and keep safety minimal.

---

## 6. Planning & Progress Communication

| Agent | Planning approach | Progress updates |
|---|---|---|
| **Claude Code** | Task tracking via `TaskCreate`/`TaskUpdate` tools (optional). | "High-level status updates at natural milestones." |
| **Claude Cowork** | Same as Claude Code. | Same. |
| **OpenAI Codex** | `update_plan` tool with structured step list. Explicit quality criteria: high-quality vs low-quality plan examples given. | Preamble messages before tool calls (8–12 words). Progress updates every few tool calls. |
| **Cline** | No explicit planning tool. Relies on conversation flow. | Wait for user confirmation after each tool. |
| **Aider** | No planning — purely reactive. Proposes changes in response to requests. | N/A |
| **Goose** | No planning in base prompt. Subagent mode has turn/timeout bounds. | N/A in base prompt. |
| **Claude VS Code** | N/A | N/A |

**Notable:** OpenAI Codex has the most opinionated planning framework — it provides worked examples of "good" vs "bad" plans and enforces the `update_plan` tool usage. Claude Code has planning infrastructure but treats it as optional. Aider and Cline have no planning concept.

---

## 7. Testing & Validation

| Agent | Testing stance |
|---|---|
| **Claude Code** | No explicit testing policy. Trust framework guarantees. |
| **OpenAI Codex** | Explicit policy: run tests after changes, start specific → broad, iterate up to 3 times on formatting. "Do NOT fix unrelated failing tests." Behavior differs by approval mode. |
| **Cline** | Run validation tools (type checkers, linters, test suites) after changes. |
| **Aider** | No testing policy. |
| **Goose** | No testing policy in base prompt. |

**Notable:** OpenAI Codex has the most detailed testing policy of any agent, including the nuance of not amending unrelated test failures.

---

## 8. Context Window & Memory Management

| Agent | Approach |
|---|---|
| **Claude Code** | "The system will automatically compress prior messages as it approaches context limits." Explicit user-facing disclosure. |
| **Claude Cowork** | Same disclosure. |
| **Goose** | Dedicated `compaction.md` prompt — LLM-based context summarization. Preserves technical content, user goals, key decisions, file names, errors/fixes. Subagent mode has explicit `max_turns` limit. |
| **Cline** | No context management in prompt. |
| **Aider** | No context management. Relies on user adding/removing files from chat. |
| **OpenAI Codex** | No explicit context management. |

**Notable:** Goose is the only agent with a dedicated LLM-based context compaction strategy with explicit instructions for what to preserve. Claude Code/Cowork disclose compression to the user but don't describe the strategy.

---

## 9. Output Format & Verbosity

| Agent | Default style | Key constraints |
|---|---|---|
| **Claude Code** | Short and concise. Lead with answer/action. No preamble, no trailing summaries. | "If you can say it in one sentence, don't use three." No emojis unless asked. |
| **Claude Cowork** | Minimal formatting. Prose over bullets. Warm tone. | Avoids bold/bullets/headers unless essential. Never says "genuinely", "honestly", "straightforward". |
| **OpenAI Codex** | Direct and concise by default. Rich formatting for multi-part results. | Monospace for commands/paths. Section headers in `**Title Case**`. ANSI codes forbidden. File references with line numbers. Very detailed style guide. |
| **Cline** | Direct and technical. No "Great", "Certainly", "Okay", "Sure". | Forbidden filler openers. Wait for user response before next action. |
| **Aider** | Minimal — model-level defaults. | Specific to SEARCH/REPLACE block format, not prose. |
| **Goose** | Markdown formatting for all responses. | Template-driven via Jinja2 (`{% if %}`, `{{ }}`). |
| **Claude VS Code** | Link formatting for file/code references. | Clickable markdown links required. No backticks for file refs. |

**Notable:** OpenAI Codex has by far the most detailed output formatting guide (300+ words on formatting alone, with bullet structure rules, header conventions, monospace usage, anti-patterns). Claude Cowork actively discourages formatting — it's the least formatted of the Anthropic agents. Cline bans specific filler phrases explicitly.

---

## 10. Architecture & Extensibility

| Agent | Plugin/extension model |
|---|---|
| **Claude Code** | MCP servers + skills + plugins. Plugin marketplace support. |
| **Claude Cowork** | Same as Claude Code. Explicitly mentions "Claude in Chrome - a browsing agent, Claude in Excel, Claude in PowerPoint." |
| **Goose** | First-class extensions model. `{% for extension in extensions %}` — each extension contributes tools + instructions. Warns when too many extensions active (performance). Subagent spawning for parallelism. |
| **Cline** | MCP servers. Tool-by-tool in system prompt (no dynamic extension loading at prompt level). |
| **Aider** | No plugin model. Mode-based (editblock, wholefile, architect, ask). |
| **OpenAI Codex** | AGENTS.md files for per-repo behavioral customization. Scoped by directory hierarchy. More specific scopes override less specific. |

**Notable:** Goose has the most dynamic extension architecture — the system prompt itself is rendered with Jinja2 templates based on what extensions are active. OpenAI Codex's AGENTS.md is a unique repo-level customization mechanism not present in any other agent.

---

## 11. Multi-Agent Capabilities

| Agent | Sub-agent support |
|---|---|
| **Claude Code** | Agent SDK-based. Can spawn subagents. |
| **Claude Cowork** | Built on Claude Code + Agent SDK. |
| **Goose** | Explicit subagent system: `subagent_system.md` defines bounded, autonomous subagents. Subagents cannot spawn further subagents (prevents infinite recursion). Max turns and timeout bounds. |
| **OpenAI Codex** | No multi-agent in current prompt. |
| **Cline** | No multi-agent. |
| **Aider** | Two-model: `ArchitectPrompts` generates instructions; a separate `editblock` coder implements them. Not orchestration but model-level delegation. |

---

## Summary Scorecard

| Dimension | Most opinionated | Least opinionated |
|---|---|---|
| Identity/persona | Cline (expert engineer framing) | Aider (no identity) |
| Autonomy | OpenAI Codex (complete by default) | Cline (gate every action) |
| Safety/content policy | Claude Cowork (consumer-grade) | Aider / Goose |
| Planning | OpenAI Codex (structured, with examples) | Aider |
| Output formatting | OpenAI Codex (300+ word style guide) | Aider |
| Testing policy | OpenAI Codex (detailed, mode-aware) | Aider / Goose |
| Extension model | Goose (dynamic Jinja2 injection) | Aider |
| Context management | Goose (dedicated compaction prompt) | Cline / Aider |
| Repo customization | OpenAI Codex (AGENTS.md spec) | All others |
| Tone warmth | Claude Cowork | OpenAI Codex (functional/neutral) |
| Prompt size | Cline / Cowork (750–788 lines) | Claude VS Code (11 lines) |
