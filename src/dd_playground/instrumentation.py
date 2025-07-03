"""Instrumentation helpers for measuring DD statistics.
Provides hooks collecting simple runtime metrics."""

from __future__ import annotations

from dataclasses import dataclass

try:
    import psutil
except Exception:
    psutil = None

try:
    from mqt.core.dd import DDPackage, VectorDD
except Exception:
    DDPackage = VectorDD = None

@dataclass
class Statistics:
    """Container for simple simulation statistics."""

    nodes: int = 0
    edges: int = 0
    gate: str = ""
    runtime_ms: float = 0.0
    ram_MB: float = 0.0
    peak_MB: float = 0.0
    fidelity: float | None = None

def collect_statistics(
    dd_package: DDPackage,
    state: VectorDD,
    gate: str,
    runtime_s: float,
    process: psutil.Process | None,
) -> Statistics:
    """Collect decision diagram statistics after applying a gate."""

    nodes = state.size()
    edges = getattr(dd_package, "num_edges", 2 * nodes)
    ram = process.memory_info().rss / 1_048_576 if psutil is not None else 0.0

    return Statistics(
        nodes=nodes,
        edges=edges,
        gate=gate,
        runtime_ms=runtime_s * 1000.0,
        ram_MB=ram,
    )

def install_playground_hook(dd_package: DDPackage, callback) -> None:
    """Expose a hook for experimenting with custom reduction rules."""

    if hasattr(dd_package, "set_reduce_callback"):
        dd_package.set_reduce_callback(callback)
