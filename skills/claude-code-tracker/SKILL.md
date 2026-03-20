---
name: claude-code-tracker
description: Extract and version-track the Claude Code CLI system prompt, settings, and plugins. Use this skill when the user wants to capture or update Claude Code prompt data in their claude-prompts repo, check if Claude Code's system prompt has changed after an update, commit a new version, or update the changelog. Trigger on any mention of "claude code prompt", "claude code version", "track claude code", "update claude-code repo", or "new version of claude code".
---

# Claude Code Tracker

Extracts the Claude Code system prompt (from the installed binary), settings, and installed plugins, commits them to the `claude-prompts` repo, and maintains a changelog.

## What this skill does

1. Gets the installed version via `claude --version`
2. Finds the binary at `~/.local/share/claude/versions/{version}`
3. Extracts system prompt sections from the binary (static JS template literals)
4. Snapshots `~/.claude/settings.json` and installed plugins from `~/.claude/plugins/cache/`
5. Hashes each to detect changes since the last commit
6. Commits changed files with a descriptive message
7. Reads the diff and writes a changelog entry to `claude-code/CHANGELOG.md`

## How the system prompt is stored

Claude Code is a Node.js Single Executable App (SEA) — the JS bundle is embedded directly in the binary at `~/.local/share/claude/versions/{version}`. The system prompt is **not** in any config file; it's constructed at runtime by JS functions in the bundle.

The extraction script finds these functions by name in the binary and pulls the string literal content:

| Function | Section |
|---|---|
| `qrK` | Identity & Behavior |
| `KrK` | System |
| `RrK` | Coding Instructions |
| `$rK` | Executing Actions with Care |
| `zrK` | Tone and Style |
| `jrK` | Output Efficiency |
| `BH7` | Environment (template) |

Dynamic sections injected at runtime (env info, CLAUDE.md, MCP instructions) are **not** captured — they vary per project/session. Template expressions in captured sections show as `{{...}}`.

## Step-by-step workflow

### Step 1: Run the extraction script

```bash
python3 skills/claude-code-tracker/scripts/extract_claude_code.py \
  --repo ~/github/claude-prompts
```

Parse the JSON output: check `status`, `changes`, `diffs`, `version`, `build_time`, `commit_hash`.

- `no_change` → tell user nothing changed, show version + hashes
- `error` → show error and stop
- `updated` → proceed to Step 2

### Step 2: Summarize the diff

Read `diffs` from the output. For each changed file, summarize what changed:

**system-prompt**: What instructions were added, removed, or reworded? Note section names.
**settings**: Model change? New hooks? Plugin enable/disable?
**plugins**: Added or removed plugins?

### Step 3: Update the changelog

Append to `claude-code/CHANGELOG.md` (newest first):

```markdown
## {date} — v{version}

**Commit:** `{commit_hash}`
**Build time:** `{build_time}`
**Prompt hash:** `{prompt_hash}` (was: `{previous_hash}`)

### Summary
{your prose summary}

### Key changes
- {specific change}
- ...

---
```

For the first entry, describe the structure instead of a diff.

### Step 4: Commit the changelog

```bash
git -C ~/github/claude-prompts add claude-code/CHANGELOG.md
git -C ~/github/claude-prompts commit -m "docs(claude-code): update changelog [v{version}]"
```

## Key file locations

| Source | Path |
|---|---|
| Binary | `~/.local/share/claude/versions/{version}` |
| Settings | `~/.claude/settings.json` |
| Plugin cache | `~/.claude/plugins/cache/{marketplace}/{plugin-name}/` |
| Session history | `~/.claude/projects/{slug}/{session-id}.jsonl` |

## Notes

- Build time is in the binary: grep for `BUILD_TIME` in the string table
- The `version` field in session JSONL entries records which Claude Code version wrote that entry
- The system prompt function names (`qrK`, `KrK`, etc.) are minified and **will change** across major rebuilds — if extraction fails on a new version, the function names may need updating in the script
