# Claude GitHub Action Changelog

---

## 2026-03-27 — v1.0.78–v1.0.81 — no content changes

**Commits:** `e617f3d`, `0f30cfd`, `8655b5d`, `7cd31af`
**Files:** identical to v1.0.77

Versions v1.0.78–v1.0.81 had no content changes to either `action.yml` or `create-prompt.ts`.

---

## 2026-03-23 — v1.0.77

**Commit:** `293fb27`
**Published:** 2026-03-23
**Files:** `action.yml` (321 lines), `create-prompt.ts` (991 lines, unchanged from v1.0.76)

### Summary
Only `action.yml` changed. The `allowed_non_write_users` input description was expanded with a new security warning about prompt injection risk when processing untrusted content, and a new `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` environment variable was added to the action's env block to scrub secrets from subprocess environments when this input is set.

### Key changes
- `allowed_non_write_users`: description expanded to multi-line YAML, added security warning: "Processing untrusted content exposes the workflow to prompt injection. When this input is set, Claude does a best-effort scrub of Anthropic, cloud, and GitHub Actions secrets from subprocess environments."
- Added `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: ${{ env.CLAUDE_CODE_SUBPROCESS_ENV_SCRUB || (inputs.allowed_non_write_users != '' && '1') || '' }}` to the action's env block
- `create-prompt.ts`: no content change (hash discrepancy due to SHA256 vs MD5 migration in tracking script)

---
