#!/bin/bash
# Push local changes to a GitHub repository.
# Usage: ./scripts/push_to_github.sh "commit message" [remote-url]
set -euo pipefail

commit_msg=${1:-"Update"}
repo_url=${2-}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository" >&2
  exit 1
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "$commit_msg"
fi

if [ -n "$repo_url" ]; then
  if ! git remote | grep -q '^origin$'; then
    git remote add origin "$repo_url"
  fi
fi

# Default branch is main
git push origin main
