"""Internal build modules; use scripts/manage.py for command-line tasks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
