#!/usr/bin/env bash
set -euo pipefail

# Set up plan directory structure for the current feature.
# Detects feature from git branch or latest .specify/specs/ entry.
# Output: JSON with FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH

# Determine repo root
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(pwd)"
    HAS_GIT=false
fi

cd "$REPO_ROOT"

# Determine current feature
get_current_feature() {
    # Check SPECIFY_FEATURE env var first
    if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
        echo "$SPECIFY_FEATURE"
        return
    fi

    # Check git branch
    if [[ "$HAS_GIT" == "true" ]]; then
        local branch
        branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [[ "$branch" =~ ^[0-9]{3}- ]]; then
            echo "$branch"
            return
        fi
    fi

    # Fall back to latest spec directory
    local specs_dir="$REPO_ROOT/.specify/specs"
    if [[ -d "$specs_dir" ]]; then
        local latest=""
        local highest=0
        for dir in "$specs_dir"/*/; do
            [[ -d "$dir" ]] || continue
            local dirname
            dirname=$(basename "$dir")
            if [[ "$dirname" =~ ^([0-9]{3})- ]]; then
                local number=${BASH_REMATCH[1]}
                number=$((10#$number))
                if [[ "$number" -gt "$highest" ]]; then
                    highest=$number
                    latest=$dirname
                fi
            fi
        done
        if [[ -n "$latest" ]]; then
            echo "$latest"
            return
        fi
    fi

    echo ""
}

CURRENT_FEATURE=$(get_current_feature)

if [[ -z "$CURRENT_FEATURE" ]]; then
    echo "ERROR: No feature found. Run /spec-kit:specify first." >&2
    exit 1
fi

FEATURE_DIR="$REPO_ROOT/.specify/specs/$CURRENT_FEATURE"
mkdir -p "$FEATURE_DIR"

FEATURE_SPEC="$FEATURE_DIR/spec.md"
IMPL_PLAN="$FEATURE_DIR/plan.md"

if [[ ! -f "$FEATURE_SPEC" ]]; then
    echo "ERROR: spec.md not found at $FEATURE_SPEC. Run /spec-kit:specify first." >&2
    exit 1
fi

# Create plan file if it doesn't exist
touch "$IMPL_PLAN"

printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","HAS_GIT":"%s"}\n' \
    "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_FEATURE" "$HAS_GIT"
