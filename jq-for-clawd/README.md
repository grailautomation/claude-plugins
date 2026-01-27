# jq-for-clawd

A Claude Code plugin that provides knowledge for querying session history using jq.

## Purpose

When users ask about past conversations, previous sessions, or want to search their conversation history, this skill teaches Claude how to:

- Locate session files in `~/.claude/projects/`
- Parse JSONL session format with jq
- Extract user messages with timestamps
- Filter by date, content, or message type
- Present results in a clean format

## Trigger Phrases

- "JQ for Claude"
- "jq4clawd"
- "jq-for-clawd"
- "find my past sessions"
- "what did I ask before"
- "search conversation history"

## Installation

Add this plugin to Claude Code:

```bash
claude --plugin-dir ~/Documents/DEV/claude-plugins/jq-for-clawd
```

Or symlink into your plugins directory.

## Requirements

- `jq` command-line JSON processor
- `bash` shell

## Usage

Simply ask Claude about your past conversations:

> "Can you find what I asked you in our last few sessions?"

> "Search my conversation history for mentions of 'API'"

> "What were my first messages from yesterday's sessions?"

Claude will use jq to query the session files and present the results.
