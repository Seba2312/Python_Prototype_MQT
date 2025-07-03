from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import matplotlib.pyplot as plt

from . import simulator
from .reference_comparison import run_statevector



"""Helpers to benchmark different simulator implementations and plot results."""

def benchmark_circuits(circuits: Iterable[str | Path]) -> pd.DataFrame:
    """Run each circuit with both implementations and collect runtimes.
    Returns a DataFrame with circuit name, implementation and runtime."""
    records: list[dict[str, object]] = []

    for path in circuits:
        cpath = Path(path)
        stats_dd, _ = simulator.run_circuit(cpath)
        runtime_dd = sum(s.runtime_ms for s in stats_dd)
        records.append({"circuit": cpath.stem, "impl": "DD", "runtime_ms": runtime_dd})

        try:
            stats_sv, _ = run_statevector(cpath)
        except Exception:
            continue
        runtime_sv = sum(d["runtime_s"] * 1000.0 for d in stats_sv)
        records.append({"circuit": cpath.stem, "impl": "StateVector", "runtime_ms": runtime_sv})

    return pd.DataFrame.from_records(records)


def plot_runtime_bars(df: pd.DataFrame) -> None:
    """Display a bar chart comparing runtimes from :func:`benchmark_circuits`."""
    pivot = df.pivot(index="circuit", columns="impl", values="runtime_ms")
    ax = pivot.plot(kind="bar")
    ax.set_xlabel("circuit")
    ax.set_ylabel("runtime [ms]")
    plt.tight_layout()
    plt.show()


def compare_logs(
    log_dd: Iterable[object], log_sv: Iterable[object]
) -> pd.DataFrame:
    """Merge per-gate statistics from both implementations.
    Returns a DataFrame with a gate index and implementation column."""

    df_dd = pd.DataFrame(getattr(s, "__dict__", s) for s in log_dd).copy()
    df_dd["impl"] = "DecisionDiagram"
    df_dd["gate_idx"] = range(len(df_dd))

    df_sv = pd.DataFrame(getattr(s, "__dict__", s) for s in log_sv).copy()
    if "runtime_s" in df_sv.columns:
        df_sv["runtime_ms"] = df_sv["runtime_s"] * 1000.0
        df_sv = df_sv.drop(columns=["runtime_s"])
    df_sv["impl"] = "StateVector"
    df_sv["gate_idx"] = range(len(df_sv))

    return pd.concat([df_dd, df_sv], ignore_index=True)


def plot_node_bars(df: pd.DataFrame, column: str = "nodes") -> None:
    """Plot side-by-side bar charts for the given metric per gate."""

    pivot = df.pivot(index="gate_idx", columns="impl", values=column)
    ax = pivot.plot(kind="bar")
    ax.set_xlabel("gate index")
    ax.set_ylabel(column)
    plt.tight_layout()
    plt.show()
