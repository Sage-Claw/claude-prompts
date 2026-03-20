# Claude Code Session JSONL Schema

Session history files are at:
`~/.claude/projects/{slug}/{session-id}.jsonl`

Where `{slug}` is the project path with `/` replaced by `-` (e.g. `-Users-alice-myproject`).

## Entry types

| `type` | Description |
|---|---|
| `progress` | Tool execution progress updates |
| `user` | User message turn |
| `assistant` | Assistant message turn |
| `last-prompt` | Metadata about the most recent prompt |
| `queue-operation` | Internal queue enqueue/dequeue events |

## Common fields (all entries)

| Field | Type | Notes |
|---|---|---|
| `type` | string | Entry type (see above) |
| `uuid` | string | UUID for this entry |
| `parentUuid` | string \| null | UUID of parent entry |
| `timestamp` | string | ISO 8601 |
| `sessionId` | string | Session UUID |
| `version` | string | Claude Code version that wrote this entry (e.g. `"2.1.80"`) |
| `cwd` | string | Working directory when entry was written |
| `gitBranch` | string \| null | Current git branch |
| `userType` | string | `"external"` or similar |
| `entrypoint` | string | How the session was started (e.g. `"cli"`) |
| `isSidechain` | boolean | Whether this is a sidechain (subagent) message |
| `slug` | string | Project slug |

## `user` entry fields

| Field | Type | Notes |
|---|---|---|
| `message` | object | `{ role: "user", content: string \| ContentBlock[] }` |

## `assistant` entry fields

| Field | Type | Notes |
|---|---|---|
| `message` | object | `{ role: "assistant", content: ContentBlock[], model, usage, stop_reason, ... }` |
| `toolUseResult` | object \| null | Result of tool use if this is a tool result |
| `sourceToolAssistantUUID` | string \| null | UUID of assistant that called the tool |
| `promptId` | string \| null | Prompt ID from API response |

## Notes

- The system prompt is **not** stored in JSONL files — it's constructed at runtime from the binary and injected into the API call.
- The `version` field records which Claude Code version was running when the entry was written — useful for correlating behavior changes with version updates.
- Sessions are stored per-project, keyed by the absolute project path.
