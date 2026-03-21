# Cowork Session JSON Schema

File location:
- macOS: `~/Library/Application Support/Claude/local-agent-mode-sessions/{uuid}/{uuid}/local_{uuid}.json`
- Windows: `~\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\local-agent-mode-sessions\{uuid}\{uuid}\local_{uuid}.json`

## Fields

| Field | Type | Notes |
|---|---|---|
| `sessionId` | string | `local_` + UUID |
| `processName` | string | Adjective-adjective-surname; VM process name |
| `vmProcessName` | string | Same as `processName` |
| `cliSessionId` | string | UUID |
| `cwd` | string | `/sessions/{processName}` — VM working dir, resets each session |
| `userSelectedFolders` | string[] | Host paths the user mounted |
| `userApprovedFileAccessPaths` | string[] | All paths approved for file access |
| `createdAt` | number | Unix timestamp ms |
| `lastActivityAt` | number | Unix timestamp ms |
| `model` | string | Claude model ID |
| `isArchived` | boolean | |
| `title` | string | Auto-generated session title |
| `initialMessage` | string | First user message |
| `slashCommands` | string[] | Available slash commands; format `plugin:command` or `command` |
| `enabledMcpTools` | object | Keys are `server:tool` or `local:server:tool-{hash}`, values always `true` |
| `remoteMcpServersConfig` | array | Remote MCP server configs; usually empty |
| `fsDetectedFiles` | object[] | `{ hostPath, fileName, timestamp }` — files accessed during session |
| `egressAllowedDomains` | string[] | Domains the VM may connect to; supports `*` wildcard prefix |
| `systemPrompt` | string | Full system prompt template with `{{placeholder}}` variables |
| `accountName` | string | **PII** — user display name |
| `emailAddress` | string | **PII** — user email |

## `systemPrompt` template variables

| Placeholder | Description |
|---|---|
| `{{accountName}}` | User display name |
| `{{emailAddress}}` | User email |
| `{{cwd}}` | VM working directory |
| `{{workspaceFolder}}` | Persistent workspace folder on host |
| `{{skillsDir}}` | Path to skills/plugins directory |
| `{{workspaceContext}}` | Whether user selected a folder |
| `{{currentDateTime}}` | Current date and time |
| `{{modelName}}` | Model being used |
| `{{folderSelected}}` | Boolean — whether user mounted a folder |
