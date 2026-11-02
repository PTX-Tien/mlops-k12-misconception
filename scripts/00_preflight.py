#!/usr/bin/env python3
"""Read-only preflight. Does not allocate GPU memory or install anything."""
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "preflight.json"


def command(args: list[str], timeout: int = 12) -> dict:
    try:
        p = subprocess.run(args, text=True, capture_output=True, timeout=timeout, check=False)
        return {"exit_code": p.returncode, "stdout": p.stdout.strip()[:10000], "stderr": p.stderr.strip()[:2000]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"error": str(exc)}


def main() -> None:
    disk = shutil.disk_usage(ROOT)
    report = {
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "workspace": str(ROOT),
        "user": os.environ.get("USER", "unknown"),
        "hostname": platform.node(),
        "python": sys.version,
        "os": platform.platform(),
        "disk_bytes": {"total": disk.total, "used": disk.used, "free": disk.free},
        "git": command(["git", "--version"]),
        "conda": command(["conda", "--version"]),
        "gpu_status": command([
            "nvidia-smi", "--query-gpu=index,name,memory.total,memory.used,utilization.gpu,temperature.gpu",
            "--format=csv,noheader,nounits"
        ]),
        "cuda_driver": command(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"]),
        "quota_if_supported": command(["quota", "-s"], timeout=5),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"Disk free: {disk.free / 1024**3:.2f} GiB")
    print("Read-only: no training, installs, downloads, GPU allocation or process termination.")


if __name__ == "__main__":
    main()
