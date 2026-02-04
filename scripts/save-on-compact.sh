#!/bin/bash
set -eo pipefail

# Hook script to save conversation before context compaction
# This runs automatically when Claude Code compacts the context window

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read hook input from stdin (JSON)
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

# Exit if no session ID
if [ -z "$SESSION_ID" ]; then
    exit 0
fi

# Check if autolog is enabled for this session
AUTOLOG_STATE_DIR="${HOME}/.claude/autolog"
AUTOLOG_STATE_FILE="${AUTOLOG_STATE_DIR}/${SESSION_ID}.enabled"

# If state file doesn't exist, autolog is disabled for this session
if [ ! -f "$AUTOLOG_STATE_FILE" ]; then
    exit 0
fi

# Read the log directory from the state file
LOG_DIR=$(cat "$AUTOLOG_STATE_FILE")

# Default to project's autolog directory if not specified
if [ -z "$LOG_DIR" ]; then
    LOG_DIR="$(pwd)/autolog"
fi

mkdir -p "$LOG_DIR"

OUTPUT_FILE="$LOG_DIR/${SESSION_ID}.md"

# Export the conversation (appends only new messages)
# If export fails, log a marker instead
if ! python3 "$SCRIPT_DIR/export_conversation.py" --append "$SESSION_ID" "$OUTPUT_FILE" 2>/dev/null; then
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "## Compaction at $(date)" >> "$OUTPUT_FILE"
    echo "Note: Full export failed, this is a marker only." >> "$OUTPUT_FILE"
fi
