# Standards crosswalk / references (verified public sources)

> This handbook is an **educational operating model**, not a claim that every company follows one identical process. Specs and target thresholds must be contextualized by your organization and license.

## Reference mapping
- [Three Levels of ML Software](https://ml-ops.org/content/three-levels-of-ml-software): Data, Model, Code; data ingestion/wrangling/split; training/evaluation/testing/packaging; serving/logging/monitoring.
- [Google Cloud MLOps level 0–2](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning): manual, pipeline automation/CT, CI/CD; data/model validation.
- [GitHub Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): required reviews and status checks; configured branch protection enforces, AI reviewer does not.
- [GitHub PR governance](https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests): issue/PR templates, code owners, review standards.
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry): lineage, immutable versions, alias `champion`, tags, rollback.
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking/): log params, metrics, artifacts, metadata.
- [Kaggle challenge page](https://www.kaggle.com/competitions/misconception-detection-in-k-12-student-math-workings/overview): verify competition details, rules and data schema before running jobs.

## Level mapping
| Level | Learning gates | Evidence |
|---|---|---|
| Level 0 manual | G0–G6 | scripts executed under pinned data/config; clear human review |
| Level 1 ML pipeline automation | G7–G10 + G12 (controlled CT) | DVC DAG, orchestration, registry with validation; do not auto-promote |
| Level 2 CI/CD | G11–G12 | PR checks, review, staged controlled release, monitoring + rollback |

MLOps **levels 0–2** are NOT the same as **Data/Model/Code** assets; both taxonomies are used in parallel.
