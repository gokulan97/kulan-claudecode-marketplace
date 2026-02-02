---
name: ""
allowed-tools: Bash(mkdir:*), Bash(echo:*), Bash(cat:*), Bash(rm:*), Bash(test:*), Bash(python3:*)
description: Toggle automatic conversation logging before context compaction
argument-hint: "[on|off|status] [log-directory]"
---

## Context

- Session ID: ${CLAUDE_SESSION_ID}
- Current directory: !`pwd`
- Autolog state directory: ~/.claude/autolog/

## Your task

The user wants to manage automatic conversation logging. Based on the arguments provided:

**If argument is "on" or "on <directory>":**
1. Create the autolog state directory if it doesn't exist: `mkdir -p ~/.claude/autolog`
2. Create/update the state file with the log directory:
   - If directory provided: `echo "<directory>" > ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
   - If no directory: `echo "$(pwd)/autolog" > ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
3. Create the log directory: `mkdir -p <directory>`
4. Run an immediate export to catch up: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/export_conversation.py ${CLAUDE_SESSION_ID} <directory>/${CLAUDE_SESSION_ID}.md`
5. Confirm to user: "Autolog enabled. Conversations will be saved to <directory>/${CLAUDE_SESSION_ID}.md before each context compaction."

**If argument is "off":**
1. Remove the state file: `rm -f ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
2. Confirm to user: "Autolog disabled for this session."

**If argument is "status" or empty:**
1. Check if state file exists: `test -f ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
2. If exists, read the directory: `cat ~/.claude/autolog/${CLAUDE_SESSION_ID}.enabled`
3. Report status to user:
   - If enabled: "Autolog is ON. Logging to: <directory>"
   - If disabled: "Autolog is OFF for this session. Use '/autolog on' to enable."

**Arguments received:** $ARGUMENTS
