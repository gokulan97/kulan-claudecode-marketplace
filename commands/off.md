---
allowed-tools: Bash(rm:*)
description: Disable automatic conversation logging for this session
---

## Context

- Session ID: ${CLAUDE_SESSION_ID}
- Autolog state directory: ~/.claude/autolog/

## Your task

Disable automatic conversation logging:

1. Remove the state file: `rm -f ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
2. Confirm to user: "Autolog disabled for this session."
