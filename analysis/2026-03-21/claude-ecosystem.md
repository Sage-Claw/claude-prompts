# Claude Product Ecosystem — System Prompt Comparison — 2026-03-21

Analysis of all Claude-branded products tracked in this repo: how Anthropic shapes
Claude's behavior differently for each surface, what's shared, and what's unique.

---

## Products Tracked

| Product | Type | Prompt content | Version |
|---|---|---|---|
| [Claude Code](../../claude-code/system-prompt.md) | CLI agent | Full system prompt | v2.1.80 |
| [Claude Cowork](../../claude-cowork/system-prompt.md) | Desktop agent (Mac) | Full system prompt | v0.2.2 / app 1.1.7714 |
| [Claude GitHub Action](../../claude-github-action/create-prompt.ts) | CI/CD agent | Dynamic prompt builder | v1.x |
| [Claude VS Code](../../claude-vs-code/vscode-extension-context.md) | IDE extension | Thin context layer | v2.0.12 |
| [Claude Agent SDK](../../claude-agent-sdk/types.py) | Developer SDK | Type definitions | latest |
| Claude Excel / PowerPoint / Chrome | Web add-ins | *(no downloadable prompt)* | — |

---

## 1. Architecture: How Each Product Is Built

```
Anthropic Claude API
        │
        ├── Claude Code (CLI / Node SEA binary)
        │       └── Claude Cowork (built on top of Claude Code + Agent SDK)
        │       └── Claude GitHub Action (uses Claude Code subprocess)
        │
        ├── Claude VS Code (extension calls Claude API directly)
        │
        └── Claude Agent SDK (Python library, wraps Claude Code)
```

**Claude Code is the foundation.** Cowork explicitly says "Claude is implemented on top of Claude Code and the Claude Agent SDK." The GitHub Action also launches a Claude Code process. The Agent SDK is a Python library that gives programmatic access to Claude Code's capabilities.

The web add-ins (Excel, PowerPoint, Chrome) are thin web clients — no embedded system prompt to extract.

---

## 2. Identity & Disclosure Policy

| Product | Identity statement | Disclosure rules |
|---|---|---|
| Claude Code | "You are Claude Code, Anthropic's official CLI for Claude." | None stated |
| Claude Cowork | NOT Claude Code. Do not mention the VM, Claude Code, or Agent SDK. | Active concealment of implementation |
| GitHub Action | "You are Claude, an AI assistant designed to help with GitHub issues and pull requests." | None stated |
| VS Code | None — only formatting instructions | N/A |

The GitHub Action uses the most generic identity ("You are Claude") with no product name. Cowork is the only product that explicitly instructs the model to hide its implementation details, framing itself as a product experience rather than a technical tool.

---

## 3. What's Shared Across Claude Code + Cowork

Cowork is built on Claude Code and inherits its behavioral foundation:

**Shared sections (same wording):**
- "Doing tasks" — coding task scope, don't propose changes without reading, no time estimates
- "Executing actions with care" — destructive ops policy, reversibility, blast radius
- "Tone and style" — concise, no emojis, file:line references
- "Output efficiency" — lead with answer, no preamble, one sentence rule
- "Using your tools" — dedicated tools over bash, parallel calls
- "System" — tool use display, permission modes, prompt injection warning, context compression disclosure

**What Cowork adds on top:**
- `<application_details>` — positions Claude in the Cowork product context
- `<claude_behavior>` — ~400 lines of claude.ai product-level policy:
  - Product information (what Anthropic products exist, how to find docs)
  - Refusal handling (child safety, weapons, malware, real public figures)
  - Legal/financial advice caveats
  - Tone and formatting (prose over bullets, CommonMark rules)
  - User wellbeing (mental health, self-harm, addiction)
  - Honesty and avoiding sycophancy
  - Memory and continuity (no false memories)
  - Cowork-specific tools (file management, workspace access, computer use)

This is the claude.ai system prompt layer injected into a Claude Code base. Cowork = Claude Code behavioral rules + claude.ai safety/product layer.

---

## 4. Claude GitHub Action — The Odd One Out

The GitHub Action has the most unique prompt design of any Claude product. It generates prompts dynamically in TypeScript (`create-prompt.ts`) rather than having a static system prompt.

### Two operating modes

**Tag mode** (default): Triggered by `@claude` in a PR comment or issue
- Constructs a full context prompt from GitHub API data (PR body, comments, review comments, changed files with SHA, images)
- Has simple prompt variant (`USE_SIMPLE_PROMPT=true`) for low-token contexts
- Injects `<trigger_comment>` with the actual user request
- Routes to different behaviors: code review vs. implementation

**Agent mode**: Runs an arbitrary prompt directly (set by workflow `prompt:` input)
```typescript
if (modeName === "agent") {
  return context.prompt || `Repository: ${context.repository}`;
}
```

### Unique characteristics

**Output channel is a single GitHub comment** — not stdout:
```
Your console outputs and tool results are NOT visible to the user.
ALL communication happens through your GitHub comment.
```
Uses `mcp__github_comment__update_claude_comment` exclusively. Never creates new comments. Uses a spinner HTML (`<img src="..."/>`) for in-progress state.

**Explicit capabilities/limitations section** — unique to this product:
- CAN: code review, implement changes, create PRs, one-comment-at-a-time
- CANNOT: submit formal GitHub reviews, approve PRs, post multiple comments, modify `.github/workflows/`, run outside repo context

**Co-authorship on commits** — includes `Co-authored-by:` trailer when the trigger user is known.

**Two commit strategies** depending on `useCommitSigning`:
- Signed: `mcp__github_file_ops__commit_files` (atomic MCP tool)
- Unsigned: `Bash(git add)` / `Bash(git commit)` / wrapped push script

**Security defaults:**
- WebSearch and WebFetch disabled by default (can be re-enabled)
- Disallows workflow file modifications
- Sanitizes comment bodies before injecting into prompt

**Task tracking via checklist in the comment** (`- [ ]` / `- [x]`), not via tools.

**Custom instructions injection** via `<custom_instructions>` tag if workflow `prompt:` input is set alongside a tag event.

**CLAUDE.md integration**: "REPOSITORY SETUP INSTRUCTIONS: Always read and follow these files." Appears twice — stronger emphasis than other products.

### Analysis structure in `<analysis>` tags
The prompt requires pre-analysis before acting:
```
Before taking any action, conduct your analysis inside <analysis> tags:
a. Summarize the event type and context
b. Determine if this is code review or implementation
c. List key information
d. Outline tasks and challenges
e. Propose high-level plan
f. Note any permission limitations
```

This is the only Claude product that mandates explicit chain-of-thought before acting.

---

## 5. Claude VS Code — Minimal Surface

The VS Code extension adds only 11 lines:
```
You are running inside a VSCode native extension environment.

IMPORTANT: When referencing files or code locations, use markdown link syntax...
```

This is a context layer injected on top of whatever model/system prompt is already configured. It doesn't override behavior, autonomy, or safety — it only changes how file references are formatted to make them clickable in the VS Code UI.

Notable: VS Code had only 2 meaningful prompt changes across 186 versions (v1.0.128 and v2.0.12), suggesting the extension's value is in the IDE integration, not behavioral differentiation.

---

## 6. Claude Agent SDK — Not a Prompt, But a Protocol

`types.py` is not a system prompt — it's the Python API surface for building agents on top of Claude Code. Key things it reveals about the Claude ecosystem:

**Permission modes:**
```python
PermissionMode = Literal["default", "acceptEdits", "plan", "bypassPermissions"]
```

**Agent definition schema:**
```python
@dataclass
class AgentDefinition:
    description: str
    prompt: str
    tools: list[str] | None = None
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None
    skills: list[str] | None = None
    memory: Literal["user", "project", "local"] | None = None
    mcpServers: list[str | dict[str, Any]] | None = None
```

**Hook lifecycle** — events the SDK can intercept:
- `PreToolUse` / `PostToolUse` / `PostToolUseFailure`
- `UserPromptSubmit`
- `Stop` / `SubagentStop` / `SubagentStart`
- `PreCompact`
- `Notification`
- `PermissionRequest`

This hook system is what powers Claude Code's pre/post tool hooks in `settings.json`. Cowork and GitHub Action are built using this same hook infrastructure.

**Beta features:**
```python
SdkBeta = Literal["context-1m-2025-08-07"]
```
Active beta: 1M context window (as of build date).

**System prompt preset:**
```python
class SystemPromptPreset(TypedDict):
    type: Literal["preset"]
    preset: Literal["claude_code"]
    append: NotRequired[str]
```
Any agent using the SDK can opt into the full Claude Code system prompt with an optional append, which is how Cowork extends Claude Code's base prompt.

---

## 7. Safety Layer Comparison

| Product | Safety depth | Audience |
|---|---|---|
| Claude Code | Minimal — coding security (OWASP) only | Developers |
| Claude Cowork | Full claude.ai product layer | Non-developers / consumers |
| GitHub Action | Medium — capability limitations, no content policy | Developers / CI systems |
| VS Code | None | Developers |

The safety depth directly tracks the expected user sophistication. Cowork (consumer-facing) gets the full claude.ai treatment. Developer tools get minimal safety framing and trust the user.

---

## 8. Customization Surface for Operators

| Product | How operators customize |
|---|---|
| Claude Code | CLAUDE.md files (per-project/global), MCP servers, plugins, settings.json permissions |
| Claude Cowork | CLAUDE.md + same plugin system as Claude Code |
| GitHub Action | `prompt:` input in workflow YAML, `allowed_tools:`, `disallowed_tools:`, `use_commit_signing:` |
| VS Code | Claude Code settings passed through |
| Agent SDK | `AgentDefinition.prompt`, `.tools`, `.model`, `.skills`, `.mcpServers` |

The GitHub Action is the most configuration-friendly for CI/CD workflows — it exposes key behavioral knobs as workflow inputs without requiring file changes to the repo.

---

## 9. Cross-Product Patterns

### Shared infrastructure
All agentic products (Code, Cowork, GitHub Action) share:
- Claude Code binary or subprocess
- MCP tool architecture
- CLAUDE.md for repo-specific instructions
- Hook lifecycle (PreToolUse, PostToolUse, etc.)
- Permission modes (default, acceptEdits, plan, bypassPermissions)

### Differentiation by surface
Each product solves the same core problem (AI-assisted work) but with different constraints:
- **CLI (Code):** Maximize developer power and speed. Minimal friction.
- **Desktop (Cowork):** Consumer safety and product experience. Sandboxed execution.
- **CI/CD (GitHub Action):** Async, unattended. Single comment output channel. Explicit capability boundaries.
- **IDE (VS Code):** Contextual integration. Minimal behavioral change.

### What "Claude Code" means architecturally
The Agent SDK reveals that "Claude Code" is the name for both the CLI product and the behavioral preset (`preset: "claude_code"`). When Cowork says it's "not Claude Code," it's distinguishing product identity while still running the same underlying software.

---

## Summary

| Dimension | Claude Code | Claude Cowork | GitHub Action | VS Code | Agent SDK |
|---|---|---|---|---|---|
| System prompt size | ~112 lines | ~500 lines | Dynamic (TypeScript) | 11 lines | N/A (types) |
| Built on | Standalone | Claude Code | Claude Code | Claude API | Claude Code |
| Target user | Developers | Non-developers | CI/CD systems | Developers | SDK builders |
| Safety depth | Security only | Full consumer | Capability limits | None | N/A |
| Output channel | stdout | stdout | GitHub comment | IDE chat | Programmatic |
| Autonomy | Mid (pause for high-risk) | Mid + VM sandbox | Async/unattended | N/A | Configurable |
| Customization | CLAUDE.md + plugins | Same | Workflow YAML | Claude Code settings | AgentDefinition |
