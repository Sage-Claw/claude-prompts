# Claude VS Code Extension Changelog

---

## 2026-03-27 — v2.1.83–v2.1.86 — no content changes

**Commits:** `b67a6ec`, `5ed220b`, `8b5df7f`, `d04ba90`
**Prompt hash:** `49b99f4335f828b9` (new hash — content unchanged from v2.1.81, hash algorithm differs from prior tracking)

Versions v2.1.83–v2.1.86 had identical VS Code extension context to v2.1.81. The hash differs from the previously recorded value because the new tracking script uses SHA256 while the prior system used a different method.

---

## Initial capture — v1.0.25–v2.1.81

Earlier versions (v1.0.25 through v2.1.81) were captured by a prior tracking setup. See `versions/` directory for snapshots. The VS Code extension context has been stable since at least v2.1.77 (hash `3bfa08a08faa1c6f` in the old system).

### VS Code context structure
The context injected into the system prompt contains two sections:

1. **Code References in Text** — instructs Claude to use markdown link syntax for file references instead of backticks or HTML tags, with relative paths from workspace root.
2. **User Selection Context** — notes that IDE selections are included in the conversation with `ide_selection` tags and may or may not be relevant.

---
