"""Utility functions for the DD Playground.
Simple helpers used across the notebook and simulation code."""

from __future__ import annotations

import pathlib
from pathlib import Path

try:
    from mqt.core import QuantumComputation
except Exception:
    QuantumComputation = None


def load_qasm(path: str | pathlib.Path) -> "QuantumComputation":
    """Load an OpenQASM file and return the parsed circuit."""

    qc_path = Path(path)
    if not qc_path.is_file():
        raise FileNotFoundError(qc_path)

    if QuantumComputation is None:
        raise RuntimeError("mqt.core is not installed")

    return QuantumComputation.from_qasm(str(qc_path))
