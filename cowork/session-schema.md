# Cowork Session JSON Schema

Schema for `local_{uuid}.json` session files found at:

- **macOS:** `~/Library/Application Support/Claude/local-agent-mode-sessions/{uuid}/{uuid}/local_{uuid}.json`
- **Windows:** `~\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\{uuid}\{uuid}\local_{uuid}.json`

Each Cowork chat session produces one file. The outer UUID directory appears to be a workspace/account identifier; the inner UUID is per-session.

---

## Top-level fields

| Field | Type | Example | Notes |
|---|---|---|---|
| `sessionId` | `string` | `"local_2452ecbd-..."` | `local_` prefix + UUID |
| `processName` | `string` | `"focused-confident-goodall"` | Adjective-adjective-surname format; VM process name |
| `vmProcessName` | `string` | `"focused-confident-goodall"` | Same as `processName` |
| `cliSessionId` | `string` | `"85f45568-..."` | UUID; internal Claude Code session ID |
| `cwd` | `string` | `"/sessions/focused-confident-goodall"` | VM working directory (resets each session) |
| `userSelectedFolders` | `string[]` | `["/Users/alice/Documents"]` | Absolute host paths the user mounted into the session |
| `userApprovedFileAccessPaths` | `string[]` | `["/Users/alice/Documents", ...]` | Full list of paths approved for file access (superset of `userSelectedFolders`) |
| `createdAt` | `number` | `1773807095475` | Unix timestamp in milliseconds |
| `lastActivityAt` | `number` | `1773818176085` | Unix timestamp in milliseconds |
| `model` | `string` | `"claude-sonnet-4-6"` | Claude model ID used for this session |
| `isArchived` | `boolean` | `false` | Whether the session has been archived |
| `title` | `string` | `"Create brisket prep and cooking tutorial"` | Auto-generated session title |
| `initialMessage` | `string` | `"give me one from an earlier part..."` | First user message in the session |
| `slashCommands` | `string[]` | `["data:validate", "compact", ...]` | Available slash commands; format is `"plugin:command"` or `"command"` for built-ins |
| `enabledMcpTools` | `{ [key: string]: true }` | `{"filesystem:list_directory": true}` | MCP tools enabled in this session; see below |
| `remoteMcpServersConfig` | `array` | `[]` | Remote MCP server configurations; usually empty |
| `fsDetectedFiles` | `FsDetectedFile[]` | see below | Files detected or used during the session |
| `egressAllowedDomains` | `string[]` | `["github.com", "*.anthropic.com"]` | Domains the VM sandbox may connect to outbound; supports `*` wildcard prefix |
| `systemPrompt` | `string` | `"<application_details>..."` | Full system prompt template with `{{placeholder}}` variables |
| `accountName` | `string` | `"Lawrence"` | **PII** — user's display name |
| `emailAddress` | `string` | `"user@example.com"` | **PII** — user's email address |

---

## `enabledMcpTools`

A flat object where each key is a tool identifier and the value is always `true`. Key formats:

| Format | Example | Meaning |
|---|---|---|
| `server:tool` | `filesystem:list_directory` | Standard MCP tool from a named server |
| `local:server:tool-{hash}` | `local:filesystem:list_directory-edbc26...` | Locally-registered tool; hash is session-specific |

---

## `FsDetectedFile`

Files that were detected or accessed during the session.

| Field | Type | Example | Notes |
|---|---|---|---|
| `hostPath` | `string` | `"/Users/alice/Movies/clip.mp4"` | Absolute path on the host machine |
| `fileName` | `string` | `"clip.mp4"` | Filename only |
| `timestamp` | `number` | `1773808133136` | Unix timestamp in milliseconds when the file was detected |

---

## Template variables in `systemPrompt`

The `systemPrompt` is a template with these placeholders substituted at session start:

| Placeholder | Description |
|---|---|
| `{{accountName}}` | User's account display name |
| `{{emailAddress}}` | User's email address |
| `{{cwd}}` | VM working directory |
| `{{workspaceFolder}}` | Persistent workspace folder on host |
| `{{skillsDir}}` | Path to skills/plugins directory |
| `{{workspaceContext}}` | Whether the user has selected a folder |
| `{{currentDateTime}}` | Current date and time |
| `{{modelName}}` | Model being used |
| `{{folderSelected}}` | Boolean — whether user mounted a folder |

---

## Notes

- The two nested UUID directories: the outer one (`d8c57b81-...`) appears stable per user/install; the inner one (`2dd73419-...`) appears to be a workspace context. The `local_{uuid}.json` file within is the actual session.
- `accountName` and `emailAddress` are present in plain text — treat these files as containing PII.
- Session files are not deleted when a session ends; they persist until manually removed.
