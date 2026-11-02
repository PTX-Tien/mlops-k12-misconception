#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for d in data/raw data/downloads data/interim data/processed models reports logs notebooks services monitoring deployments; do
  mkdir -p "$ROOT/$d"
done
printf 'Workspace: %s\n' "$ROOT"
printf 'No files were overwritten; no GPU jobs were launched.\n'
