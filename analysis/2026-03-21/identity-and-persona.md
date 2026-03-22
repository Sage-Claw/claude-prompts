# Identity & Persona — 2026-03-21

How each agent defines itself and frames its role to the model.

---

## Claude Code (v2.1.80)

```
You are Claude Code, Anthropic's official CLI for Claude.
```

One sentence. No expertise claims, no backstory. The identity is purely relational — defined by the product it is, not a persona it performs. The rest of the prompt is behavioral rules, not character.

---

## Claude Cowork (v0.2.2)

```
Claude is powering Cowork mode, a feature of the Claude desktop app. Cowork mode is
currently a research preview. Claude is implemented on top of Claude Code and the Claude
Agent SDK, but Claude is NOT Claude Code and should not refer to itself as such. Claude
runs in a lightweight Linux VM on the user's computer...
```

Notable for what it explicitly forbids: don't say you're Claude Code, don't mention the VM, don't mention implementation details unless relevant. The identity is defined by contrast and concealment — a product identity over a technical one.

---

## OpenAI Codex (rust-v0.117.0-alpha.8)

```
You are a coding agent running in the Codex CLI, a terminal-based coding assistant.
Codex CLI is an open source project led by OpenAI. You are expected to be precise, safe,
and helpful.
```

Three adjectives as the core personality spec: precise, safe, helpful. Mentions open-source provenance. The rest of the identity is implied by capability sections rather than stated.

---

## Cline (v3.75.0)

```
You are Cline, a highly skilled software engineer with extensive knowledge in many
programming languages, frameworks, design patterns, and best practices.
```

Most elaborate persona framing of any agent: claims expertise in languages, frameworks, design patterns, and best practices. This is aspirational — it sets a bar for how the model should reason and respond, not just what product it is.

---

## Aider (v0.86.2)

No identity statement. The closest thing is the mode-specific opener in `editblock_prompts.py`:

```python
main_system = """Act as an expert software developer.
Always use best practices when coding.
Respect and use existing conventions, libraries, etc that are already present in the code base.
```

Role is entirely implied by behavioral instructions. There's no named persona — "aider" is the CLI command, not a character in the prompt.

---

## Goose (v1.28.0)

```
You are a general-purpose AI agent called goose, created by Block, the parent company
of Square, CashApp, and Tidal. goose is being developed as an open-source software project.
```

Unique for including corporate lineage (Block, Square, CashApp, Tidal) and emphasizing open-source development. This grounds the agent in a specific company identity rather than just a product. The name is lowercase ("goose") throughout — deliberate de-emphasis of the agent as a capital-I "Intelligence."

---

## Claude VS Code (v2.0.12)

No identity statement whatsoever. The entire prompt is operational guidance about link formatting:

```
You are running inside a VSCode native extension environment.

## Code References in Text
IMPORTANT: When referencing files or code locations, use markdown link syntax...
```

The VS Code extension adds a thin context layer, not a persona.

---

## Patterns

**Named persona vs. functional role:** Cline and Goose give the agent a named character. Claude Code, Cowork, and Codex define a functional role. Aider has neither.

**Expertise claims:** Cline makes the strongest explicit expertise claim ("highly skilled software engineer"). Codex uses adjectives (precise, safe, helpful). Aider uses imperatives ("act as an expert"). Claude Code/Cowork/Goose make no expertise claims.

**Corporate attribution:** Goose is the most explicit about its corporate origin (Block/Square/CashApp). Claude Code and Cowork mention Anthropic but don't build identity around it. OpenAI Codex mentions OpenAI once. Cline and Aider are vendor-neutral.

**Concealment vs. transparency:** Cowork explicitly instructs the model to hide implementation details (Claude Code, Agent SDK, VM). No other agent does this.
