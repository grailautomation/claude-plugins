---
name: jq-for-clawd
description: Query Claude Code session history using jq to find past conversations. Use when users mention "JQ for Claude", "jq4clawd", "jq-for-clawd", "find my past sessions", "what did I ask before", "search conversation history", or "query session files".
---

# JQ for Claude - Session History Queries

Use this skill when users ask about past conversations, previous sessions, or conversation history.

---

## Session File Location

Claude Code stores session history as JSONL files at:

```
~/.claude/projects/<encoded-project-path>/<session-id>.jsonl
```

**Path encoding**: Project paths use dashes instead of slashes.
- `/Users/dave/Documents/my-project` becomes `-Users-dave-Documents-my-project`

### Find the Project Directory

To find sessions for a specific project path:

```bash
# Encode project path (replace / with -)
PROJECT_PATH="/Users/dave/Documents/my-project"
ENCODED=$(echo "$PROJECT_PATH" | sed 's|^/|-|; s|/|-|g')
SESSION_DIR="$HOME/.claude/projects/$ENCODED"

# List sessions sorted by modification time
ls -lt "$SESSION_DIR"/*.jsonl 2>/dev/null | head -10
```

### List All Project Directories

```bash
ls -lt ~/.claude/projects/ | head -20
```

---

## JSONL File Structure

Each session file contains one JSON object per line:

| Line Type | Key Fields | Description |
|-----------|------------|-------------|
| `summary` | `type`, `summary`, `leafUuid` | Session metadata (first line) |
| `user` | `type`, `timestamp`, `message` | User messages |
| `assistant` | `type`, `timestamp`, `message` | Claude responses |
| `system` | `type`, `message` | System prompts |
| `file-history-snapshot` | `type`, `snapshot` | File state snapshots |

### Message Content Structure

User and assistant messages have this structure:

```json
{
  "type": "user",
  "timestamp": "2026-01-10T22:32:07.522Z",
  "message": {
    "role": "user",
    "content": "your message text here"
  },
  "sessionId": "uuid",
  "uuid": "message-uuid"
}
```

**Note**: `message.content` can be either:
- A string: `"content": "hello"`
- An array: `"content": [{"type": "text", "text": "hello"}]`

---

## Common jq Patterns

### Extract User Messages with Timestamps

```bash
cat session.jsonl | jq -r '
  select(.type == "user") |
  .timestamp + " | " + (
    if .message.content | type == "string"
    then .message.content[0:300]
    else (.message.content[0].text // "N/A")[0:300]
    end
  )
' | grep -v "N/A" | grep -v "command-name" | grep -v "local-command"
```

### Count Message Types in a Session

```bash
cat session.jsonl | jq -r '.type' | sort | uniq -c
```

### Get Session Start Time

```bash
head -5 session.jsonl | jq -r 'select(.type == "user") | .timestamp' | head -1
```

### Find Sessions by Content

Search across all sessions in a project for a keyword:

```bash
SESSION_DIR="$HOME/.claude/projects/-Users-dave-Documents-my-project"
for f in "$SESSION_DIR"/*.jsonl; do
  if grep -q "keyword" "$f" 2>/dev/null; then
    echo "=== $f ==="
    cat "$f" | jq -r 'select(.type == "user" and (.message.content | tostring | test("keyword"; "i"))) | .timestamp + " | " + (.message.content | tostring)[0:200]' 2>/dev/null
  fi
done
```

### List Recent Sessions with First User Message

```bash
SESSION_DIR="$HOME/.claude/projects/-Users-dave-Documents-my-project"
for f in $(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | grep -v "agent-" | head -5); do
  echo ""
  echo "=== $(basename $f) ==="
  cat "$f" | jq -r '
    select(.type == "user") |
    .timestamp + " | " + (
      if .message.content | type == "string"
      then .message.content[0:150]
      else (.message.content[0].text // "N/A")[0:150]
      end
    )
  ' 2>/dev/null | grep -v "N/A" | grep -v "command-name" | head -3
done
```

---

## Filtering Tips

### Exclude Agent Sessions

Agent/subagent sessions have filenames starting with `agent-`:

```bash
ls -lt "$SESSION_DIR"/*.jsonl | grep -v "agent-"
```

### Filter by Date

Sessions include ISO timestamps. Filter with jq:

```bash
cat session.jsonl | jq -r '
  select(.type == "user" and .timestamp > "2026-01-10") |
  .timestamp + " | " + (.message.content | tostring)[0:100]
'
```

### Exclude System Messages

Filter out command invocations and system noise:

```bash
grep -v "command-name" | grep -v "local-command" | grep -v "N/A"
```

---

## Example Workflow

When a user asks "what did I ask you in our last few sessions?":

1. **Identify the project path** (current working directory or ask user)

2. **Encode and locate sessions**:
   ```bash
   ENCODED=$(echo "$PWD" | sed 's|^/|-|; s|/|-|g')
   SESSION_DIR="$HOME/.claude/projects/$ENCODED"
   ```

3. **List recent non-agent sessions**:
   ```bash
   ls -lt "$SESSION_DIR"/*.jsonl | grep -v "agent-" | head -5
   ```

4. **Extract user messages from each**:
   ```bash
   cat "$SESSION_DIR/<session-id>.jsonl" | jq -r '
     select(.type == "user") |
     .timestamp + " | " + (
       if .message.content | type == "string"
       then .message.content[0:300]
       else (.message.content[0].text // "N/A")[0:300]
       end
     )
   ' | grep -v "N/A" | grep -v "command-name" | head -5
   ```

5. **Present results** in a clean, organized format grouped by session with timestamps.

---

## Troubleshooting

**No sessions found**: Verify the project path encoding matches exactly. Check `ls ~/.claude/projects/` for the correct directory name.

**jq parse errors**: Some lines may have malformed JSON. Add `2>/dev/null` to suppress errors.

**Empty content**: Some user messages (like tool approvals) have array content without text. Filter with `grep -v "N/A"`.
