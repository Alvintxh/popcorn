from __future__ import annotations

from pathlib import Path


def load_qss(filename: str) -> str:
    # Allow keeping style.qss at repo root for easy tweaking
    root = Path(__file__).resolve().parents[3]
    qss_path = root / filename
    if qss_path.exists():
        return qss_path.read_text(encoding="utf-8")

    # Fallback: relative to this file
    qss_path = Path(__file__).resolve().parent / filename
    return qss_path.read_text(encoding="utf-8")
