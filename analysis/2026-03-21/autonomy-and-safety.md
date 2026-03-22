# Autonomy & Safety — 2026-03-21

Autonomy levels, approval models, safety constraints, and refusal posture.

---

## Autonomy Spectrum

```
← Human-in-the-loop ─────────────────────── Fully autonomous →

  Aider     Cline     Claude Code    Goose    OpenAI Codex
             ↑            ↑                        ↑
         gate every    pause for              "keep going until
          action       high-stakes             completely resolved"
```

---

## Claude Code

**Default stance:** Autonomous for local/reversible actions, requires confirmation for high-stakes.

Explicit categories requiring user confirmation:
- Destructive ops (rm -rf, reset --hard, drop tables, kill processes)
- Hard-to-reverse ops (force push, amend published commits, remove packages, modify CI/CD)
- Visible-to-others actions (push, PR comments, Slack/email, external service posts)

Key principle: "The cost of pausing to confirm is low, while the cost of an unwanted action can be very high."

Authorization scope is narrow: a user approving one push doesn't authorize all pushes. "Match the scope of your actions to what was actually requested."

---

## Claude Cowork

Same policy as Claude Code, but with lower blast radius by design: the agent runs in a sandboxed Linux VM with access only to a workspace folder. Structural containment supplements policy containment.

Also has an extensive content safety layer inherited from the claude.ai product (see below).

---

## OpenAI Codex

**Default stance:** Maximum autonomy. "Keep going until the query is completely resolved before ending your turn."

Explicit per-run approval modes:
- `never` — autonomous, proactively run tests/lint
- `on-failure` — run validation; stop on failure for user input
- `untrusted` — interactive; suggest next step, let user confirm before finalizing
- `on-request` — interactive; hold off on tests until user is ready

Working on any repo is allowed, even proprietary. Vulnerability analysis is allowed. No destructive action policy stated — the model is trusted to be "precise and safe."

---

## Cline

**Default stance:** Maximum caution. Every tool call requires user response before proceeding.

`execute_command` has a `requires_approval` boolean that can be set per-call:
- `true` — always prompt even in auto-approve mode (for installs, deletes, network ops, config changes)
- `false` — allowed without prompt (reads, dev servers, builds)

"It is critical you wait for the user's response after each tool use, in order to confirm the success of the tool use."

Yolo mode (`yoloModeToggled`) removes the "ask follow-up questions" constraint but doesn't change tool gating.

---

## Aider

**Default stance:** Conversational/collaborative. The human controls what files are in scope.

Autonomy is structurally limited by design: the model can only edit files the user has explicitly added to the chat. If it needs to edit a file, it must ask first. No command execution model.

---

## Goose

**Default stance:** General-purpose agent. Autonomy depends on which extensions/tools are active.

Subagent system adds bounded autonomy:
- Subagents have a `max_turns` limit
- Subagents cannot spawn further subagents
- Each subagent has a specific task scope

---

## Safety & Content Policy

### Claude Cowork — most extensive

Full consumer-grade content layer:
- Child safety (anyone under 18, stricter in some regions)
- Weapons/harmful substances — decline regardless of stated intent or "publicly available" framing
- Malware/exploits — refuse even for "educational" purposes
- Real named public figures — avoid creative content, persuasive fictional quotes
- Mental health: no self-harm techniques (including "harm reduction" substitutes like ice cubes)
- Financial/legal advice: factual only, no confident recommendations
- Ad policy: clarify Anthropic products are ad-free, distinguish from third-party builds
- No suicide/self-harm resources unless asked; note sensitivity

### Claude Code

Security-focused but no content policy:
- OWASP top 10 awareness (XSS, SQL injection, command injection)
- Fix security vulnerabilities immediately if introduced
- No broader content safety layer — assumes developer audience

### OpenAI Codex

Minimal but explicit:
- Working on proprietary repos: allowed
- Vulnerability analysis: allowed
- Showing code/tool details: allowed

Implied refusal: harmful commands in tool calls would be caught by the model's base training.

### Cline

One explicit security rule:
- Quote variable text with `--` separator to prevent argument injection (`my-cli -- "$value"`)

No content policy.

### Aider, Goose, Claude VS Code

No explicit safety or refusal policy. Entirely model-default behavior.

---

## Summary

| Agent | Autonomy default | Gate mechanism | Content policy depth |
|---|---|---|---|
| Claude Code | Mid — pause for high-stakes | In-prompt policy | None (security-focused only) |
| Claude Cowork | Mid — pause for high-stakes | In-prompt policy + VM sandbox | Extensive (consumer-grade) |
| OpenAI Codex | High — complete before yielding | Approval mode per run | Minimal |
| Cline | Low — gate every action | Per-tool `requires_approval` flag | None |
| Aider | Lowest — user controls scope | User adds files to chat | None |
| Goose | Variable — extension-dependent | Extension + subagent bounds | None in base prompt |
| Claude VS Code | N/A | N/A | None |
