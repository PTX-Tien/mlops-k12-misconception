#!/usr/bin/env bash
# Source this file before using conda, pip, Kaggle, Hugging Face, or any other project tooling:
#   source scripts/00_private_runtime.sh
# Do NOT execute via `bash scripts/00_private_runtime.sh`: exports must persist in this shell.

if [ -z "${BASH_VERSION:-}" ]; then
  echo 'ERROR: This file must be sourced from bash.' >&2
  return 1 2>/dev/null || exit 1
fi

_MLOPS_SETUP_SCRIPT="${BASH_SOURCE[0]}"
_MLOPS_SETUP_DIR="$(cd "$(dirname "$_MLOPS_SETUP_SCRIPT")" && pwd -P)" || return 1
export MLOPS_PROJECT="$(cd "$_MLOPS_SETUP_DIR/.." && pwd -P)" || return 1
export MLOPS_USER_ROOT='/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01'

case "$MLOPS_PROJECT/" in
  "$MLOPS_USER_ROOT/"*) ;;
  *) echo "ERROR: Project must reside beneath $MLOPS_USER_ROOT (found $MLOPS_PROJECT)" >&2; return 1 ;;
esac

export MLOPS_RUNTIME="$MLOPS_PROJECT/.runtime"
export CONDA_PKGS_DIRS="$MLOPS_RUNTIME/conda-pkgs"
export CONDA_ENVS_PATH="$MLOPS_RUNTIME/conda-envs"
export XDG_CACHE_HOME="$MLOPS_RUNTIME/cache"
export XDG_CONFIG_HOME="$MLOPS_RUNTIME/config"
export XDG_DATA_HOME="$MLOPS_RUNTIME/data"
export XDG_STATE_HOME="$MLOPS_RUNTIME/state"
export TMPDIR="$MLOPS_RUNTIME/tmp"
export TMP="$TMPDIR"
export TEMP="$TMPDIR"
export PIP_CACHE_DIR="$XDG_CACHE_HOME/pip"
export HF_HOME="$XDG_CACHE_HOME/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"
export HF_DATASETS_CACHE="$HF_HOME/datasets"
export HF_ASSETS_CACHE="$HF_HOME/assets"
export TORCH_HOME="$XDG_CACHE_HOME/torch"
export CUDA_CACHE_PATH="$XDG_CACHE_HOME/nv/ComputeCache"
export TRITON_CACHE_DIR="$XDG_CACHE_HOME/triton"
export MPLCONFIGDIR="$XDG_CONFIG_HOME/matplotlib"
export NUMBA_CACHE_DIR="$XDG_CACHE_HOME/numba"
export JOBLIB_TEMP_FOLDER="$TMPDIR/joblib"
export WANDB_DIR="$MLOPS_RUNTIME/logs/wandb"
export WANDB_CACHE_DIR="$XDG_CACHE_HOME/wandb"
export UV_CACHE_DIR="$XDG_CACHE_HOME/uv"
export KAGGLE_CONFIG_DIR="$XDG_CONFIG_HOME/kaggle"
export KAGGLEHUB_CACHE="$XDG_CACHE_HOME/kagglehub"
export PYTHONUSERBASE="$MLOPS_RUNTIME/python-userbase"
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

# A project-local conda config prevents accidental conda config writes to HOME.
export CONDARC="$XDG_CONFIG_HOME/condarc"

mkdir -p \
  "$CONDA_PKGS_DIRS" "$CONDA_ENVS_PATH" \
  "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME" \
  "$TMPDIR" "$PIP_CACHE_DIR" "$HF_HOME" "$HF_HUB_CACHE" \
  "$HF_DATASETS_CACHE" "$HF_ASSETS_CACHE" "$TORCH_HOME" \
  "$CUDA_CACHE_PATH" "$TRITON_CACHE_DIR" "$MPLCONFIGDIR" \
  "$NUMBA_CACHE_DIR" "$JOBLIB_TEMP_FOLDER" "$WANDB_DIR" \
  "$WANDB_CACHE_DIR" "$UV_CACHE_DIR" "$KAGGLE_CONFIG_DIR" \
  "$KAGGLEHUB_CACHE" "$PYTHONUSERBASE" || return 1
chmod 700 "$MLOPS_RUNTIME" "$KAGGLE_CONFIG_DIR" || return 1

if [ ! -f "$CONDARC" ]; then
  printf 'pkgs_dirs:\n  - %s\nenvs_dirs:\n  - %s\n' \
    "$CONDA_PKGS_DIRS" "$CONDA_ENVS_PATH" > "$CONDARC" || return 1
fi

printf 'Private runtime enabled for: %s\nConda packages: %s\nPip cache: %s\nTemporary files: %s\n' \
  "$MLOPS_PROJECT" "$CONDA_PKGS_DIRS" "$PIP_CACHE_DIR" "$TMPDIR"

unset _MLOPS_SETUP_SCRIPT _MLOPS_SETUP_DIR
