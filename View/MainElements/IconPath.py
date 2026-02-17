"""
Provides a single, centralized way to access icon files throughout the entire application.
"""
from pathlib import Path


def icon(name) -> str:
    icon_path = Path(__file__).resolve().parents[1] / "Icons"
    path = icon_path / name
    if not path.exists():
        print(f"Missing icon: {path}")
    return str(path)