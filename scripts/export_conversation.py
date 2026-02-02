#!/usr/bin/env python3
"""
Export Claude Code conversation to markdown.

This script reads the JSONL conversation file stored by Claude Code and converts
it to a readable markdown format. It tracks the last exported line to enable
incremental exports without duplicating content.

Usage:
    export_conversation.py <session_id> <output_file>
    export_conversation.py --append <session_id> <output_file>
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime


def get_project_dir():
    """Find the project directory in ~/.claude/projects/"""
    cwd = os.getcwd()
    # Convert path to Claude's format: /path/to/project -> -path-to-project
    project_name = '-' + cwd.replace('/', '-').lstrip('-')

    claude_dir = Path.home() / '.claude' / 'projects' / project_name
    if claude_dir.exists():
        return claude_dir

    # Try to find it by partial match
    projects_dir = Path.home() / '.claude' / 'projects'
    if projects_dir.exists():
        for d in projects_dir.iterdir():
            if cwd.replace('/', '-').lstrip('-') in d.name:
                return d

    return None


def extract_text_content(content):
    """Extract text from message content (can be string or list of blocks)"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get('type') == 'text':
                    texts.append(block.get('text', ''))
                elif block.get('type') == 'tool_use':
                    tool_name = block.get('name', 'unknown')
                    tool_input = block.get('input', {})
                    input_str = json.dumps(tool_input, indent=2)
                    if len(input_str) > 500:
                        input_str = input_str[:500] + '...'
                    texts.append(f"\n**Tool: {tool_name}**\n```json\n{input_str}\n```\n")
                elif block.get('type') == 'tool_result':
                    result_content = block.get('content', '')
                    if isinstance(result_content, str):
                        if len(result_content) > 500:
                            result_content = result_content[:500] + '...'
                        texts.append(f"\n**Tool Result:**\n```\n{result_content}\n```\n")
        return '\n'.join(texts)
    return str(content)


def get_last_exported_line(tracking_file):
    """Get the last exported line number from tracking file"""
    if tracking_file.exists():
        try:
            return int(tracking_file.read_text().strip())
        except (ValueError, IOError):
            pass
    return 0


def save_last_exported_line(tracking_file, line_num):
    """Save the last exported line number"""
    tracking_file.write_text(str(line_num))


def export_conversation(session_file, output_file, is_compaction=False):
    """Export a conversation JSONL file to markdown, appending only new content"""

    # Track last exported line per session
    tracking_file = output_file.parent / f".{output_file.stem}.lastline"
    start_line = get_last_exported_line(tracking_file)

    messages = []
    current_line = 0

    with open(session_file, 'r') as f:
        for line in f:
            current_line += 1
            if current_line <= start_line:
                continue

            try:
                msg = json.loads(line)
                msg_type = msg.get('type')

                if msg_type == 'user':
                    content = msg.get('message', {})
                    if isinstance(content, dict):
                        text = extract_text_content(content.get('content', ''))
                    else:
                        text = str(content)
                    if text.strip():
                        messages.append(('user', text))

                elif msg_type == 'assistant':
                    content = msg.get('message', {})
                    if isinstance(content, dict):
                        text = extract_text_content(content.get('content', ''))
                    else:
                        text = str(content)
                    if text.strip():
                        messages.append(('assistant', text))

            except json.JSONDecodeError:
                continue

    if not messages:
        print(f"No new messages to export (already at line {start_line})")
        return

    # Append to output file
    file_exists = output_file.exists() and output_file.stat().st_size > 0

    with open(output_file, 'a') as f:
        if not file_exists:
            f.write(f"# Claude Code Conversation Log\n\n")
            f.write(f"**Session**: {session_file.name}\n\n")

        f.write(f"\n---\n\n")
        if is_compaction:
            f.write(f"## Pre-Compaction Export: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        else:
            f.write(f"## Export: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for role, content in messages:
            if role == 'user':
                f.write(f"### User\n\n{content}\n\n")
            else:
                f.write(f"### Assistant\n\n{content}\n\n")

    # Update tracking
    save_last_exported_line(tracking_file, current_line)
    print(f"Exported {len(messages)} new messages to {output_file}")


def main():
    if len(sys.argv) < 3:
        print("Usage: export_conversation.py <session_id> <output_file>")
        print("       export_conversation.py --append <session_id> <output_file>")
        sys.exit(1)

    is_compaction = False
    if sys.argv[1] == '--append':
        if len(sys.argv) < 4:
            print("Error: --append requires session_id and output_file")
            sys.exit(1)
        is_compaction = True
        session_id = sys.argv[2]
        output_file = sys.argv[3]
    else:
        session_id = sys.argv[1]
        output_file = sys.argv[2]

    project_dir = get_project_dir()
    if not project_dir:
        print("Error: Could not find project directory in ~/.claude/projects/")
        sys.exit(1)

    session_file = project_dir / f"{session_id}.jsonl"
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}")
        sys.exit(1)

    export_conversation(session_file, Path(output_file), is_compaction=is_compaction)


if __name__ == '__main__':
    main()
