#!/usr/bin/env bash
# Non-destructive overlay installer. Does not modify source/tests/env/data/models.
set -euo pipefail
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
if [[ ! -f "$SOURCE/docs/enterprise/00_START_HERE.md" ]]; then
  echo "ERROR: overlay source not found; run script from extracted overlay/scripts" >&2
  exit 2
fi
DEST="${1:-/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01/mlops-k12-misconception}"
ALLOWED='/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01'
case "$DEST" in
  "$ALLOWED"/*) ;;
  *) echo "ERROR: target must be within $ALLOWED: $DEST" >&2; exit 2;;
esac
if [[ ! -d "$DEST" || ! -e "$DEST/pyproject.toml" ]]; then
  echo "ERROR: target is not an existing K12 project (missing pyproject.toml): $DEST" >&2
  exit 2
fi
DEST="$(cd "$DEST" && pwd -P)"
case "$DEST" in
  "$ALLOWED"/*) ;;
  *) echo "ERROR: resolved target escaped allowed root: $DEST" >&2; exit 2;;
esac
if [[ "$SOURCE" == "$DEST" ]]; then
  echo "ERROR: overlay source and project destination identical" >&2; exit 2
fi
created=0
skipped=0
while IFS= read -r -d '' src; do
  relative="${src#"$SOURCE"/}"
  target="$DEST/$relative"
  if [[ -e "$target" || -L "$target" ]]; then
    echo "SKIP existing: $relative"
    skipped=$((skipped+1))
    continue
  fi
  mkdir -p "$(dirname "$target")"
  parent_real="$(cd "$(dirname "$target")" && pwd -P)"
  case "$parent_real" in
    "$DEST"|"$DEST"/*) ;;
    *) echo "ERROR: symlink/parent escaped project root: $relative" >&2; exit 3;;
  esac
  cp -n "$src" "$target"
  echo "CREATE: $relative"
  created=$((created+1))
done < <(find "$SOURCE" -type f -print0)
printf 'Governance overlay installed: created=%s skipped=%s target=%s\n' "$created" "$skipped" "$DEST"
echo 'No code, dataset, cache, training job or Git remote was changed.'
