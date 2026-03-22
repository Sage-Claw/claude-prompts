# Tool Use & File Editing Formats — 2026-03-21

How each agent invokes tools and formats file edits.

---

## Claude Code & Claude Cowork

Uses Claude API native `tool_use` blocks (JSON function calls). No custom syntax in the prompt itself — the tool definitions are injected separately at runtime.

**File editing philosophy:**
- Prefer editing existing files over creating new ones
- Read before modifying
- Minimal, focused changes — don't fix unrelated code
- No helpers/abstractions for one-time operations

---

## OpenAI Codex

Uses `apply_patch` with a custom patch format:

```
{"command":["apply_patch","*** Begin Patch\n*** Update File: path/to/file.py\n@@ def example():\n- pass\n+ return 123\n*** End Patch"]}
```

Key constraints:
- ONLY `apply_patch` — never `applypatch` or `apply-patch` (explicit warning)
- Do NOT re-read files after patching (trust the tool succeeded)
- Do NOT `git commit` unless explicitly requested
- No inline comments unless explicitly requested
- No one-letter variable names unless explicitly requested
- No copyright/license headers unless requested

---

## Cline

XML-style tags for every tool:

```xml
<read_file>
<path>src/main.js</path>
</read_file>

<replace_in_file>
<path>src/app.ts</path>
<diff>
<<<<<<< SEARCH
old content
=======
new content
>>>>>>> REPLACE
</diff>
</replace_in_file>
```

Key constraints:
- One tool call per message — always wait for user response before the next
- `replace_in_file` for targeted edits (SEARCH/REPLACE blocks must be complete lines, ordered by position in file)
- `write_to_file` for new files or full rewrites — must include COMPLETE file content
- `requires_approval: true/false` on `execute_command` for safety gating
- SEARCH blocks must match exact full lines — no partial line matches

---

## Aider

Pure text diff blocks embedded in the model response:

```
filename.py
```python
<<<<<<< SEARCH
old code
=======
new code
>>>>>>> REPLACE
```

Modes:
- **editblock** — SEARCH/REPLACE diffs, most common mode
- **wholefile** — rewrites entire file content
- **architect** — generates natural language instructions for a separate editor model
- **ask** — no file editing, conversation only

Key constraints:
- Model must request user to add files to chat before editing them
- Cannot edit files not already in the chat
- Always reply to user in their language (`{language}` template)

---

## Goose

Uses model-native JSON tool calls (same as Claude API function calling pattern). Tool set is dynamic — determined by which extensions are active:

```jinja
You have access to {{tool_count}} tools: {{available_tools}}
```

No prescribed file editing strategy in the base system prompt — each extension defines its own tools and behavior.

---

## Claude VS Code

No tool use. The prompt only modifies how the model formats file references in its text output:

```markdown
- For files: [filename.ts](src/filename.ts)
- For specific lines: [filename.ts:42](src/filename.ts#L42)
- For a range of lines: [filename.ts:42-51](src/filename.ts#L42-L51)
```

No backticks for file references (use clickable links instead).

---

## Comparison Summary

| Agent | Format | Atomic? | Approval gating |
|---|---|---|---|
| Claude Code | JSON tool_use | No (parallel allowed) | High-stakes only |
| Claude Cowork | JSON tool_use | No (parallel allowed) | High-stakes only |
| OpenAI Codex | `apply_patch` custom format | No | Mode-dependent |
| Cline | XML tags | Yes (one at a time) | Every command |
| Aider | SEARCH/REPLACE text blocks | Yes (per-file) | User adds files to chat |
| Goose | JSON tool_use (dynamic) | No | Extension-dependent |
| Claude VS Code | N/A (text formatting only) | N/A | N/A |
