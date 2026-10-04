"""Run the unchanged original computations and make failed checks fatal."""
from pathlib import Path
import json
import platform
import subprocess
import sys


def main():
    import numpy
    import scipy

    root = Path(__file__).resolve().parent.parent
    results = root / "results"
    results.mkdir(parents=True, exist_ok=True)
    environment = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "operating_system": platform.system(),
        "architecture": platform.machine(),
        "seed": 20261001,
    }
    (results / "environment.json").write_text(
        json.dumps(environment, indent=2) + "\n", encoding="utf-8"
    )
    subprocess.run(
        [sys.executable, "-u", str(root / "scripts/completeness_checks.py")],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(root / "scripts/verify_results.py")],
        cwd=root,
        check=True,
    )
    print("All eleven computational checks reproduced and verified.")


if __name__ == "__main__":
    main()
