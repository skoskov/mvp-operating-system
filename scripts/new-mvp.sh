#!/usr/bin/env bash
set -euo pipefail

# Create a new idea-to-MVP project under the DEV root using the MVP Operating System template.
# Usage:
#   ./scripts/new-mvp.sh relationship-agent-mvp
# Optional env:
#   DEV_ROOT=/mnt/c/Users/skoskov/Documents/_DEV
#   GITHUB_VISIBILITY=private|public|internal
#   PUSH_TO_GITHUB=1|0

PROJECT_NAME="${1:-}"
DEV_ROOT="${DEV_ROOT:-/mnt/c/Users/skoskov/Documents/_DEV}"
VISIBILITY="${GITHUB_VISIBILITY:-private}"
PUSH_TO_GITHUB="${PUSH_TO_GITHUB:-1}"

if [[ -z "$PROJECT_NAME" ]]; then
  echo "Usage: $0 <project-name>" >&2
  exit 1
fi

if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "Invalid project name: $PROJECT_NAME" >&2
  echo "Use only letters, numbers, dot, underscore, hyphen." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$OS_ROOT/template/mvp-project-template"
PROJECT_DIR="$DEV_ROOT/$PROJECT_NAME"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template not found: $TEMPLATE_DIR" >&2
  exit 1
fi

mkdir -p "$DEV_ROOT"
if [[ -e "$PROJECT_DIR" ]]; then
  echo "Project already exists: $PROJECT_DIR" >&2
  echo "Open it in Codex and run bootstrap/recovery from there." >&2
  exit 2
fi

cp -R "$TEMPLATE_DIR" "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Keep placeholder files out of the first commit only if they are empty scaffolding.
find . -name ".gitkeep" -type f -delete || true

if [[ ! -f README.md ]]; then
  cat > README.md <<EOF
# $PROJECT_NAME

MVP project initialized from mvp-operating-system template.

## Operating flow

Use the mvp-operating-system skill before implementation:
memory preflight → decision cards → token budget → OpenSpec → independent review → Codex implementation → verification → learning update.
EOF
fi

if [[ ! -f .gitignore ]]; then
  cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.env
.env.*
.DS_Store
.vscode/
.idea/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
node_modules/
EOF
fi

git init >/dev/null
git branch -M main

git add .
git commit -m "Initial MVP operating system bootstrap" >/dev/null

echo "Created local Git repo: $PROJECT_DIR"
echo "Branch: main"

if [[ "$PUSH_TO_GITHUB" == "1" ]]; then
  if command -v gh >/dev/null 2>&1; then
    if gh auth status >/dev/null 2>&1; then
      gh repo create "$PROJECT_NAME" --"$VISIBILITY" --source=. --remote=origin --push
      echo "GitHub repo created and pushed: $PROJECT_NAME ($VISIBILITY)"
    else
      echo "GitHub CLI is installed but not authenticated. Run: gh auth login" >&2
      echo "Local repo is ready. GitHub push skipped." >&2
    fi
  else
    echo "GitHub CLI not found. Local repo is ready. GitHub push skipped." >&2
  fi
fi

echo "Next: open $PROJECT_DIR in Codex App and choose Worktree for the first implementation slice."
