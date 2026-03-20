---
name: cowork-prompt-tracker
description: Extract and version-track the Claude Cowork system prompt. Use this skill when the user wants to capture or update the Cowork system prompt in their claude-prompts repo, check if Cowork's system prompt has changed, commit a new version, or update the changelog with a diff summary. Trigger on any mention of "cowork prompt", "system prompt", "track changes", "update the repo", or "new version of cowork".
---

# Cowork Prompt Tracker

Extracts the Claude Cowork system prompt from local session files, commits it to the `claude-prompts` repo, and maintains a changelog with diff summaries.

## What this skill does

1. Finds the most recent Cowork session file and extracts the `systemPrompt` field
2. Detects the Cowork plugin version (from `cowork-plugin-management` in the session's plugin cache)
3. Hashes the prompt to check if it changed since the last commit
4. Writes `cowork/system-prompt.md` to the repo with metadata header
5. Commits it with a descriptive message
6. Reads the diff and writes a changelog entry to `cowork/CHANGELOG.md`

## Session file locations

- **macOS:** `~/Library/Application Support/Claude/local-agent-mode-sessions/{uuid}/{uuid}/local_{uuid}.json`
- **Windows:** `~\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\{uuid}\{uuid}\local_{uuid}.json`

The script handles macOS automatically. For Windows, the user will need to run it in WSL or adapt the path.

## Step-by-step workflow

### Step 1: Run the extraction script

```bash
python3 skills/cowork-prompt-tracker/scripts/extract_prompt.py \
  --repo ~/github/claude-prompts \
  --app-version "1.1.7464 (2809b6)"   # Claude for Mac version — update each run
```

`--app-version` is not in the session JSON. Find it at **Claude for Mac → menu bar → Claude → About Claude**. Ask the user for it before running if they haven't provided it.

The script outputs JSON. Parse it to get `status`, `full_diff`, `diff_added`, `diff_removed`, `model`, `cowork_version`, `app_version`, `commit_hash`, `previous_hash`, and `prompt_hash`.

If `status == "no_change"`: tell the user nothing changed and show the current hash.
If `status == "error"`: show the error message and stop.
If `status == "updated"`: proceed to Step 2.

### Step 2: Read and summarize the diff

Read `full_diff` from the JSON output. Produce a human-readable summary of what changed:
- New sections added
- Sections removed or renamed
- Modified instructions (tone changes, new rules, updated tool references)
- Model name changes
- Version bumps

Be specific — "the `<computer_use>` section added a new paragraph about X" is more useful than "some text changed". If there's no previous version (first commit), describe the structure of the prompt instead.

### Step 3: Update the changelog

Append a new entry to `cowork/CHANGELOG.md` (create the file if it doesn't exist, with a `# Changelog` header). Entries go at the top, newest first.

Use this format:

```markdown
## {date} — {version_label} (model: {model})

**Commit:** `{commit_hash}`
**Changes:** +{added} lines, -{removed} lines
**Prompt hash:** `{prompt_hash}` (was: `{previous_hash}`)

### Summary
{your diff summary in prose — 2–5 sentences}

### Key changes
- {specific change 1}
- {specific change 2}
- ...

---
```

Where `{version_label}` is `v{cowork_version}` if available, else just `{model}`.

If this is the **first entry** (no previous hash), write:

```markdown
## {date} — {version_label} — Initial capture

**Commit:** `{commit_hash}`
**Prompt hash:** `{prompt_hash}`

### Summary
First capture of the Cowork system prompt. {brief structural description}

---
```

### Step 4: Commit the changelog

```bash
git -C ~/github/claude-prompts add cowork/CHANGELOG.md
git -C ~/github/claude-prompts commit -m "docs(cowork): update changelog [{version_label}]"
```

Then tell the user what happened: the version detected, what changed (your summary), and the two commit hashes.

## Repo path

Default: `~/github/claude-prompts`. If the user has a different location, pass it via `--repo`.

## Notes

- The script scrubs nothing — the raw `systemPrompt` is a template with `{{placeholder}}` variables, not actual PII. The session file itself has `accountName`/`emailAddress` but the script only extracts `systemPrompt`.
- "Version" of Cowork = the `cowork-plugin-management` semver found in the session's plugin cache (e.g., `0.2.2`). This is the most reliable version signal available.
- If no version is detected, fall back to the model name as the version label.
- Sessions are sorted by `lastActivityAt` to pick the most recent one.
