# Autolog Plugin

Automatically saves conversation history before context compaction to prevent losing valuable session context.

## Problem

When Claude Code's context window fills up, it compacts the conversation to make room for new content. This means earlier parts of your conversation are summarized or lost. For long debugging sessions or complex projects, this can be frustrating.

## Solution

The autolog plugin:
1. Hooks into the `PreCompact` event
2. Exports your full conversation to a markdown file before compaction occurs
3. Uses incremental exports to avoid duplicating content across multiple compactions

## Installation

Copy this plugin to your Claude Code plugins directory:

```bash
cp -r plugins/autolog ~/.claude/plugins/
```

Or install via the plugin command:
```
/plugin install autolog
```

## Usage

### Enable autolog for current session

```
/autolog on
```

This saves logs to `./autolog/<session-id>.md` in your current directory.

### Enable with custom directory

```
/autolog on ~/my-logs
```

### Check status

```
/autolog status
```

### Disable

```
/autolog off
```

## How it works

1. When you run `/autolog on`, the plugin creates a state file at `~/.claude/autolog/<session-id>.enabled`
2. The `PreCompact` hook checks for this state file before each compaction
3. If enabled, it runs `export_conversation.py` to append new messages to your log file
4. A tracking file (`.session-id.lastline`) prevents duplicate exports

## Output format

Conversations are exported as markdown:

```markdown
# Claude Code Conversation Log

**Session**: abc123-def456.jsonl

---

## Pre-Compaction Export: 2024-01-15 10:30:00

### User

How do I fix this bug?

### Assistant

Let me look at the code...

---

## Pre-Compaction Export: 2024-01-15 11:45:00

### User

Can you also add tests?

...
```

## Files

- `commands/autolog.md` - The `/autolog` slash command
- `hooks/hooks.json` - Registers the `PreCompact` hook
- `scripts/save-on-compact.sh` - Shell script that runs before compaction
- `scripts/export_conversation.py` - Python script that parses and exports conversations

## Requirements

- Python 3.6+
- Claude Code with hooks support

## Notes

- Logs are session-specific; each session gets its own file
- The plugin only logs when explicitly enabled via `/autolog on`
- Tool calls and results are included but truncated to 500 characters for readability
