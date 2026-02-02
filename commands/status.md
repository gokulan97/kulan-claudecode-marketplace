---
allowed-tools: Bash(test:*), Bash(cat:*)
description: Check if automatic conversation logging is enabled
---

## Context

- Session ID: ${CLAUDE_SESSION_ID}
- Autolog state directory: ~/.claude/autolog/

## Your task

Check the autolog status:

1. Check if state file exists: `test -f ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
2. If exists, read the directory: `cat ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
3. Report status to user:
   - If enabled: "Autolog is ON. Logging to: <directory>"
   - If disabled: "Autolog is OFF for this session. Use '/autolog:on' to enable."
