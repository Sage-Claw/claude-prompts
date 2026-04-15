#!/usr/bin/env python3
"""Extract and track Claude Code CLI system prompt, settings, and plugins.

Sources:
  - Binary:  ~/.local/share/claude/versions/{version}  (system prompt sections, build time)
  - CLI:     claude --version
  - Config:  ~/.claude/settings.json
  - Plugins: ~/.claude/plugins/cache/

Usage:
    python extract_claude_code.py [--repo REPO_PATH] [--dry-run]

Output: JSON to stdout with status and diff info.
"""

import json, glob, os, re, hashlib, subprocess, sys, argparse
from datetime import datetime
from pathlib import Path

DEFAULT_REPO = os.path.expanduser("~/github/claude-prompts")
VERSIONS_DIR = os.path.expanduser("~/.local/share/claude/versions")
SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")
PLUGINS_CACHE = os.path.expanduser("~/.claude/plugins/cache")

# System prompt section functions to extract from binary
# v2.1.87  (2026-03-30): LD/_yz/Yyz/zyz/jyz/wyz/Jyz
# v2.1.86+ (2026-03-27): qJ/UYK/QYK/lYK/aYK/oYK/tYK
# v2.1.80  (2026-03-17): qrK/KrK/RrK/$rK/zrK/jrK/BH7
SECTIONS_BY_VERSION = {
    "2.1.87": [
        ("identity",    b"async function LD("),
        ("system",      b"function _yz("),
        ("coding",      b"function Yyz("),
        ("safety",      b"function zyz("),
        ("tone",        b"function jyz("),
        ("efficiency",  b"function wyz("),
        ("env",         b"async function Jyz("),
    ],
    "default": [
        ("identity",    b"async function qJ("),
        ("system",      b"function UYK("),
        ("coding",      b"function QYK("),
        ("safety",      b"function lYK("),
        ("tone",        b"function aYK("),
        ("efficiency",  b"function oYK("),
        ("env",         b"async function tYK("),
    ],
}

def get_sections(version):
    return SECTIONS_BY_VERSION.get(version, SECTIONS_BY_VERSION["default"])

SECTIONS = SECTIONS_BY_VERSION["default"]  # fallback for compatibility


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def sha16(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]

def read_frontmatter_field(path, field):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()
    m = re.search(rf"^{field}:\s*(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None

def run_git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)

def frontmatter(date_str, version, build_time, extra=""):
    return (f"---\nextracted: {date_str}\nversion: {version}\n"
            f"build-time: {build_time or 'unknown'}\n{extra}---\n\n")


# ── Detection ─────────────────────────────────────────────────────────────────

def get_version():
    r = run(["claude", "--version"])
    m = re.search(r"([\d]+\.[\d]+\.[\d]+)", r.stdout)
    return m.group(1) if m else r.stdout.strip()

def get_binary_path(version):
    p = os.path.join(VERSIONS_DIR, version)
    return p if os.path.exists(p) else None

def get_build_time(binary_path):
    """Extract BUILD_TIME from the binary."""
    r = run(["strings", "-n", "20", binary_path])
    for line in r.stdout.split("\n"):
        m = re.search(r'BUILD_TIME["\s:]+(\d{4}-\d{2}-\d{2}T[\d:\.]+Z)', line)
        if m:
            return m.group(1)
    return None


# ── System prompt extraction ──────────────────────────────────────────────────

def extract_strings_from_chunk(chunk, min_len=40):
    """Pull readable string literals out of a chunk of minified JS."""
    texts = []
    i = 0
    while i < len(chunk):
        if chunk[i] in ('"', "'", "`"):
            delim = chunk[i]
            j = i + 1
            buf = []
            while j < len(chunk):
                if chunk[j] == "\\" and j + 1 < len(chunk):
                    # Handle common escapes
                    esc = chunk[j + 1]
                    if esc == "n":   buf.append("\n")
                    elif esc == "t": buf.append("\t")
                    elif esc == "u" and j + 5 < len(chunk):
                        try:
                            cp = int(chunk[j+2:j+6], 16)
                            buf.append(chr(cp))
                            j += 4
                        except ValueError:
                            buf.append(chunk[j+1])
                    else:
                        buf.append(esc)
                    j += 2
                    continue
                if chunk[j] == delim:
                    break
                # Stop template literal expressions
                if delim == "`" and chunk[j] == "$" and j + 1 < len(chunk) and chunk[j+1] == "{":
                    buf.append("{{...}}")
                    # Skip to closing }
                    depth = 1
                    j += 2
                    while j < len(chunk) and depth > 0:
                        if chunk[j] == "{": depth += 1
                        elif chunk[j] == "}": depth -= 1
                        j += 1
                    continue
                buf.append(chunk[j])
                j += 1
            text = "".join(buf).strip()
            # Keep if it looks like natural language (has spaces, reasonable length)
            if (len(text) >= min_len and " " in text
                    and not text.startswith("function ")
                    and not re.match(r"^[a-zA-Z_$][a-zA-Z0-9_$]*\(", text)
                    and "\n" not in text[:20] or len(text) > 200):
                texts.append(text)
            i = j + 1
        else:
            i += 1
    return texts


def extract_section(binary_data, func_marker, window=12000):
    """Extract readable text from a named function in the binary."""
    idx = binary_data.find(func_marker)
    if idx < 0:
        return None
    chunk = binary_data[idx:idx + window].decode("latin-1", errors="replace")
    texts = extract_strings_from_chunk(chunk)
    if not texts:
        return None
    return "\n\n".join(texts)


def extract_system_prompt(binary_path, version=None):
    """Extract all system prompt sections from the binary."""
    with open(binary_path, "rb") as f:
        data = f.read()

    # Try version-specific markers first, fall back to default
    section_list = get_sections(version) if version else SECTIONS
    sections = {}
    for name, marker in section_list:
        text = extract_section(data, marker)
        if text:
            sections[name] = text

    # If version-specific markers found nothing, try default
    if not sections and version and version in SECTIONS_BY_VERSION:
        for name, marker in SECTIONS_BY_VERSION["default"]:
            text = extract_section(data, marker)
            if text:
                sections[name] = text

    return sections


# ── Writers ───────────────────────────────────────────────────────────────────

def write_system_prompt(sections, path, date_str, version, build_time):
    prompt_hash = sha16("\n".join(sections.values()))
    header = frontmatter(date_str, version, build_time,
                         extra=f"prompt-hash: {prompt_hash}\n")

    parts = [header, "# Claude Code System Prompt\n",
             f"> Extracted from binary `{version}` (build: `{build_time}`)\n",
             f"> Prompt hash: `{prompt_hash}`\n",
             "> Dynamic sections (env info, CLAUDE.md, MCP instructions) are injected at runtime and not captured here.\n",
             "> Template expression placeholders shown as `{{...}}`.\n\n---\n"]

    section_titles = {
        "identity":   "Identity & Behavior",
        "system":     "System",
        "coding":     "Coding Instructions",
        "safety":     "Executing Actions with Care",
        "tone":       "Tone and Style",
        "efficiency": "Output Efficiency",
        "env":        "Environment (template)",
    }
    for name, text in sections.items():
        title = section_titles.get(name, name.title())
        parts.append(f"## {title}\n\n{text}\n\n---\n")

    with open(path, "w") as f:
        f.write("\n".join(parts))
    return prompt_hash


def write_settings(path, date_str, version, build_time):
    try:
        with open(SETTINGS_PATH) as f:
            settings = json.load(f)
    except Exception as e:
        settings = {"error": str(e)}

    # Scrub PII-adjacent paths but keep structure
    content_hash = sha16(json.dumps(settings, sort_keys=True))
    fm = frontmatter(date_str, version, build_time,
                     extra=f"content-hash: {content_hash}\n")
    with open(path, "w") as f:
        f.write(fm + "# Claude Code Settings\n\n")
        f.write("```json\n" + json.dumps(settings, indent=2) + "\n```\n")
    return content_hash


def write_plugins(path, date_str, version, build_time):
    plugins = []
    if os.path.isdir(PLUGINS_CACHE):
        for marketplace in sorted(os.listdir(PLUGINS_CACHE)):
            mp_dir = os.path.join(PLUGINS_CACHE, marketplace)
            if os.path.isdir(mp_dir):
                for plugin in sorted(os.listdir(mp_dir)):
                    plugins.append(f"{plugin}@{marketplace}")

    content_hash = sha16("\n".join(plugins))
    fm = frontmatter(date_str, version, build_time,
                     extra=f"count: {len(plugins)}\ncontent-hash: {content_hash}\n")
    with open(path, "w") as f:
        f.write(fm)
        for p in plugins:
            f.write(f"- `{p}`\n")
    return content_hash


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_path = os.path.expanduser(args.repo)
    out_dir = os.path.join(repo_path, "claude-code")
    date_str = datetime.now().strftime("%Y-%m-%d")

    version = get_version()
    binary_path = get_binary_path(version)
    build_time = get_build_time(binary_path) if binary_path else None
    binary_hash = sha256_file(binary_path) if binary_path else None

    files = {
        "system_prompt": os.path.join(out_dir, "system-prompt.md"),
        "plugins":       os.path.join(out_dir, "plugins.md"),
    }

    prev_hashes = {
        "system_prompt": read_frontmatter_field(files["system_prompt"], "prompt-hash"),
        "plugins":       read_frontmatter_field(files["plugins"], "content-hash"),
    }

    if args.dry_run:
        print(json.dumps({"status": "dry_run", "version": version,
                          "build_time": build_time, "binary_hash": binary_hash}))
        return

    os.makedirs(out_dir, exist_ok=True)

    # Extract and write
    sections = extract_system_prompt(binary_path, version=version) if binary_path else {}
    new_hashes = {
        "system_prompt": write_system_prompt(sections, files["system_prompt"], date_str, version, build_time),
        "plugins":       write_plugins(files["plugins"], date_str, version, build_time),
    }

    changes = {k: prev_hashes[k] != new_hashes[k] for k in new_hashes}

    if not any(changes.values()):
        print(json.dumps({"status": "no_change", "version": version,
                          "build_time": build_time, "message": "Nothing changed"}))
        return

    # Collect diffs and stage
    file_map = {
        "system_prompt": "claude-code/system-prompt.md",
        "plugins":       "claude-code/plugins.md",
    }
    diffs = {}
    for key, git_path in file_map.items():
        diffs[key] = run_git(["diff", git_path], cwd=repo_path).stdout
        if changes[key]:
            run_git(["add", git_path], cwd=repo_path)

    changed_labels = [k.replace("_", "-") for k, v in changes.items() if v]
    is_first = prev_hashes["system_prompt"] is None
    commit_msg = (f"chore(claude-code): initial capture [v{version}]" if is_first
                  else f"chore(claude-code): update {', '.join(changed_labels)} [v{version}]")

    commit_result = run_git(["commit", "-m", commit_msg], cwd=repo_path)
    if commit_result.returncode != 0:
        print(json.dumps({"status": "error",
                          "message": f"git commit failed: {commit_result.stderr.strip()}"}))
        sys.exit(1)

    commit_hash = run_git(["log", "--oneline", "-1"], cwd=repo_path).stdout.split()[0]

    print(json.dumps({
        "status": "updated",
        "message": commit_msg,
        "version": version,
        "build_time": build_time,
        "binary_hash": binary_hash,
        "changes": changes,
        "diffs": diffs,
        "commit_hash": commit_hash,
        "commit_msg": commit_msg,
        "date": date_str,
    }))


if __name__ == "__main__":
    main()
