#!/usr/bin/env python3
"""Extract Cowork system prompt from local session files and commit to repo.

Usage:
    python extract_prompt.py [--repo REPO_PATH] [--dry-run] [--app-version VERSION]

    --app-version: Claude for Mac app version string (e.g. "1.1.7464 (2809b6)").
                   Not available in session JSON — must be provided manually.
                   Find it in Claude for Mac → menu bar → Claude → About Claude.

Output (JSON to stdout):
    {
        "status": "updated" | "no_change" | "error",
        "output_path": str,
        "model": str,
        "cowork_version": str | null,
        "app_version": str | null,
        "prompt_hash": str,
        "previous_hash": str | null,
        "commit_hash": str | null,
        "commit_msg": str | null,
        "diff_added": int,
        "diff_removed": int,
        "full_diff": str,
        "date": str,
        "message": str
    }
"""

import json
import glob
import os
import hashlib
import subprocess
import re
import sys
import argparse
from datetime import datetime

SESSIONS_BASE = os.path.expanduser(
    "~/Library/Application Support/Claude/local-agent-mode-sessions"
)
DEFAULT_REPO = os.path.expanduser("~/github/claude-prompts")


def find_sessions(base=SESSIONS_BASE):
    """Find all local session JSON files (local_{uuid}.json pattern)."""
    pattern = os.path.join(base, "*", "*", "local_*.json")
    return glob.glob(pattern)


def get_cowork_version(session_dir):
    """Get cowork-plugin-management version from the session's plugin cache."""
    pattern = os.path.join(
        session_dir, "cowork_plugins", "cache", "*",
        "cowork-plugin-management", "*", ".claude-plugin", "plugin.json"
    )
    for match in glob.glob(pattern):
        parts = match.replace("\\", "/").split("/")
        for i, p in enumerate(parts):
            if p == "cowork-plugin-management" and i + 1 < len(parts):
                candidate = parts[i + 1]
                # Validate looks like a semver
                if re.match(r"^\d+\.\d+", candidate):
                    return candidate
    return None


def hash_prompt(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]


def read_previous_hash(output_path):
    if not os.path.exists(output_path):
        return None
    with open(output_path) as f:
        content = f.read()
    m = re.search(r"prompt-hash:\s*([a-f0-9]+)", content)
    return m.group(1) if m else None


def run_git(args, cwd, check=False):
    return subprocess.run(
        ["git"] + args, cwd=cwd,
        capture_output=True, text=True, check=check
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--app-version", default=None,
                        help="Claude for Mac app version (e.g. '1.1.7464 (2809b6)')")
    args = parser.parse_args()

    repo_path = os.path.expanduser(args.repo)
    output_path = os.path.join(repo_path, "cowork", "system-prompt.md")
    app_version = args.app_version

    # --- Find & load sessions ---
    sessions = find_sessions()
    if not sessions:
        result = {"status": "error", "message": "No session files found at " + SESSIONS_BASE}
        print(json.dumps(result))
        sys.exit(1)

    loaded = []
    for path in sessions:
        try:
            with open(path) as f:
                data = json.load(f)
            if "systemPrompt" in data:
                loaded.append((data, path))
        except Exception as e:
            sys.stderr.write(f"Skipping {path}: {e}\n")

    if not loaded:
        result = {"status": "error", "message": "No sessions with systemPrompt found"}
        print(json.dumps(result))
        sys.exit(1)

    # Most recent by lastActivityAt
    loaded.sort(key=lambda x: x[0].get("lastActivityAt", 0), reverse=True)
    data, path = loaded[0]

    system_prompt = data["systemPrompt"]
    model = data.get("model", "unknown")
    session_id = data.get("sessionId", "unknown")
    session_dir = os.path.dirname(path)
    cowork_version = get_cowork_version(session_dir)
    prompt_hash = hash_prompt(system_prompt)
    date_str = datetime.now().strftime("%Y-%m-%d")
    previous_hash = read_previous_hash(output_path)

    if previous_hash == prompt_hash:
        result = {
            "status": "no_change",
            "message": f"System prompt unchanged (hash: {prompt_hash})",
            "prompt_hash": prompt_hash,
            "model": model,
            "cowork_version": cowork_version,
            "output_path": output_path,
            "date": date_str,
        }
        print(json.dumps(result))
        return

    # --- Write the prompt file ---
    version_label = f"v{cowork_version}" if cowork_version else model
    app_version_line = f"app-version: {app_version}\n" if app_version else ""
    app_version_row = f"| Claude for Mac | `{app_version}` |\n" if app_version else ""
    content = f"""---
extracted: {date_str}
model: {model}
cowork-version: {cowork_version or "unknown"}
{app_version_line}prompt-hash: {prompt_hash}
source-session: {session_id}
---

# Cowork System Prompt

| Field | Value |
|---|---|
| Extracted | {date_str} |
| Model | `{model}` |
| Cowork plugin version | `{version_label}` |
{app_version_row}| Prompt hash | `{prompt_hash}` |
| Source session | `{session_id}` |

---

```
{system_prompt}
```
"""

    if not args.dry_run:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(content)

    # --- Diff ---
    diff_result = run_git(["diff", "cowork/system-prompt.md"], cwd=repo_path)
    full_diff = diff_result.stdout

    # Count changed lines (exclude file headers)
    added = sum(1 for l in full_diff.splitlines()
                if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in full_diff.splitlines()
                  if l.startswith("-") and not l.startswith("---"))

    if args.dry_run:
        result = {
            "status": "dry_run",
            "message": "Would write and commit (dry run)",
            "output_path": output_path,
            "model": model,
            "cowork_version": cowork_version,
            "prompt_hash": prompt_hash,
            "previous_hash": previous_hash,
            "diff_added": added,
            "diff_removed": removed,
            "full_diff": full_diff,
            "date": date_str,
        }
        print(json.dumps(result))
        return

    # --- Git commit ---
    run_git(["add", "cowork/system-prompt.md"], cwd=repo_path)

    is_first = not run_git(["log", "--oneline", "-1"], cwd=repo_path).stdout.strip()
    if is_first or previous_hash is None:
        commit_msg = f"chore(cowork): add initial system prompt [{version_label}]"
    else:
        commit_msg = f"chore(cowork): update system prompt [{version_label}] ({prompt_hash[:8]})"

    commit_result = run_git(["commit", "-m", commit_msg], cwd=repo_path)
    if commit_result.returncode != 0:
        result = {
            "status": "error",
            "message": f"git commit failed: {commit_result.stderr.strip()}",
        }
        print(json.dumps(result))
        sys.exit(1)

    # Get commit hash
    log_result = run_git(["log", "--oneline", "-1"], cwd=repo_path)
    commit_hash = log_result.stdout.split()[0] if log_result.stdout else "unknown"

    result = {
        "status": "updated",
        "message": f"Committed system prompt update [{version_label}]",
        "output_path": output_path,
        "model": model,
        "cowork_version": cowork_version,
        "app_version": app_version,
        "prompt_hash": prompt_hash,
        "previous_hash": previous_hash,
        "commit_hash": commit_hash,
        "commit_msg": commit_msg,
        "diff_added": added,
        "diff_removed": removed,
        "full_diff": full_diff,
        "date": date_str,
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
