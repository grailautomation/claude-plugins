#!/usr/bin/env bash
set -euo pipefail

# Set up plan directory structure for the current feature.
# Detects feature from git branch or latest .specify/specs/ entry.
# Output: JSON with FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH

WRITE_CONTEXT=true
ALLOW_LATEST="${SPEC_KIT_ALLOW_LATEST:-false}"
for arg in "$@"; do
    case "$arg" in
        --no-context) WRITE_CONTEXT=false ;;
        --allow-latest) ALLOW_LATEST=true ;;
        --help|-h)
            echo "Usage: $0 [--no-context] [--allow-latest]" >&2
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'" >&2
            exit 1
            ;;
    esac
done

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
        printf 'env\t%s\n' "$SPECIFY_FEATURE"
        return
    fi

    # Check git branch
    if [[ "$HAS_GIT" == "true" ]]; then
        local branch
        branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [[ "$branch" =~ ^[0-9]{3}- ]]; then
            printf 'branch\t%s\n' "$branch"
            return
        fi
    fi

    # Fall back to latest spec directory only when explicitly allowed or when no
    # git repo exists. In established repos, silent "latest" selection can bind
    # the plan to the wrong feature.
    local specs_dir="$REPO_ROOT/.specify/specs"
    if [[ -d "$specs_dir" && ( "$ALLOW_LATEST" == "true" || "$HAS_GIT" != "true" ) ]]; then
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
            printf 'latest\t%s\n' "$latest"
            return
        fi
    fi

    printf '\t\n'
}

FEATURE_RESULT=$(get_current_feature)
FEATURE_SOURCE=${FEATURE_RESULT%%$'\t'*}
CURRENT_FEATURE=${FEATURE_RESULT#*$'\t'}

if [[ -z "$CURRENT_FEATURE" ]]; then
    echo "ERROR: No active feature found." >&2
    echo "Run /spec-kit:specify first, set SPECIFY_FEATURE, switch to a ###-feature branch, or re-run with --allow-latest if you intentionally want the latest spec directory." >&2
    exit 1
fi

FEATURE_DIR="$REPO_ROOT/.specify/specs/$CURRENT_FEATURE"
mkdir -p "$FEATURE_DIR"
mkdir -p "$REPO_ROOT/.specify/memory"

FEATURE_SPEC="$FEATURE_DIR/spec.md"
IMPL_PLAN="$FEATURE_DIR/plan.md"

if [[ ! -f "$FEATURE_SPEC" ]]; then
    echo "ERROR: spec.md not found at $FEATURE_SPEC. Run /spec-kit:specify first." >&2
    exit 1
fi

# Create plan file if it doesn't exist
touch "$IMPL_PLAN"

PROJECT_CONTEXT="$REPO_ROOT/.specify/memory/project-context.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

json_escape() {
    local value=${1//\\/\\\\}
    value=${value//\"/\\\"}
    value=${value//$'\n'/\\n}
    value=${value//$'\r'/\\r}
    value=${value//$'\t'/\\t}
    printf '%s' "$value"
}

if [[ "$WRITE_CONTEXT" == "true" ]]; then
    if [[ -x "$SCRIPT_DIR/detect-project-context.sh" ]]; then
        "$SCRIPT_DIR/detect-project-context.sh" --write >/dev/null
    elif [[ -f "$SCRIPT_DIR/detect-project-context.sh" ]]; then
        bash "$SCRIPT_DIR/detect-project-context.sh" --write >/dev/null
    fi
fi

printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","FEATURE_SOURCE":"%s","HAS_GIT":"%s","PROJECT_CONTEXT":"%s"}\n' \
    "$(json_escape "$FEATURE_SPEC")" \
    "$(json_escape "$IMPL_PLAN")" \
    "$(json_escape "$FEATURE_DIR")" \
    "$(json_escape "$CURRENT_FEATURE")" \
    "$(json_escape "$FEATURE_SOURCE")" \
    "$(json_escape "$HAS_GIT")" \
    "$(json_escape "$PROJECT_CONTEXT")"
