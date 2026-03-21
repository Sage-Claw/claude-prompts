---
extracted: 2026-03-19
version: 2.1.80
build-time: 2026-03-19T21:00:45Z
content-hash: 07f6e4397224a016
---

# Claude Code Settings

```json
{
  "cleanupPeriodDays": 99999,
  "attribution": {
    "commit": "",
    "pr": ""
  },
  "model": "opusplan",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/lawrencewu/.claude/hooks/peon-ping/peon.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/lawrencewu/.claude/hooks/peon-ping/peon.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/lawrencewu/.claude/hooks/peon-ping/peon.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/lawrencewu/.claude/hooks/peon-ping/peon.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/lawrencewu/.claude/hooks/peon-ping/peon.sh",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "/bin/bash /Users/lawrencewu/.claude/statusline-command.sh"
  },
  "enabledPlugins": {
    "claude-md-management@claude-plugins-official": true,
    "skill-creator@claude-plugins-official": true,
    "frontend-design@claude-plugins-official": true
  },
  "effortLevel": "medium",
  "skipDangerousModePermissionPrompt": true
}
```
