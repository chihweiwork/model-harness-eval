import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "fixtures"
RESULTS_DIR = Path(os.environ.get("BENCH_RESULTS_DIR", ROOT / "results")).resolve()
