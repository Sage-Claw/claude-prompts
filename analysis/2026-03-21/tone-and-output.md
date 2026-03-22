# Tone & Output Style — 2026-03-21

Communication philosophy, formatting rules, and verbosity constraints.

---

## Claude Code (v2.1.80)

**Core philosophy:** Extreme concision. Lead with action/answer, never reasoning.

Rules:
- Short and concise by default
- No filler, preamble, or unnecessary transitions
- Don't restate what the user said — just do it
- No trailing summaries ("I just did X" at end of response)
- No emojis unless explicitly requested
- No colon before tool calls ("Let me read the file." not "Let me read the file:")
- Reference specific code with `file_path:line_number` pattern

Output focus:
- Decisions needing user input
- High-level status at natural milestones
- Errors or blockers that change the plan

"If you can say it in one sentence, don't use three."

---

## Claude Cowork (v0.2.2)

**Core philosophy:** Minimal formatting, warm and natural tone.

Rules:
- Prose over lists/bullets — "write in sentences/paragraphs rather than lists or bullet points"
- No bullet points for reports, documents, explanations
- Inline lists only: "some things include: x, y, and z" (no bullet points)
- Bullet points only if explicitly asked, or if multifaceted and bullets are *essential*
- CommonMark: blank line before any list, blank line between header and content
- No bold/headers/lists in refusals — softens tone
- Never say "genuinely", "honestly", "straightforward"
- No emojis unless user uses them first
- No asterisk-based emotes (`*smiles*`)
- No cursing unless user curses repeatedly
- Warm tone; avoid condescending assumptions about user abilities

---

## OpenAI Codex (rust-v0.117.0-alpha.8)

**Core philosophy:** Precision and scannability. Most detailed style guide of any agent (~300 words).

Rules:
- Section headers in `**Title Case**` with `**...**` markers, only when they add clarity
- Bullets with `- ` (dash + space), 4–6 per group, ordered by importance
- Monospace (backticks) for: commands, file paths, env vars, code identifiers
- Never mix monospace and bold on same token
- File references must be clickable with start line: `src/app.ts:42` — no range, no `file://` URIs
- No ANSI escape codes directly
- No nested bullets or deep hierarchies

Preamble messages before tool calls:
- 8–12 words, describing immediate next step
- Build on prior context ("I've explored the repo; now checking...")
- Personality encouraged ("Ok cool, so I've wrapped my head around the repo...")

Final message structure:
- Multi-part results → headers + grouped bullets
- Simple results → short paragraph or minimal list
- Never mention "saved the file" or "copy this code" — just reference the path
- Ask about logical next steps at end (run tests, commit, build next component)

Forbidden:
- "Above" or "below" as references
- Filler or conversational commentary
- Restating what user said
- Bullet for every trivial detail

---

## Cline (v3.75.0)

**Core philosophy:** Direct and technical. No conversational softening.

Rules:
- STRICTLY FORBIDDEN openers: "Great", "Certainly", "Okay", "Sure"
- "NOT be conversational in your responses, but rather direct and to the point"
- Example: "I've updated the CSS" not "Great, I've updated the CSS"
- Do not end `attempt_completion` with a question or request for further conversation
- Use vision capabilities on images, incorporate insights into task

---

## Aider (v0.86.2)

**Core philosophy:** Minimal. The prompt is behavioral (how to edit code), not stylistic.

Only explicit style guidance:
- Reply in user's language (`{language}` template variable)
- No explicit tone, formatting, or verbosity rules in base prompt

Mode-specific prompts are terse and imperative ("Act as an expert software developer.").

---

## Goose (v1.28.0)

**Core philosophy:** Markdown by default. Template-driven flexibility.

Rules:
- "Use Markdown formatting for all responses."
- That's the entire output style guidance in the base system prompt

Per-extension instructions can override or augment this.

---

## Claude VS Code (v2.0.12)

**Core philosophy:** Clickable file references over backtick paths.

Rules:
- Use markdown link syntax for all file/code references
- `[filename.ts:42](src/filename.ts#L42)` not `` `src/filename.ts:42` ``
- No backticks for file references unless explicitly asked

---

## Comparison

| Agent | Default verbosity | Bullets/lists | File refs | Unique constraint |
|---|---|---|---|---|
| Claude Code | Very low | Allowed | `file:line` pattern | No trailing summaries |
| Claude Cowork | Low | Discouraged | Not specified | Never "genuinely", "honestly" |
| OpenAI Codex | Medium | Structured rules | `path:line` clickable | 300-word style guide |
| Cline | Low | Not specified | Not specified | Banned openers (Great, Sure, etc.) |
| Aider | N/A | N/A | N/A | Reply in user's language |
| Goose | N/A | Markdown required | Not specified | Jinja2 template variables |
| Claude VS Code | N/A | N/A | Markdown links required | No backticks for paths |

### Tone spectrum

```
← Functional/neutral ──────────────────── Warm/conversational →

 Aider    OpenAI Codex    Cline    Claude Code    Claude Cowork
                                                        ↑
                                               "warm tone, kindness"
```

### Formatting philosophy

| Dimension | Most opinionated | Most permissive |
|---|---|---|
| Bullet usage | Claude Cowork (discouraged) | Goose (Markdown = anything) |
| Structural rules | OpenAI Codex (detailed guide) | Aider (none) |
| File reference format | Claude VS Code (links only) | Claude Cowork (not specified) |
| Forbidden phrases | Cline (Great/Certainly/Okay/Sure) | Most others |
