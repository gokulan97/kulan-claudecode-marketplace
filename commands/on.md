---
allowed-tools: Bash(mkdir:*), Bash(echo:*), Bash(python3:*)
description: Enable automatic conversation logging before context compaction
argument-hint: "[log-directory]"
---

## Context

- Session ID: ${CLAUDE_SESSION_ID}
- Current directory: !`pwd`
- Autolog state directory: ~/.claude/autolog/

## Your task

Enable automatic conversation logging:

1. Create the autolog state directory if it doesn't exist: `mkdir -p ~/.claude/autolog`
2. Create/update the state file with the log directory:
   - If directory provided in arguments: `echo "<directory>" > ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
   - If no directory provided: `echo "$(pwd)/autolog" > ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
3. Create the log directory: `mkdir -p <directory>`
4. Run an immediate export to catch up: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/export_conversation.py ${CLAUDE_SESSION_ID} <directory>/${CLAUDE_SESSION_ID}.md`
5. Confirm to user: "Autolog enabled. Conversations will be saved to <directory>/${CLAUDE_SESSION_ID}.md before each context compaction."

**Arguments received:** $ARGUMENTS
