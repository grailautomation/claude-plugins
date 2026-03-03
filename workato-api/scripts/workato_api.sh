#!/usr/bin/env bash
set -euo pipefail

# Workato API helper — thin wrapper around curl for common operations
# Usage: workato_api.sh <method> <endpoint> [data]
#
# Examples:
#   workato_api.sh GET /api/users/me
#   workato_api.sh GET "/api/recipes?per_page=10&running=true"
#   workato_api.sh GET /api/recipes/12345
#   workato_api.sh PUT /api/recipes/12345/start
#   workato_api.sh POST /api/recipes '{"recipe":{"name":"test"}}'

WORKATO_BASE_URL="${WORKATO_BASE_URL:-https://www.workato.com}"
JQ="${JQ:-jq}"

if [ -z "${WORKATO_API_TOKEN:-}" ]; then
  echo "ERROR: WORKATO_API_TOKEN is not set" >&2
  exit 1
fi

METHOD="${1:?Usage: workato_api.sh <METHOD> <ENDPOINT> [DATA]}"
ENDPOINT="${2:?Usage: workato_api.sh <METHOD> <ENDPOINT> [DATA]}"
DATA="${3:-}"

# Build URL — handle both /api/... and full URLs
if [[ "$ENDPOINT" == http* ]]; then
  URL="$ENDPOINT"
else
  URL="${WORKATO_BASE_URL}${ENDPOINT}"
fi

# Build curl args
CURL_ARGS=(
  -s
  -H "Authorization: Bearer $WORKATO_API_TOKEN"
  -H "Content-Type: application/json"
  -X "$METHOD"
)

if [ -n "$DATA" ]; then
  CURL_ARGS+=(-d "$DATA")
fi

# Execute and format
RESPONSE=$(curl "${CURL_ARGS[@]}" "$URL")

# Try to format with jq, fall back to raw output
if command -v "$JQ" &>/dev/null; then
  echo "$RESPONSE" | "$JQ" '.' 2>/dev/null || echo "$RESPONSE"
else
  echo "$RESPONSE"
fi
