# Safe setup on the shared RTX 2080 Ti server

1. At the moment provided (2026-11-02 10:29:57 local), GPUs 0/1/2/4/5/6 had active processes, and GPUs 3/7 appeared low load but still had ~522–592 MiB reserved. GPU utilization is only a snapshot; no GPU is guaranteed free.
2. Run preflight first; don't `kill`, `pkill`, `chmod -R`, change server drivers, or `sudo` anything.
3. Use a private conda environment inside your project folder; verify free disk space (raw image data ~5+ GB; experiment/caches can multiply that size). Put caches on available storage; do not silently write huge artifacts to home.
4. CPU-only preparation and TF-IDF baseline work even when all GPUs are busy.
5. For GPU stages, first inspect `nvidia-smi` again and seek permission under local sharing rules. Set `CUDA_VISIBLE_DEVICES=<authorized_gpu>` before launching. CUDA numbering in Python then starts from 0 within the visible list.
6. RTX 2080 Ti is Turing (sm75); use FP16 where supported rather than BF16. Installing a torch CUDA wheel should be done after inspecting Python, driver and dependency compatibility; do not assume arbitrary CUDA versions work.
7. Only bind API/MLflow dashboards to `127.0.0.1` and use SSH tunnel from workstation. Never open public ports on a shared GPU server without permission.
8. Work with synthetic traffic/metadata during serving demonstration; do not return real student images to public clients.

## Expected starter tree
```
mlops-k12-misconception/
├── configs/                  # hyperparameter and data-contract configs
├── data/
│   ├── raw/                 # immutable restricted source data (gitignored)
│   ├── downloads/           # received zip files (gitignored)
│   ├── interim/             # intermediate results (gitignored)
│   └── processed/           # split IDs and processed features (gitignored)
├── docs/                    # ADRs, gates, model cards, incident playbooks
├── notebooks/               # EDA only; promote verified methods into src/
├── src/k12mlops/            # testable reusable Python ML library
├── scripts/                 # reproducible CLI steps
├── tests/                   # unit/contract/integration tests
├── models/                  # local weights and preprocessors (gitignored)
├── reports/                 # metrics, provenance, charts (gitignored)
├── services/                # upcoming FastAPI app
├── monitoring/              # upcoming drift and alerts
├── deployments/             # upcoming docker / staging config
├── .github/workflows/       # CPU-only CI
├── pyproject.toml
└── README.md
```

## First exercise (do manually; reflect instead of copy/paste blindly)
- What is the role of each folder? Why do raw files belong in Gitignore?
- Run `python scripts/00_preflight.py`, inspect capacity and GPUs.
- Write what failure you would expect if sample_submission columns differ.
- Run `python -m pytest -q`, prove wrong MAP code gets detected by intentionally failing a test and reverting.
- Explain why group-question validation has a different target than the official student-disjoint Kaggle test.
