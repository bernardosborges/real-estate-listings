import os
import subprocess
import sys
from pathlib import Path

# You must run python .\scripts-dev\lint.py for resolving PYTHONPATH


def main():
    # Add project root to the PYTHONPATH
    project_root = Path(__file__).parent.parent
    env = {**os.environ, "PYTHONPATH": str(project_root)}

    # Run Pylint in app/
    target = sys.argv[1] if len(sys.argv) > 1 else "app"
    subprocess.run([sys.executable, "-m", "pylint", target], env=env, check=False)


if __name__ == "__main__":
    main()
