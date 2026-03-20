#!/usr/bin/env python3
"""Extract Cowork session data from local session files and commit to repo.

Tracks: system prompt, slash commands, MCP tools, egress domains.

Usage:
    python extract_prompt.py [--repo REPO_PATH] [--dry-run] [--app-version VERSION]

    --app-version: Claude for Mac app version string (e.g. "1.1.7464 (2809b6)").
                   Auto-detected from /Applications/Claude.app if not provided.

Output (JSON to stdout):
    {
        "status": "updated" | "no_change" | "error",
        "model": str,
        "cowork_version": str | null,
        "app_version": str | null,
        "prompt_hash": str,
        "previous_hash": str | null,
        "commit_hash": str | null,
        "commit_msg": str | null,
        "changes": { "system_prompt": bool, "slash_commands": bool, "mcp_tools": bool, "egress_domains": bool },
        "diffs": { "system_prompt": str, "slash_commands": str, "mcp_tools": str, "egress_domains": str },
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
CLAUDE_APP = "/Applications/Claude.app"


# ── Brew update check ──────────────────────────────────────────────────────────

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def get_brew_versions():
    """Return (installed, latest) version strings from `brew info --cask claude`.
    Returns (None, None) if brew or the cask isn't available."""
    r = run(["brew", "info", "--cask", "claude", "--json=v2"])
    if r.returncode != 0:
        return None, None
    try:
        data = json.loads(r.stdout)
        casks = data.get("casks", [])
        if not casks:
            return None, None
        cask = casks[0]
        latest = cask.get("version")
        installed_list = cask.get("installed")  # list of installed version dicts or None
        if installed_list:
            installed = installed_list[0].get("version") if isinstance(installed_list[0], dict) else installed_list[0]
        else:
            installed = None
        return installed, latest
    except Exception:
        return None, None


def brew_upgrade_claude():
    """Run `brew upgrade --cask claude`. Returns (success, output)."""
    r = run(["brew", "upgrade", "--cask", "claude"])
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def detect_app_version():
    """Auto-detect Claude for Mac version from the app bundle."""
    try:
        import plistlib
        plist_path = os.path.join(CLAUDE_APP, "Contents", "Info.plist")
        with open(plist_path, "rb") as f:
            info = plistlib.load(f)
        version = info.get("CFBundleShortVersionString") or info.get("CFBundleVersion")
        if not version:
            return None
        version_txt = os.path.join(CLAUDE_APP, "Contents", "Resources", "claude-ssh", "version.txt")
        if os.path.exists(version_txt):
            with open(version_txt) as f:
                full_hash = f.read().strip()
            short_hash = full_hash[:7] if len(full_hash) >= 7 else full_hash
            return f"{version} ({short_hash})"
        return version
    except Exception:
        return None


def find_sessions(base=SESSIONS_BASE):
    pattern = os.path.join(base, "*", "*", "local_*.json")
    return glob.glob(pattern)


def get_cowork_version(session_dir):
    pattern = os.path.join(
        session_dir, "cowork_plugins", "cache", "*",
        "cowork-plugin-management", "*", ".claude-plugin", "plugin.json"
    )
    for match in glob.glob(pattern):
        parts = match.replace("\\", "/").split("/")
        for i, p in enumerate(parts):
            if p == "cowork-plugin-management" and i + 1 < len(parts):
                candidate = parts[i + 1]
                if re.match(r"^\d+\.\d+", candidate):
                    return candidate
    return None


def sha16(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def read_frontmatter_field(path, field):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()
    m = re.search(rf"^{field}:\s*(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None


def run_git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def frontmatter(date_str, model, cowork_version, app_version, extra=""):
    av = f"app-version: {app_version}\n" if app_version else ""
    return f"---\nextracted: {date_str}\napp-version: {app_version or 'unknown'}\ncowork-version: {cowork_version or 'unknown'}\nmodel: {model}\n{extra}---\n\n"


# ── Writers ────────────────────────────────────────────────────────────────────

def write_system_prompt(data, path, date_str, model, cowork_version, app_version):
    system_prompt = data["systemPrompt"]
    session_id = data.get("sessionId", "unknown")
    prompt_hash = sha16(system_prompt)
    version_label = f"v{cowork_version}" if cowork_version else model
    app_row = f"| Claude for Mac | `{app_version}` |\n" if app_version else ""
    content = (
        frontmatter(date_str, model, cowork_version, app_version,
                    extra=f"prompt-hash: {prompt_hash}\nsource-session: {session_id}\n")
        + f"# Cowork System Prompt\n\n"
        + f"| Field | Value |\n|---|---|\n"
        + f"| Extracted | {date_str} |\n"
        + f"| Model | `{model}` |\n"
        + f"| Cowork plugin version | `{version_label}` |\n"
        + app_row
        + f"| Prompt hash | `{prompt_hash}` |\n"
        + f"| Source session | `{session_id}` |\n\n---\n\n```\n{system_prompt}\n```\n"
    )
    with open(path, "w") as f:
        f.write(content)
    return prompt_hash


def write_slash_commands(data, path, date_str, model, cowork_version, app_version):
    commands = sorted(data.get("slashCommands", []))
    lines = frontmatter(date_str, model, cowork_version, app_version,
                        extra=f"count: {len(commands)}\n")
    for cmd in commands:
        lines += f"- `{cmd}`\n"
    with open(path, "w") as f:
        f.write(lines)
    return sha16("\n".join(commands))


def write_mcp_tools(data, path, date_str, model, cowork_version, app_version):
    tools = data.get("enabledMcpTools", {})
    stable_keys = sorted(
        re.sub(r"-[a-f0-9]{32}$", "-{hash}", k) for k in tools.keys()
    )
    content_hash = sha16("\n".join(stable_keys))
    lines = frontmatter(date_str, model, cowork_version, app_version,
                        extra=f"count: {len(tools)}\n")
    for key in sorted(tools.keys()):
        lines += f"- `{key}`\n"
    with open(path, "w") as f:
        f.write(lines)
    return content_hash


def write_egress_domains(data, path, date_str, model, cowork_version, app_version):
    domains = sorted(data.get("egressAllowedDomains", []))
    content_hash = sha16("\n".join(domains))
    lines = frontmatter(date_str, model, cowork_version, app_version,
                        extra=f"count: {len(domains)}\n")
    for d in domains:
        lines += f"- `{d}`\n"

    with open(path, "w") as f:
        f.write(lines)
    return content_hash


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--app-version", default=None)
    parser.add_argument("--no-upgrade", action="store_true",
                        help="Skip the brew upgrade check")
    args = parser.parse_args()

    repo_path = os.path.expanduser(args.repo)
    cowork_dir = os.path.join(repo_path, "cowork")

    # --- Step 0: check for a newer Claude app via brew and upgrade if available ---
    upgrade_info = {}
    if not args.no_upgrade:
        installed_ver, latest_ver = get_brew_versions()
        if installed_ver and latest_ver and installed_ver != latest_ver:
            success, output = brew_upgrade_claude()
            upgrade_info = {
                "upgraded": success,
                "from": installed_ver,
                "to": latest_ver,
                "output": output,
            }
            if not success:
                sys.stderr.write(f"brew upgrade failed: {output}\n")
        elif installed_ver:
            upgrade_info = {"upgraded": False, "installed": installed_ver, "latest": latest_ver}

    app_version = args.app_version or detect_app_version()

    # --- Find most recent session ---
    sessions = find_sessions()
    if not sessions:
        print(json.dumps({"status": "error", "message": "No session files found at " + SESSIONS_BASE}))
        sys.exit(1)

    loaded = []
    for p in sessions:
        try:
            with open(p) as f:
                d = json.load(f)
            if "systemPrompt" in d:
                loaded.append((d, p))
        except Exception as e:
            sys.stderr.write(f"Skipping {p}: {e}\n")

    if not loaded:
        print(json.dumps({"status": "error", "message": "No sessions with systemPrompt found"}))
        sys.exit(1)

    loaded.sort(key=lambda x: x[0].get("lastActivityAt", 0), reverse=True)
    data, session_path = loaded[0]

    model = data.get("model", "unknown")
    session_dir = os.path.dirname(session_path)
    cowork_version = get_cowork_version(session_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")

    # File paths
    files = {
        "system_prompt":  os.path.join(cowork_dir, "system-prompt.md"),
        "slash_commands": os.path.join(cowork_dir, "slash-commands.md"),
        "mcp_tools":      os.path.join(cowork_dir, "mcp-tools.md"),
        "egress_domains": os.path.join(cowork_dir, "egress-domains.md"),
    }

    # Read previous hashes
    prev_hashes = {
        "system_prompt":  read_frontmatter_field(files["system_prompt"], "prompt-hash"),
        "slash_commands": read_frontmatter_field(files["slash_commands"], "content-hash"),
        "mcp_tools":      read_frontmatter_field(files["mcp_tools"], "content-hash"),
        "egress_domains": read_frontmatter_field(files["egress_domains"], "content-hash"),
    }

    if args.dry_run:
        print(json.dumps({"status": "dry_run", "message": "Dry run — no files written",
                          "model": model, "app_version": app_version,
                          "cowork_version": cowork_version, "upgrade": upgrade_info}))
        return

    os.makedirs(cowork_dir, exist_ok=True)

    # Write all files and collect new hashes
    new_hashes = {}
    new_hashes["system_prompt"]  = write_system_prompt(data, files["system_prompt"], date_str, model, cowork_version, app_version)
    new_hashes["slash_commands"] = write_slash_commands(data, files["slash_commands"], date_str, model, cowork_version, app_version)
    new_hashes["mcp_tools"]      = write_mcp_tools(data, files["mcp_tools"], date_str, model, cowork_version, app_version)
    new_hashes["egress_domains"] = write_egress_domains(data, files["egress_domains"], date_str, model, cowork_version, app_version)

    # Detect what changed
    changes = {k: prev_hashes[k] != new_hashes[k] for k in new_hashes}

    if not any(changes.values()):
        print(json.dumps({
            "status": "no_change",
            "message": "Nothing changed",
            "model": model, "app_version": app_version, "cowork_version": cowork_version,
            "prompt_hash": new_hashes["system_prompt"], "date": date_str,
            "upgrade": upgrade_info,
        }))
        return

    # Stage changed files
    file_map = {
        "system_prompt":  "cowork/system-prompt.md",
        "slash_commands": "cowork/slash-commands.md",
        "mcp_tools":      "cowork/mcp-tools.md",
        "egress_domains": "cowork/egress-domains.md",
    }
    diffs = {}
    for key, git_path in file_map.items():
        diffs[key] = run_git(["diff", git_path], cwd=repo_path).stdout
        if changes[key]:
            run_git(["add", git_path], cwd=repo_path)

    version_label = f"v{cowork_version}" if cowork_version else model
    changed_labels = [k.replace("_", "-") for k, v in changes.items() if v]
    is_first = prev_hashes["system_prompt"] is None
    if is_first:
        commit_msg = f"chore(cowork): initial capture [{version_label}]"
    else:
        commit_msg = f"chore(cowork): update {', '.join(changed_labels)} [{version_label}]"

    commit_result = run_git(["commit", "-m", commit_msg], cwd=repo_path)
    if commit_result.returncode != 0:
        print(json.dumps({"status": "error", "message": f"git commit failed: {commit_result.stderr.strip()}"}))
        sys.exit(1)

    commit_hash = run_git(["log", "--oneline", "-1"], cwd=repo_path).stdout.split()[0]

    print(json.dumps({
        "status": "updated",
        "message": commit_msg,
        "model": model,
        "cowork_version": cowork_version,
        "app_version": app_version,
        "prompt_hash": new_hashes["system_prompt"],
        "previous_hash": prev_hashes["system_prompt"],
        "commit_hash": commit_hash,
        "commit_msg": commit_msg,
        "changes": changes,
        "diffs": diffs,
        "date": date_str,
        "upgrade": upgrade_info,
    }))


if __name__ == "__main__":
    main()
