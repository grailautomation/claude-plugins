---
name: codex-session-history
description: Query local Codex session history with jq. Use when users explicitly ask to search Codex sessions, inspect prior Codex conversations, find previous user messages, locate tool calls, summarize past work by working directory, or query Codex rollout JSONL files.
---

# Codex Session History

Use this skill when the user explicitly asks to inspect local Codex session history. Codex session files can contain private prompts, screenshots, tool outputs, and credentials accidentally pasted by a user, so extract only the fields needed to answer the request.

## Session Locations

Codex stores active session JSONL files under date-partitioned directories:

```bash
~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
```

Older sessions may be archived flat under:

```bash
~/.codex/archived_sessions/rollout-*.jsonl
```

Memory summaries under `~/.codex/memories/rollout_summaries/` are derived summaries, not raw session logs. Use them only when the user asks for memory-derived history or when raw session search is too broad.

## JSONL Structure

Each line is a JSON object. Common top-level `type` values:

| Type | Useful fields | Notes |
| --- | --- | --- |
| `session_meta` | `.payload.id`, `.payload.cwd`, `.payload.originator`, `.payload.cli_version`, `.payload.source`, `.payload.model_provider` | Also may contain large instructions; do not print the full payload by default. |
| `turn_context` | `.payload.turn_id`, `.payload.cwd`, `.payload.current_date`, `.payload.model`, `.payload.summary` | Marks turn boundaries and compaction context. |
| `event_msg` | `.payload.type`, plus event-specific fields | Includes `user_message`, `agent_message`, `task_started`, `task_complete`, `token_count`, and patch events. |
| `response_item` | `.payload.type`, `.payload.role`, `.payload.content`, `.payload.name`, `.payload.arguments` | Stores model messages, reasoning, function calls, and tool outputs. |

Common `response_item.payload.type` values include `message`, `reasoning`, `function_call`, `function_call_output`, `custom_tool_call`, and `custom_tool_call_output`.

## Safe Search Defaults

- Prefer field extraction with `jq`; avoid raw `cat`, `head`, or `grep` over full files.
- Skip or summarize `session_meta.payload.base_instructions`, large image payloads, and full tool outputs unless the user explicitly needs them.
- Use `--arg` for user-provided search text instead of interpolating it into jq programs.
- Truncate message/tool excerpts in exploratory commands.
- Report file paths and timestamps so the user can request a deeper follow-up.

## Find Session Files

Recent active sessions:

```bash
find "$HOME/.codex/sessions" -name '*.jsonl' -type f -print0 |
  xargs -0 ls -t |
  head -20
```

Recent active and archived sessions together:

```bash
find "$HOME/.codex/sessions" "$HOME/.codex/archived_sessions" \
  -name '*.jsonl' -type f -print0 2>/dev/null |
  xargs -0 ls -t |
  head -30
```

Sessions for a working directory:

```bash
TARGET_CWD="$PWD"
find "$HOME/.codex/sessions" "$HOME/.codex/archived_sessions" \
  -name '*.jsonl' -type f -print0 2>/dev/null |
  while IFS= read -r -d '' f; do
    jq -e --arg cwd "$TARGET_CWD" '
      select(.type == "session_meta" and .payload.cwd == $cwd)
    ' "$f" >/dev/null 2>&1 && printf '%s\n' "$f"
  done |
  xargs ls -t 2>/dev/null |
  head -20
```

## Inspect File Shape

Count top-level line types:

```bash
jq -r '.type // "<missing>"' "$SESSION_FILE" | sort | uniq -c
```

Count response item types:

```bash
jq -r '
  select(.type == "response_item") |
  .payload.type // "<missing>"
' "$SESSION_FILE" | sort | uniq -c
```

Show safe metadata:

```bash
jq -c '
  select(.type == "session_meta") |
  {
    timestamp,
    id: .payload.id,
    cwd: .payload.cwd,
    originator: .payload.originator,
    cli_version: .payload.cli_version,
    source: .payload.source,
    model_provider: .payload.model_provider
  }
' "$SESSION_FILE"
```

## Extract Messages

User messages from the event stream:

```bash
jq -r '
  select(.type == "event_msg" and .payload.type == "user_message") |
  .timestamp + " | " + (.payload.message // "" | gsub("\n"; " ") | .[0:300])
' "$SESSION_FILE"
```

Assistant final/intermediate messages from the event stream:

```bash
jq -r '
  select(.type == "event_msg" and .payload.type == "agent_message") |
  .timestamp + " | " + ((.payload.phase // "agent") + " | " + (.payload.message // "" | gsub("\n"; " ") | .[0:300]))
' "$SESSION_FILE"
```

Messages from response items:

```bash
jq -r '
  def content_text:
    if (.payload.content | type) == "array" then
      [.payload.content[]? | .text // .input_text // empty] | join(" ")
    elif (.payload.content | type) == "string" then
      .payload.content
    else
      ""
    end;

  select(.type == "response_item" and .payload.type == "message") |
  .timestamp + " | " + (.payload.role // "unknown") + " | " + (content_text | gsub("\n"; " ") | .[0:300])
' "$SESSION_FILE"
```

## Search By Keyword

Search user and assistant event messages across active and archived sessions:

```bash
QUERY="keyword"
find "$HOME/.codex/sessions" "$HOME/.codex/archived_sessions" \
  -name '*.jsonl' -type f -print0 2>/dev/null |
  while IFS= read -r -d '' f; do
    jq -r --arg q "$QUERY" --arg file "$f" '
      select(
        .type == "event_msg" and
        (.payload.type == "user_message" or .payload.type == "agent_message") and
        ((.payload.message // "") | test($q; "i"))
      ) |
      $file + "\t" + .timestamp + "\t" + .payload.type + "\t" +
      ((.payload.message // "") | gsub("\n"; " ") | .[0:240])
    ' "$f" 2>/dev/null
  done
```

Search response item text while avoiding session metadata:

```bash
QUERY="keyword"
jq -r --arg q "$QUERY" '
  def content_text:
    if (.payload.content | type) == "array" then
      [.payload.content[]? | .text // .input_text // empty] | join(" ")
    elif (.payload.content | type) == "string" then
      .payload.content
    else
      ""
    end;

  select(.type == "response_item" and .payload.type == "message") |
  content_text as $text |
  select($text | test($q; "i")) |
  .timestamp + " | " + (.payload.role // "unknown") + " | " + ($text | gsub("\n"; " ") | .[0:240])
' "$SESSION_FILE"
```

## Tool Calls

List function calls without full arguments:

```bash
jq -r '
  select(.type == "response_item" and .payload.type == "function_call") |
  .timestamp + " | " + (.payload.name // "tool") + " | " + (.payload.call_id // "")
' "$SESSION_FILE"
```

Find calls to a specific tool:

```bash
TOOL_NAME="exec_command"
jq -r --arg tool "$TOOL_NAME" '
  select(
    .type == "response_item" and
    .payload.type == "function_call" and
    .payload.name == $tool
  ) |
  .timestamp + " | " + (.payload.call_id // "") + " | " + ((.payload.arguments // "") | tostring | gsub("\n"; " ") | .[0:300])
' "$SESSION_FILE"
```

List tool outputs by call id without printing full output:

```bash
jq -r '
  select(.type == "response_item" and .payload.type == "function_call_output") |
  .timestamp + " | " + (.payload.call_id // "") + " | " + ((.payload.output // "") | tostring | gsub("\n"; " ") | .[0:220])
' "$SESSION_FILE"
```

## Typical Workflow

When the user asks to find prior Codex work:

1. Identify whether they mean the current repository, a date range, a keyword, or a specific task.
2. List likely session files by modification time, or filter by `session_meta.payload.cwd`.
3. Count line types in one representative file before extracting details.
4. Search `event_msg` user and assistant messages first; use `response_item` for deeper reconstruction.
5. Return a compact answer with timestamps, matching excerpts, and the session file paths used.
