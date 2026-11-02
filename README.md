# K12 Misconception Detection — End-to-End MLOps Learning Lab

> Educational, learning-first project: understand each gate before automating it. Do NOT
> redistribute children's handwritten work, competition data, or models trained on it.

## Problem
Predict `root_code` (one of 75 misconception codes) or `NONE` from a **photo of a student's handwritten math working** plus question context. The official competition measures MAP@3. The training set includes a privileged `transcription_steps` field; the **test and serving requests do not**. Never train a deployed classifier directly on this field unless an OCR/transcription subsystem exists in inference.

Read: https://www.kaggle.com/competitions/misconception-detection-in-k-12-student-math-workings/overview
Data terms mirror: https://huggingface.co/datasets/colearnlab/misconception-detection
Background: https://ml-ops.org/content/three-levels-of-ml-software
MLOps maturity: https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

## Start on server (copy archive using scp first)
```bash
ROOT=/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01/mlops-k12-misconception
mkdir -p "$ROOT"
tar -xzf /path/to/mlops_k12_learning_kit.tar.gz -C "$ROOT" --strip-components=1
cd "$ROOT"
bash scripts/01_init_workspace.sh
git init -b main
python scripts/00_preflight.py
cat reports/preflight.json
```
No connection to the server is provided to the assistant, so **you** run the commands above.

## Environment (after preflight passes)
```bash
conda create -p "$PWD/.conda" python=3.11 -y
conda activate "$PWD/.conda"
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
python -m pytest -q
python -m ruff check src tests
python -m pip freeze > reports/environment-installed.txt
```
If `conda activate` fails, run `conda init bash`, start a new shell, or use `source $(conda info --base)/etc/profile.d/conda.sh` before activating. Do not alter the base environment. Do not install torch until you choose an actual image model.

## Download data only after agreeing to the official competition rules
```bash
python -m pip install kaggle
# First accept rules on Kaggle. Authenticate via `kaggle auth login --no-launch-browser` or a protected token file.
# Do not print, paste or commit your token.
kaggle competitions download -c misconception-detection-in-k-12-student-math-workings -p data/downloads
ls -lh data/downloads
# Inspect archive structure and disk quota, then unzip into data/raw (not into Git):
unzip -l data/downloads/*.zip | head -30
unzip -q data/downloads/*.zip -d data/raw
python scripts/02_dataset_audit.py --data-dir data/raw --image-sample 12
cat reports/data_audit.json
```
If the archive has a wrapper folder, move the dataset **within** `data/raw` so `train.csv`, `test.csv`, `sample_submission.csv` and `images/` are under `data/raw/`. Do not copy these into Git, chat messages or external model APIs. Check the exact Kaggle rules about external compute.

## Learning gate sequence (DO NOT skip)
| Gate | What to learn | Artifact | Acceptance |
|---|---|---|---|
| G0 | Business vs ML objective, scope and privacy | `docs/01_problem_framing.md` | Sign off requirements, understand restrictions |
| G1 | Infrastructure preflight; isolated env; Git | `reports/preflight.json`, Git commit | No shared GPU disruption; tests pass |
| G2 | Ingestion, provenance, contracts, EDA | `reports/data_audit.json`, EDA notes | CSVs/images valid, data leakage threats documented |
| G3 | Validation design, leakage, MAP@3 | `data/processed/split.csv` | No ID overlap, group split verified, metric tests pass |
| G4 | Baseline with available-at-serving metadata | `models/baseline.joblib`, metrics | Reproducible run, no privileged field leakage |
| G5 | Working-aware model: OCR/vision feature extraction + classifier | versioned features | Test inference without `transcription_steps` works |
| G6 | Compare model candidates, calibration, robustness, confidence | evaluation/error analysis | Improvement beyond G4 without test leakage |
| G7 | Version data and runs | DVC manifests + MLflow runs | Run re-created from fixed code/data/config |
| G8 | Pipeline orchestration | DAG, Prefect flow | Idempotent repeat, cache, retry, failure report |
| G9 | Test + registry + approval gates | model registry, model card | Rejected unsafe/regressing model cannot promote |
| G10 | Batch inference and REST API | API + smoke tests | Serving parity, latency and schema tests pass |
| G11 | CI/CD | PR tests + safe staging release | Automatic code tests, no auto deployment on shared GPU |
| G12 | Monitoring & controlled CT | data drift & incident report | Simulated drift → human-approved retrain or rollback |

Read `docs/LEARNING_PLAN.md` for exact step-level learning objectives, pitfalls and exit criteria.

## First baseline execution (ONLY after data audit and split review)
```bash
python scripts/03_make_split.py --data-dir data/raw --test-size 0.20 --seed 42
python scripts/04_train_baseline.py --data-dir data/raw --split data/processed/split.csv
python scripts/05_predict_submission.py --data-dir data/raw --model models/baseline.joblib
cat reports/baseline_metrics.json
```
The baseline intentionally **does not look at the handwritten working**. It is a wiring/reproducibility baseline, not a competitive misconception detector. You will build a real image/OCR-enabled pipeline at G5. The official `test.csv` is never used for model selection.

## Key safety rules
- Use only competition-allowed data/model use; no public deployment of private competition data or trained models without permission.
- No photographing or redistributing identifiable student work; no student identification.
- No `transcription_steps`, `clean`, `final_answer_correct`, `misconceptions`, or target in serving feature set.
- Never run `nvidia-smi` output as proof a GPU will remain idle; inspect again before jobs and set `CUDA_VISIBLE_DEVICES` explicitly.
- Don't store Kaggle credentials in Git or a shared console log.
- Do not run GPU CI jobs on the shared server without permission/scheduling.
