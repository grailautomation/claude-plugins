# Google Workspace Plugin

Google Workspace is one broad plugin for the `gws` CLI. It is intentionally not
split by product or side-effect class: Gmail, Drive, Calendar, Sheets, Docs,
Slides, Chat, Meet, Tasks, Forms, Keep, Events, Model Armor, personas, and
cross-product recipes live together because they share one CLI and one auth
model.

## Runtime Contract

- The `gws` binary must be on `$PATH`.
- Use `gws` v0.22.5 or newer. Older versions are missing helper commands used by
  these skills, including Gmail reply, reply-all, forward, attachments, drafts,
  and Calendar timezone support.
- Verify the installed version with `gws --version` before relying on helper
  commands.
- This plugin does not ship an MCP server or `.mcp.json`; it preserves the
  existing CLI-backed behavior for Claude Code and Codex.

## Auth Contract

- Check auth with `gws auth status` before running commands that call Google APIs.
- Use `gws auth login` for interactive OAuth.
- Use `gws auth login --readonly` when read-only access is enough.
- Use `gws auth login --full` when Workspace Events, Pub/Sub, cloud-platform, or
  Model Armor workflows are needed.
- Service-account credentials can be supplied with
  `GOOGLE_APPLICATION_CREDENTIALS` when the target API and domain policy support
  that mode.

## Side-Effect Classes

- Read: agenda, Gmail triage, Drive/Sheets/Docs reads, reports, and schema
  inspection.
- Write: docs writes, sheet appends, Drive uploads, Calendar inserts, Tasks,
  Forms, Keep, and Classroom changes.
- Send/share/invite: Gmail sends/replies/forwards, Chat sends, Drive permission
  changes, event attendee updates, and recipe workflows that notify people.
- Watch/subscribe/renew: Gmail watches, Drive watches, Workspace Events, Pub/Sub
  resources, and renewal helpers. Some resources persist unless `--cleanup` is
  used.
- Admin/security: Admin Reports, directory/admin APIs where present, and Model
  Armor template operations.
- Multi-product recipes: treat the whole recipe as the highest-impact class among
  its steps.

For write, delete, send, share, invite, watch, subscribe, renew, admin, security,
or multi-product workflows, confirm intent with the user before executing. Prefer
`--dry-run` where the helper supports it.
