# Claude Code System Prompt Changelog

---

## v2.1.91 — 2026-04-14

**Prompt hash:** `e3b0c44298fc1c14` (was: `1258ff383e073bc9`)
**Build time:** `unknown`
**Commit:** `ad847f1`

### Summary
Extraction captured an effectively empty prompt payload for Claude Code v2.1.91, and plugin snapshot dropped to zero entries. This appears to be an extractor regression tied to bundle/layout changes, not a likely intentional prompt wipe.

### Key changes
- **System prompt capture:** `claude-code/system-prompt.md` collapsed from full multi-section content to header metadata only.
- **Plugins snapshot:** `claude-code/plugins.md` changed from 3 plugins to 0 plugins.
- **Extractor health signal:** Prompt hash became SHA-256 empty-content prefix (`e3b0...`), indicating parse failure or no extracted body.

---

## v2.1.86 — 2026-03-27

**Prompt hash:** `1258ff383e073bc9` (was: `852c4b5d81f2a66f`)
**Build time:** `2026-03-27T20:29:28Z`
**Commit:** `bbf4607` (content) + re-extracted after function name fix

### Summary
Major bundle rebuild — all section function names changed (`qrK/KrK/…` → `qJ/UYK/QYK/lYK/aYK/oYK/tYK`). Several real prompt changes alongside the structural churn. The identity section (`qJ`) is now the main system prompt assembly function and captures runtime context blocks (MCP instructions, env, model info) that were previously dynamic-only.

### Key changes
- **System:** Added `! <command>` shorthand tip — suggest `! gcloud auth login` style for interactive shell commands the user needs to run themselves.
- **Coding Instructions:** Refined the "don't brute-force" instruction → "If an approach fails, diagnose why before switching tactics — read the error, check your assumptions, try a focused fix. Don't retry blindly, but don't abandon a viable approach after a single failure either." Also tightened the complexity rule: "what the task actually requires — no speculative abstractions, but no half-finished implementations either."
- **Executing Actions with Care:** Added explicit tool-preference rules: use `Read` instead of cat/head/tail/sed, `Edit` instead of sed/awk, `Write` instead of echo-heredoc, `Glob` instead of find, `Grep` instead of grep/rg. Reserve `Bash` for system commands only.
- **Tone and Style:** Added GitHub issue/PR link format instruction — use `owner/repo#123` (e.g. `anthropics/claude-code#100`) so references render as clickable links.
- **Identity (new content):** Added `# Scratchpad Directory` — instructs Claude to use a session-specific scratchpad path for all temp files instead of `/tmp`. Added agent-mode instructions (absolute paths, concise final report). Added Claude 4.5/4.6 model family reference with current model IDs.

---

## v2.1.78–v2.1.80 — 2026-03-17

**Prompt hash:** `852c4b5d81f2a66f`
**Diff size:** ~2560 chars

### Key changes
- Added warning that uploading content to third-party web tools (diagram renderers, pastebins, gists) publishes it and may be cached or indexed even if later deleted.
- Removed the generic output-polish instruction ("Your output to the user should be concise and polished…") in favor of the "Tone and style" section header.

---

## v2.1.75–v2.1.77 — 2026-03-13

**Prompt hash:** `3387e952e0eed0ee`
**Diff size:** ~1026 chars

### Key changes
- Removed the instruction to use the ask tool when a tool call is denied without explanation.

---

## v2.1.72–v2.1.74 — 2026-03-09

**Prompt hash:** `b42f38f98c680a21`
**Diff size:** ~1026 chars

### Key changes
- Added: if Claude does not understand why a tool call was denied, it should use the ask tool to clarify with the user.

---

## v2.1.70–v2.1.71 — 2026-03-06

**Prompt hash:** `3387e952e0eed0ee`
**Diff size:** ~683 chars

### Key changes
- Removed the `<claude_background_info>` and `<fast_mode_info>` blocks from the prompt.

---

## v2.1.69 — 2026-03-04

**Prompt hash:** `ccd922a297a1d3eb`
**Diff size:** ~2169 chars

### Key changes
- Output efficiency section consolidated: replaced multiple-variant "CRITICAL/IMPORTANT/Go straight to the point" copies with a single IMPORTANT-prefixed version.

---

## v2.1.66–v2.1.68 — 2026-03-04

**Prompt hash:** `c3af9036662a49b1`
**Diff size:** ~2044 chars

### Key changes
- Restored the "Focus text output on decisions, milestones, and blockers" instruction and expanded output efficiency to include three labelled tiers (CRITICAL, IMPORTANT, unlabelled).

---

## v2.1.64 — 2026-03-03

**Prompt hash:** `ccd922a297a1d3eb`
**Diff size:** ~2169 chars

### Key changes
- Collapsed three output-efficiency paragraphs (CRITICAL / IMPORTANT / concise) into a single IMPORTANT-level instruction.

---

## v2.1.53–v2.1.63 — 2026-02-24

**Prompt hash:** `c3af9036662a49b1`
**Diff size:** ~11879 chars

### Key changes
- Major prompt restructure: replaced bullet-list style System section with prose instructions integrated into the general body.
- Added explicit note that tools are executed under a user-selected permission mode and users are prompted for confirmation when needed.
- Added prompt-injection warning: if a tool result appears to contain an injection attempt, flag it to the user before continuing.
- Added context compression notice: the system auto-compresses prior messages as context limit approaches.
- Merged anti-over-engineering rules ("Don't add features… Don't add error handling…") directly into the main instruction text.
- Added: if an approach is blocked, do not brute-force; consider alternatives rather than retrying the same failing action.

---

## v2.1.48–v2.1.52 — 2026-02-19

**Prompt hash:** `d3ebd52485b893d2`
**Diff size:** ~1847 chars

### Key changes
- Added a new "Output efficiency" section instructing Claude to focus text output on decisions needing user input, high-level status updates, and blockers; prefer short direct sentences.

---

## v2.1.42–v2.1.47 — 2026-02-13

**Prompt hash:** `d23f3ff4b69049b7`
**Diff size:** ~223 chars

### Key changes
- Removed "Today's date" from the environment info block injected into the prompt.

---

## v2.1.36–v2.1.41 — 2026-02-07

**Prompt hash:** `0ae18e00949be45d`
**Diff size:** ~585 chars

### Key changes
- Added `<fast_mode_info>` block explaining that fast mode uses the same model with faster output and can be toggled with `/fast`.

---

## v2.1.32–v2.1.34 — 2026-02-05

**Prompt hash:** `865a790628d295a3`
**Diff size:** ~1879 chars

Minor wording adjustment.

---

## v2.1.30–v2.1.31 — 2026-02-03

**Prompt hash:** `ae69a8f3c9d87a8a`
**Diff size:** ~2674 chars

### Key changes
- Added new "Executing actions with care" section: Claude must consider reversibility and blast radius before acting, and must ask for confirmation for destructive or hard-to-reverse operations (deleting files/branches, force-pushing, modifying CI/CD pipelines, posting to external services, etc.).

---

## v2.1.20–v2.1.29 — 2026-01-27

**Prompt hash:** `2220b6d128d3ce5f`
**Diff size:** ~3049 chars

### Key changes
- Added instruction to use the plan/todo tool for task planning and the ask tool for clarifying questions.
- Removed the strict "NEVER propose changes to code you haven't read" rule.

---

## v2.1.9–v2.1.19 — 2026-01-15

**Prompt hash:** `db63f96474b7d873`
**Diff size:** ~3198 chars

### Key changes
- Rewrote the no-timeline rule: replaced "Planning without timelines" (no time estimates in task plans) with a broader "No time estimates" rule that covers both Claude's own work and project-planning advice.

---

## v2.1.1–v2.1.8 — 2026-01-07

**Prompt hash:** `619e241a0076ce83`
**Diff size:** ~3524 chars

### Key changes
- Removed the "Insights" and "Requesting Human Contributions" educational mode sections; restored the model-identity block.

---

## v2.1.0 — 2026-01-07

**Prompt hash:** `d5c0f80718f3bbdd`
**Diff size:** ~3525 chars

### Key changes
- Re-added the "Insights" (Explanatory Style / Learning Style) and "Requesting Human Contributions" educational scaffolding sections.
- Removed the `<claude_background_info>` block containing the most-recent-model reference.

---

## v2.0.77 — 2026-01-06

**Prompt hash:** `619e241a0076ce83`
**Diff size:** ~3404 chars

### Key changes
- Re-added the rule: do not use a colon before tool calls (e.g. "Let me read the file." not "Let me read the file:").

---

## v2.0.75–v2.0.76 — 2025-12-20

**Prompt hash:** `0de13d16a1dcf2ac`
**Diff size:** ~3404 chars

### Key changes
- Removed the "do not use a colon before tool calls" instruction.

---

## v2.0.68–v2.0.74 — 2025-12-12

**Prompt hash:** `619e241a0076ce83`
**Diff size:** ~3404 chars

### Key changes
- Added the rule: do not use a colon before tool calls, since tool calls may not appear inline in output.

---

## v2.0.47–v2.0.67 — 2025-11-19

**Prompt hash:** `0de13d16a1dcf2ac`
**Diff size:** ~1898 chars

### Key changes
- Added several anti-over-engineering rules: never propose changes to unread code; avoid over-engineering; don't add features or refactors beyond what was asked; don't add unnecessary error handling; don't create helpers for one-time operations.

---

## v2.0.43–v2.0.46 — 2025-11-17

**Prompt hash:** `93d5e3a6488f2c32`
**Diff size:** ~2723 chars

### Key changes
- Added "Planning without timelines" section: provide concrete implementation steps without time estimates; never suggest timelines like "this will take 2-3 weeks."
- Added rule to avoid backwards-compatibility hacks (renaming `_vars`, re-exporting types, adding `// removed` comments); delete unused code completely.

---

## v2.0.36–v2.0.42 — 2025-11-07

**Prompt hash:** `e77f1dcf45348ab9`
**Diff size:** ~517 chars

Minor wording adjustment.

---

## v2.0.34–v2.0.35 — 2025-11-05

**Prompt hash:** `ba45c7b3f6d7b2c0`
**Diff size:** ~517 chars

Minor wording adjustment.

---

## v2.0.31–v2.0.33 — 2025-10-31

**Prompt hash:** `6e0aa6a7009fc33c`
**Diff size:** ~3933 chars

### Key changes
- Removed all "Insights" and "Requesting Human Contributions" educational mode sections.
- Added `<claude_background_info>` block noting the most recent frontier Claude model.

---

## v2.0.30 — 2025-10-30

**Prompt hash:** `7ca9caeb1d5a7bc0`
**Diff size:** ~3443 chars

### Key changes
- Re-added "Insights" (Explanatory Style / Learning Style) and "Requesting Human Contributions" educational scaffolding sections.
- Added security guidance: be careful not to introduce vulnerabilities (command injection, XSS, SQL injection, OWASP top 10); fix immediately if insecure code is noticed.

---

## v2.0.28–v2.0.29 — 2025-10-27

**Prompt hash:** `8df1f8623f74b767`
**Diff size:** ~3274 chars

Minor wording adjustment.

---

## v2.0.22–v2.0.27 — 2025-10-17

**Prompt hash:** `1c40c3ae16c8713e`
**Diff size:** ~222 chars

Minor wording adjustment.

---

## v2.0.14–v2.0.21 — 2025-10-10

**Prompt hash:** `70fdd881ae5e6cd2`
**Diff size:** ~3058 chars

### Key changes
- Added "# Tone and style" header to the System section.
- Added explicit instruction: never create files unless absolutely necessary; always prefer editing an existing file (including markdown files).
- Added output-to-user instruction inside the System section.

---

## v2.0.12–v2.0.13 — 2025-10-09

**Prompt hash:** `0b69a6bc957d291e`
**Diff size:** ~303 chars

Minor wording adjustment.

---

## v2.0.11 — 2025-10-08

**Prompt hash:** `f0eb125151717a89`
**Diff size:** ~5453 chars

### Key changes
- Condensed tone/style guidance into the System section: short and concise responses, emoji restriction, and professional objectivity.
- Removed the standalone "# Proactiveness" section and verbose conciseness rules (4-line limit, no preamble) from the previous structure.
- Merged "# Professional objectivity" directly into the System section.

---

## v2.0.8–v2.0.10 — 2025-10-04

**Prompt hash:** `c4a2cfe22c096028`
**Diff size:** ~2155 chars

### Key changes
- Rewrote "Professional objectivity": expanded from a truncated sentence to a full instruction to prioritize technical accuracy over validating the user's beliefs, focusing on facts without unnecessary superlatives.
- Removed the CommonMark/markdown rendering reminder from the General section.

---

## v2.0.5 — 2025-10-02

**Prompt hash:** `bc54ef52e07da612`
**Diff size:** ~2155 chars

### Key changes
- Reverted the professional-objectivity expansion from v2.0.2–v2.0.3; restored the abbreviated form.

---

## v2.0.2–v2.0.3 — 2025-09-30

**Prompt hash:** `c4a2cfe22c096028`
**Diff size:** ~2155 chars

### Key changes
- Rewrote "Professional objectivity" to full sentence form: prioritize technical accuracy and truthfulness over validating user beliefs.

---

## v2.0.1 — 2025-09-30

**Prompt hash:** `bc54ef52e07da612`
**Diff size:** ~3273 chars

### Key changes
- Removed all "Insights" (Explanatory Style / Learning Style) and "Requesting Human Contributions" sections introduced in v2.0.0.
- Restored model identity block.

---

## v2.0.0 — 2025-09-29

**Prompt hash:** `1bab6d5d861c0813`
**Diff size:** ~4854 chars

### Key changes
- Added "Insights" section with Explanatory Style and Learning Style modes: Claude provides brief educational explanations before and after writing code.
- Added "Requesting Human Contributions" section: Claude invites users to write 2–10 line code pieces on design decisions, business logic, and key algorithms in a "Learn by Doing" format.
- Removed model identity and "NEVER commit" commit-guard instructions from this section.

---

## v1.0.128 — 2025-09-27

**Prompt hash:** `0d9444ee05661aaa`
**Diff size:** ~3576 chars

### Key changes
- Rewrote conciseness instruction: replaced hard "fewer than 4 lines" and "one word answers" rules with a more nuanced instruction to match detail level to query complexity.
- After completing file work, briefly confirm completion rather than just stopping silently.
- Reworded brevity guideline: "Brief answers are best, but be sure to provide complete information."

---

## v1.0.127 — 2025-09-26

**Prompt hash:** `2f42be9792a5754b`
**Diff size:** ~2513 chars

### Key changes
- Replaced the explicit task steps (search, implement, verify, lint) with a single bullet placeholder in the Doing tasks section.

---

## v1.0.125–v1.0.126 — 2025-09-25

**Prompt hash:** `2f4073537b29d5d1`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.124 — 2025-09-25

**Prompt hash:** `5b8844ea140e7a8e`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.122–v1.0.123 — 2025-09-23

**Prompt hash:** `2f4073537b29d5d1`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.116–v1.0.120 — 2025-09-16

**Prompt hash:** `c4af38d26a477a6b`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.115 — 2025-09-16

**Prompt hash:** `fa90290cf4bb7faf`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.114 — 2025-09-15

**Prompt hash:** `22a820c924f949b2`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.113 — 2025-09-13

**Prompt hash:** `fa90290cf4bb7faf`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.111–v1.0.112 — 2025-09-10

**Prompt hash:** `513ec8b5107b1018`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.110 — 2025-09-09

**Prompt hash:** `22a820c924f949b2`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.109 — 2025-09-08

**Prompt hash:** `9e1ff7a97dd23f9b`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.108 — 2025-09-05

**Prompt hash:** `3f41310d3eee9da6`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.107 — 2025-09-05

**Prompt hash:** `9465fce7b472b787`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.106 — 2025-09-04

**Prompt hash:** `0863f8e5eec89dff`
**Diff size:** ~3746 chars

### Key changes
- Added "# Professional objectivity" section: prioritize technical accuracy over validating user beliefs; provide direct, objective technical information.
- Rewrote brevity rule: "Answer the user's question directly, avoiding any elaboration… Brief answers are best, but be sure to provide complete information."
- Removed the "# Following conventions" section (code style / library check guidelines).

---

## v1.0.103–v1.0.105 — 2025-09-03

**Prompt hash:** `f5d6c607e5ce6cbc`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.102 — 2025-09-02

**Prompt hash:** `a029512ebab9d982`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.98–v1.0.100 — 2025-08-29

**Prompt hash:** `91f67dc1647fedfb`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.96 — 2025-08-28

**Prompt hash:** `4009d7f0298b7da7`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.93–v1.0.95 — 2025-08-26

**Prompt hash:** `30c4b249f8323701`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.91–v1.0.92 — 2025-08-25

**Prompt hash:** `4009d7f0298b7da7`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.89–v1.0.90 — 2025-08-22

**Prompt hash:** `fb12646f00678879`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.87–v1.0.88 — 2025-08-21

**Prompt hash:** `46c04d62d73f5926`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.86 — 2025-08-20

**Prompt hash:** `aa3be0e590fb521e`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.85 — 2025-08-19

**Prompt hash:** `00465753e65ad575`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.84 — 2025-08-18

**Prompt hash:** `aa3be0e590fb521e`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.83 — 2025-08-15

**Prompt hash:** `b0548ebcdf2458d4`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.80–v1.0.82 — 2025-08-13

**Prompt hash:** `aa3be0e590fb521e`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.78–v1.0.79 — 2025-08-13

**Prompt hash:** `d06f24597900afa1`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.74–v1.0.77 — 2025-08-12

**Prompt hash:** `553c75ab0c9e47cb`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.73 — 2025-08-11

**Prompt hash:** `63c8056e541ecbd8`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.72 — 2025-08-08

**Prompt hash:** `d7e6afa2e53a5121`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.71 — 2025-08-07

**Prompt hash:** `a03b785121212352`
**Diff size:** ~2698 chars

### Key changes
- Replaced the agent-mode identity ("You are an agent for Claude Code…" with strengths/guidelines) with the simpler identity: "You are Claude Code, Anthropic's official CLI for Claude."

---

## v1.0.70 — 2025-08-06

**Prompt hash:** `af15b62bde95b0fd`
**Diff size:** ~1641 chars

### Key changes
- Minor wording change in an example assistant response: "runs ls" instead of "use the ls tool."

---

## v1.0.69 — 2025-08-05

**Prompt hash:** `4c93e80133667c91`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.68 — 2025-08-04

**Prompt hash:** `5e9f09fabff3a7bb`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.66–v1.0.67 — 2025-08-01

**Prompt hash:** `f4f062d1ddd8ee53`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.65 — 2025-07-31

**Prompt hash:** `6e8042e612165bfd`
**Diff size:** ~3764 chars

### Key changes
- Added "# Tone and style" header.
- Removed hooks-feedback, system-reminder, and tool-usage-policy blocks from the Coding Instructions section (likely reorganised into other sections).

---

## v1.0.64 — 2025-07-30

**Prompt hash:** `fa82b26ba25401ef`
**Diff size:** ~1217 chars

Minor wording adjustment.

---

## v1.0.63 — 2025-07-29

**Prompt hash:** `ba9d4d58211cc83d`
**Diff size:** ~20546 chars

### Key changes
- Major restructure: moved "# Doing tasks" steps, tool-usage-policy, and hooks-feedback from the Tone and Style section into Coding Instructions.
- Removed the full "Tone and Style" section content (proactiveness, following conventions, code style rules, markdown rendering note, emoji policy).
- The "Coding Instructions" section now owns the main task workflow.

---

## v1.0.61–v1.0.62 — 2025-07-25

**Prompt hash:** `873ddfb45f007b13`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.60 — 2025-07-24

**Prompt hash:** `2000ef36d5fed066`
**Diff size:** ~1219 chars

Minor wording adjustment.

---

## v1.0.59 — 2025-07-23

**Prompt hash:** `1cff5fe47fce8c62`
**Diff size:** ~16606 chars

### Key changes
- Added "# Proactiveness" section: balance taking requested actions with not surprising users; answer questions before jumping to actions.
- Added "# Following conventions" section: mimic existing code style, verify library availability before use, follow naming/typing conventions, enforce security best practices.
- Condensed conciseness rules: "You should be concise, direct, and to the point." plus a 4-line limit and no-preamble rules.
- Added: "Do not add additional code explanation summary unless requested. After working on a file, just stop."
- Added direct-answer rule: "Answer the user's question directly, without elaboration… One word answers are best."
- Removed several conciseness example dialogues (2+2, prime number examples).

---

## v1.0.58 — 2025-07-22

**Prompt hash:** `4827e0d9473a0495`
**Diff size:** ~2692 chars

Minor wording adjustment.

---

## v1.0.57 — 2025-07-21

**Prompt hash:** `90bfeca69906d12f`
**Diff size:** ~1644 chars

### Key changes
- Added Shell field to the environment info block.

---

## v1.0.56 — 2025-07-18

**Prompt hash:** `419876cb758391a5`
**Diff size:** ~1547 chars

### Key changes
- Added an additional environment context field to the prompt header.

---

## v1.0.55 — 2025-07-17

**Prompt hash:** `e579ea878327757d`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.54 — 2025-07-16

**Prompt hash:** `a13cb6809394b523`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.53 — 2025-07-15

**Prompt hash:** `e06057a8d0bb81a3`
**Diff size:** ~14409 chars

### Key changes
- Added agent-mode identity paragraph: "You are an agent for Claude Code… Do what has been asked; nothing more, nothing less."
- Added agent strengths list: code search, multi-file analysis, complex investigations, multi-step research.
- Added agent guidelines: prefer Grep/Glob over find, never create files unless necessary, never proactively create docs/READMEs, share absolute paths, avoid emojis.
- Changed hooks-feedback instruction: treat hooks (including `<user-prompt-submit-hook>`) as user feedback rather than as blockers to work around.
- Added custom-slash-command instruction in Tone and Style: execute slash commands via the appropriate tool.

---

## v1.0.52 — 2025-07-15

**Prompt hash:** `2398feb7cf76b826`
**Diff size:** ~501 chars

### Key changes
- Added detailed PR-creation guidelines (NEVER update git config, DO NOT use certain tools, return PR URL).
- Added "# Other common operations" section with a `gh api` example for viewing PR comments.

---

## v1.0.45–v1.0.51 — 2025-07-08

**Prompt hash:** `c3ba9de0f2a306a5`
**Diff size:** ~765 chars

Minor wording adjustment.

---

## v1.0.44 — 2025-07-07

**Prompt hash:** `d3be356d0d29df94`
**Diff size:** ~739 chars

### Key changes
- Completed the truncated `<system-reminder>` tag text in the tool-results instruction.

---

## v1.0.42–v1.0.43 — 2025-07-03

**Prompt hash:** `c8418985bad9ed6f`
**Diff size:** ~2051 chars

### Key changes
- Completed truncated "Tool results and user messages" instruction text.
- Updated tool-usage-policy to include the full batching instruction text.

---

## v1.0.38–v1.0.41 — 2025-06-30

**Prompt hash:** `75f1c06e30db775b`
**Diff size:** ~14375 chars

### Key changes
- Added user-configurable hooks instruction: if blocked by a hook, determine whether to adjust actions rather than simply failing.
- Removed the task-tracking TodoList tool instruction, code-references pattern (`file_path:line_number`), and environment info block from this section.
- Removed the full Tone and Style section (moved or merged elsewhere).

---

## v1.0.35–v1.0.37 — 2025-06-25

**Prompt hash:** `7cbe99b2500ab050`
**Diff size:** ~13846 chars

### Key changes
- Added instruction to always use the TodoList tool to plan and track tasks throughout the conversation.
- Added "# Code References" section: reference specific functions using `file_path:line_number` pattern.
- Added model-identity lines ("You are powered by the model named…") to the prompt.
- Added full Tone and Style section with conciseness and no-preamble instructions.
- Removed the old example dialogues for "write tests" task.

---

## v1.0.34 — 2025-06-24

**Prompt hash:** `b8248052239c5e77`
**Diff size:** ~1638 chars

Minor wording adjustment.

---

## v1.0.31–v1.0.33 — 2025-06-20

**Prompt hash:** `cee83968eb62739a`
**Diff size:** ~8712 chars

### Key changes
- Restored the full interactive-CLI identity paragraph, URL policy, help/feedback instructions, and Tone and Style section.
- Added response brevity examples ("2 + 2 → 4", "what is 2+2?").
- Added: "IMPORTANT: Keep your responses short… fewer than 4 lines."

---

## v1.0.30 — 2025-06-19

**Prompt hash:** `060fa115261057f7`
**Diff size:** ~210 chars

### Key changes
- Added Shell field before Platform in the environment info block.

---

## v1.0.28–v1.0.29 — 2025-06-18

**Prompt hash:** `f02fc875f32afe2f`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.26–v1.0.27 — 2025-06-17

**Prompt hash:** `d0c17bc2af0a26b4`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.25 — 2025-06-16

**Prompt hash:** `fc3e259981d4de56`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.24 — 2025-06-14

**Prompt hash:** `f02fc875f32afe2f`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.23 — 2025-06-13

**Prompt hash:** `5e43b762558793a2`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.22 — 2025-06-12

**Prompt hash:** `052fe40bec2c32e5`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.21 — 2025-06-11

**Prompt hash:** `f3e983410f64dafd`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.20 — 2025-06-11

**Prompt hash:** `d0c17bc2af0a26b4`
**Diff size:** ~3124 chars

### Key changes
- Removed the explicit malicious-code-refusal instructions ("IMPORTANT: Refuse to write code or explain code that may be used maliciously…").

---

## v1.0.19 — 2025-06-10

**Prompt hash:** `0b5d45e375d0de83`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.18 — 2025-06-09

**Prompt hash:** `262c5b36ceac9fe3`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.17 — 2025-06-06

**Prompt hash:** `f538208d78a2edcb`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.16 — 2025-06-06

**Prompt hash:** `143b6b4a5f0c6622`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.15 — 2025-06-05

**Prompt hash:** `f538208d78a2edcb`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.11–v1.0.14 — 2025-06-04

**Prompt hash:** `143b6b4a5f0c6622`
**Diff size:** ~1444 chars

Minor wording adjustment.

---

## v1.0.10 — 2025-06-03

**Prompt hash:** `3f03c96b84b7e8c2`
**Diff size:** ~1443 chars

Minor wording adjustment.

---

## v1.0.8–v1.0.9 — 2025-06-02

**Prompt hash:** `aee8d8fda69099da`
**Diff size:** ~1442 chars

Minor wording adjustment.

---

## v1.0.7 — 2025-05-30

**Prompt hash:** `9ff9b4900eafd8d0`
**Diff size:** ~3822 chars

### Key changes
- Added: "Only use emojis if the user explicitly requests it. Avoid using emojis in all communication unless asked." (appears in multiple sections).

---

## v1.0.6 — 2025-05-29

**Prompt hash:** `b47089de870b6047`
**Diff size:** ~1496 chars

Minor wording adjustment.

---

## v1.0.4–v1.0.5 — 2025-05-28

**Prompt hash:** `5027f7bed9048dd2`
**Diff size:** ~3185 chars

### Key changes
- Updated model-identity format: replaced single "Model: {{...}}" environment field with two-line format "You are powered by the model named {{...}}. The exact model ID is {{...}}." plus a shorter fallback line.
- Updated docs sub-pages list format.

---

## v1.0.3 — 2025-05-23

**Prompt hash:** `0a45673800ba84c4`
**Diff size:** ~1496 chars

Minor wording adjustment.

---

## v1.0.0–v1.0.2 — 2025-05-22

**Prompt hash:** `871d2ecb4c7bc940`
**Diff size:** ~3248 chars

### Key changes
- Updated tool-usage-policy wording: replaced the older parallel-calls instruction with "You have the capability to call multiple tools in a single response. When multiple independent pieces of information are requested, batch your tool calls together for optimal performance."

---

## v0.2.126 — 2025-05-22

**Prompt hash:** `74e65416a5fdbb6f`
**Diff size:** ~1500 chars

Minor wording adjustment.

---

## v0.2.125 — 2025-05-21

**Prompt hash:** `aa22721cdc59fd97`
**Diff size:** ~1500 chars

Minor wording adjustment.

---

## v0.2.123–v0.2.124 — 2025-05-20

**Prompt hash:** `e22be869d347eee4`
**Diff size:** ~14080 chars

### Key changes
- Moved "# Proactiveness", "# Following conventions", and "# Code style" sections from General into the Tone and Style section.
- Minor formatting change in the conciseness rule (space before parenthetical in "fewer than 4 lines of text").

---

## v0.2.119–v0.2.122 — 2025-05-19

**Prompt hash:** `909fa14ca3b373ef`
**Diff size:** ~1500 chars

Minor wording adjustment.

---

## v0.2.118 — 2025-05-18

**Prompt hash:** `e44adf77bce5aa18`
**Diff size:** ~1500 chars

Minor wording adjustment.

---

## v0.2.117 — 2025-05-17

**Prompt hash:** `bcf4ce707871ac31`
**Diff size:** ~1500 chars

Minor wording adjustment.

---

## v0.2.116 — 2025-05-17

**Prompt hash:** `8e36bfc3b2d09971`
**Diff size:** ~14085 chars

### Key changes
- Added "# Proactiveness" section: balance taking requested actions with not surprising users; answer questions before jumping to actions.
- Added "# Following conventions" section: mimic existing code style, verify library availability before use, follow naming/typing conventions, enforce security best practices.
- Added "# Code style" section with the IMPORTANT: DO NOT ADD COMMENTS rule.
- Reorganised sections: these new sections moved into General from Coding Instructions.

---

## v0.2.113 — 2025-05-13

**Prompt hash:** `92bf53685beb4e42`
**Diff size:** ~1510 chars

Minor wording adjustment.

---

## v0.2.108–v0.2.109 — 2025-05-13

**Prompt hash:** `e54cb69f1447071a`
**Diff size:** ~3115 chars

### Key changes
- Updated docs lookup instruction: replaced generic "Overview" and "Tutorials" links with a structured sub-pages list (`overview`, `cli-usage`, `memory`, `settings`, `security`) and an example URL pattern.

---

## v0.2.106–v0.2.107 — 2025-05-09

**Prompt hash:** `373c3d3898958f2e`
**Diff size:** ~3534 chars

### Key changes
- Added instruction that tool results and user messages may include `<system-reminder>` tags, which are not part of user input or tool results.

---

## v0.2.103–v0.2.105 — 2025-05-06

**Prompt hash:** `62f1efc376a19cad`
**Diff size:** ~1510 chars

Minor wording adjustment.

---

## v0.2.102 — 2025-05-05

**Prompt hash:** `4a7099884c67eb8e`
**Diff size:** ~1510 chars

Minor wording adjustment.

---

## v0.2.101 — 2025-05-05

**Prompt hash:** `e74529eadab55ca0`
**Diff size:** ~2779 chars

### Key changes
- Removed the "# Synthetic messages" section that explained how synthetic assistant messages appear in conversation.

---

## v0.2.96–v0.2.100 — 2025-05-01

**Prompt hash:** `31dbd8f23261a921`
**Diff size:** ~961 chars

### Key changes
- Replaced raw JavaScript template string expressions for environment variables with clean placeholder format.
- Added "Today's date" and "Model" fields to the environment info block.
- Added "Here is useful information about the environment you are running in:" header.

---

## v0.2.93–v0.2.94 — 2025-04-30

**Prompt hash:** `b9279a9010d50249`
**Diff size:** ~2807 chars

Minor wording adjustment.

---

## v0.2.92 — 2025-04-29

**Prompt hash:** `c728789c43539efb`
**Diff size:** ~1286 chars

Minor wording adjustment.

---

## v0.2.91 — 2025-04-29

**Prompt hash:** `d81caddf0d0e31de`
**Diff size:** ~1323 chars

Minor wording adjustment.

---

## v0.2.90 — 2025-04-29

**Prompt hash:** `2bd6f157921edcf9`
**Diff size:** ~1323 chars

Minor wording adjustment.

---

## v0.2.89 — 2025-04-28

**Prompt hash:** `ef83247fec5aa645`
**Diff size:** ~2807 chars

Minor wording adjustment.

---

## v0.2.86 — 2025-04-26

**Prompt hash:** `58e3242ff21248d5`
**Diff size:** ~1214 chars

Minor wording adjustment.

---

## v0.2.85 — 2025-04-25

**Prompt hash:** `eaecd0df102b84a3`
**Diff size:** ~2698 chars

Minor wording adjustment.

---

## v0.2.84 — 2025-04-25

**Prompt hash:** `8b5588dca00afb15`
**Diff size:** ~1214 chars

Minor wording adjustment.

---

## v0.2.83 — 2025-04-25

**Prompt hash:** `c0b19b016253a7a7`
**Diff size:** ~5235 chars

### Key changes
- Removed the explicit "# Tool usage policy" text from both the System Prompt and Coding Instructions sections; replaced with a collapsed placeholder format.
- Removed the individual parallel-calls rule ("When making multiple tool calls, you MUST use {{...}} to run the calls in parallel").

---

## v0.2.81 — 2025-04-24

**Prompt hash:** `4cb57fdc62a1dea8`
**Diff size:** ~1174 chars

Minor wording adjustment.

---

## v0.2.80 — 2025-04-24

**Prompt hash:** `218076beacbab0f4`
**Diff size:** ~2730 chars

Minor wording adjustment.

---

## v0.2.79 — 2025-04-23

**Prompt hash:** `3fe248aeed5755da`
**Diff size:** ~1283 chars

Minor wording adjustment.

---

## v0.2.78 — 2025-04-22

**Prompt hash:** `4254bd0bde38302a`
**Diff size:** ~1174 chars

Minor wording adjustment.

---

## v0.2.77 — 2025-04-22

**Prompt hash:** `212394440b4c046f`
**Diff size:** ~6783 chars

### Key changes
- Changed task steps from numbered list (1. 2. 3. 4.) to unnumbered bullet list (- - - -) in both the System Prompt and Coding Instructions sections.

---

## v0.2.76 — 2025-04-21

**Prompt hash:** `3d66c2d575faa4cb`
**Diff size:** ~2583 chars

### Key changes
- Added "OS Version" field to the environment info block.

---

## v0.2.74 — 2025-04-18

**Prompt hash:** `954ed0c2e15e487f`
**Diff size:** ~936 chars

Minor wording adjustment.

---

## v0.2.73 — 2025-04-18

**Prompt hash:** `898b364095f551e2`
**Diff size:** ~2487 chars

Minor wording adjustment.

---

## v0.2.72 — 2025-04-17

**Prompt hash:** `25127aef00340dbc`
**Diff size:** ~2487 chars

Minor wording adjustment.

---

## v0.2.70 — 2025-04-15

**Prompt hash:** `29bc28671e124965`
**Diff size:** ~2420 chars

Minor wording adjustment.

---

## v0.2.69 — 2025-04-11

**Prompt hash:** `d8ec98b6496ee544`
**Diff size:** ~2092 chars

Minor wording adjustment.

---

## v0.2.67–v0.2.68 — 2025-04-09

**Prompt hash:** `2542cc5b62879984`
**Diff size:** ~2487 chars

Minor wording adjustment.

---

## v0.2.66 — 2025-04-09

**Prompt hash:** `9ad0434667bef5f1`
**Diff size:** ~14281 chars

### Key changes
- Major reorganisation: removed the interactive-CLI identity, URL policy, help/feedback instructions, and Tone and Style section from the General section; moved them into "Coding Instructions."
- The "Coding Instructions" section now leads with the full task-workflow instructions rather than them appearing in the General section.

---

## v0.2.65 — 2025-04-07

**Prompt hash:** `f3492834ab25e772`
**Diff size:** ~2487 chars

Minor wording adjustment.

---

## v0.2.64 — 2025-04-04

**Prompt hash:** `f8a08bbc714fe603`
**Diff size:** ~2487 chars

Minor wording adjustment.

---

## v0.2.62 — 2025-04-04

**Prompt hash:** `914ac03a92395db7`
**Diff size:** ~13190 chars

### Key changes
- Re-added interactive-CLI identity paragraph, URL policy, help/feedback instructions, and Tone and Style section to the General section.
- Re-added malicious-code-refusal instructions to the General section.

---

## v0.2.61 — 2025-04-03

**Prompt hash:** `e9d7f868c7201c51`
**Diff size:** ~936 chars

Minor wording adjustment.

---

## v0.2.60 — 2025-04-02

**Prompt hash:** `85f3f28d320687a2`
**Diff size:** ~936 chars

Minor wording adjustment.

---

## v0.2.59 — 2025-04-02

**Prompt hash:** `b6aecb085b5fadd9`
**Diff size:** ~2481 chars

Minor wording adjustment.

---

## v0.2.57 — 2025-03-31

**Prompt hash:** `037a8d507bfbe4e2`
**Diff size:** ~2515 chars

Minor wording adjustment.

---

## v0.2.56 — 2025-03-27

**Prompt hash:** `e965d60b8dd7b597`
**Diff size:** ~2420 chars

Minor wording adjustment.

---

## v0.2.55 — 2025-03-26

**Prompt hash:** `f078c36b0a657e2b`
**Diff size:** ~2481 chars

Minor wording adjustment.

---

## v0.2.54 — 2025-03-25

**Prompt hash:** `9e1afe3641ed9d58`
**Diff size:** ~4718 chars

### Key changes
- Added dedicated help/feedback block: "If the user asks for help or wants to give feedback inform them of the following."
- Changed the docs-lookup trigger to only fire when the user directly asks about Claude Code capabilities, and to use the tool to gather information from docs before answering.
- Replaced hardcoded doc URLs with dynamic placeholders for Overview and Tutorials.

---

## v0.2.53 — 2025-03-21

**Prompt hash:** `4e23647f2885cc46`
**Diff size:** ~13187 chars

### Key changes
- Major restructure: removed interactive-CLI identity, URL policy, help/feedback, slash commands, and Tone and Style section from the Tone and Style section; moved content into General section with raw template expressions.
- Removed the malicious-code-refusal IMPORTANT blocks from the Tone and Style section.

---

## v0.2.52 — 2025-03-20

**Prompt hash:** `f91a9d5dfa821ba4`
**Diff size:** ~13474 chars

### Key changes
- Added dedicated "Tone and Style" section with: interactive-CLI identity, malicious-code-refusal IMPORTANT blocks, URL-generation policy, slash command list, feedback/help info, docs tool instruction with Overview and Tutorials links, conciseness and brevity rules.
- Added synthetic-messages explanation: system-injected assistant messages may appear in conversation.
- Removed old CLAUDE.md section describing its three purposes (bash commands, code style prefs, codebase structure).

---

## v0.2.51 — 2025-03-20

**Prompt hash:** `5873ce333eba1e0d`
**Diff size:** ~3341 chars

### Key changes
- Added feedback link placeholder to replace the `/compact` slash command entry.
- Removed `/compact: Compact and continue the conversation` from the slash-commands list.
- Removed the inline help-docs instruction (the `claude -h` second-person trigger).

---

## v0.2.50 — 2025-03-19

**Prompt hash:** `fbe27675a4a1e4b2`
**Diff size:** ~1031 chars

Minor wording adjustment.

---

## v0.2.49 — 2025-03-18

**Prompt hash:** `19e701fd34a6ce96`
**Diff size:** ~1647 chars

### Key changes
- Strengthened the no-comments rule: replaced "Do not add comments to the code you write, unless the user asks you to, or the code is complex" with "IMPORTANT: DO NOT ADD ***ANY*** COMMENTS unless asked."

---

## v0.2.47–v0.2.48 — 2025-03-18

**Prompt hash:** `5c6dd2c0f173d4c9`
**Diff size:** ~2515 chars

Minor wording adjustment.

---

## v0.2.46 — 2025-03-17

**Prompt hash:** `1404ccb0b79c5e87`
**Diff size:** ~1043 chars

### Key changes
- Added "Is directory a git repo" field to the environment info block.

---

## v0.2.45 — 2025-03-15

**Prompt hash:** `92b2831eb3154539`
**Diff size:** ~936 chars

Minor wording adjustment.

---

## v0.2.44 — 2025-03-15

**Prompt hash:** `b72dbcd5cc1d749d`
**Diff size:** ~2481 chars

Minor wording adjustment.

---

## v0.2.43 — 2025-03-14

**Prompt hash:** `5c42ed404806b087`
**Diff size:** ~936 chars

Minor wording adjustment.

---

## v0.2.42 — 2025-03-14

**Prompt hash:** `d9b9c7ba2f7a3640`
**Diff size:** ~5033 chars

### Key changes
- Added: "IMPORTANT: You must NEVER generate or guess URLs for the user unless you are confident that the URLs are for helping the user with programming."
- Added: "VERY IMPORTANT: When making multiple tool calls, you MUST use {{...}} to run the calls in parallel."
- Changed the slash-commands help trigger: only run `claude -h` if the user directly asks about Claude Code or asks in second person ("are you able…", "can you do…"), rather than any mention.
- Changed `assistant: true` to `assistant: Yes` in an example response.

---

## v0.2.41 — 2025-03-14

**Prompt hash:** `9e639fd96503f2d2`
**Diff size:** ~2515 chars

Minor wording adjustment.

---

## v0.2.40 — 2025-03-13

**Prompt hash:** `eb733f976f915e5e`
**Diff size:** ~2515 chars

Minor wording adjustment.

---

## v0.2.39 — 2025-03-13

**Prompt hash:** `63ffdcf1cf91f88e`
**Diff size:** ~1003 chars

Minor wording adjustment.

---

## v0.2.38 — 2025-03-12

**Prompt hash:** `cc24e40f7403b56f`
**Diff size:** ~2599 chars

### Key changes
- Changed `assistant: true` to `assistant: Yes` in the example conversation snippet.

---

## v0.2.37 — 2025-03-11

**Prompt hash:** `0957a3e1eb79b80b`
**Diff size:** ~2487 chars

Minor wording adjustment.

---

## v0.2.36 — 2025-03-10

**Prompt hash:** `256643181795949d`
**Diff size:** ~2460 chars

### Key changes
- Added `{{...}}` (parallel tool call syntax) to the lint/typecheck completion instruction: "you MUST run the lint and typecheck commands… with {{...}} if they were provided."

---

## v0.2.35 — 2025-03-08

**Prompt hash:** `fde6009b047cfdf3`
**Diff size:** ~2420 chars

Minor wording adjustment.

---

## v0.2.33–v0.2.34 — 2025-03-07 — Initial capture

**Prompt hash:** `24d86e23431478df`

First captured version. Sections include general instructions, coding guidelines, tool usage policy, environment info (working directory, git repo status, platform), malicious-code refusal rules, and slash-command help instructions.

---
