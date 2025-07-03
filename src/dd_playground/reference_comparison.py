from __future__ import annotations
import time
from pathlib import Path
from typing import List, Tuple
import numpy as np
import psutil

from mqt.core.ir import QuantumComputation
from mqt.core import dd as _dd

_ddpkg = _dd.DDPackage()
def _gate_matrix(op) -> np.ndarray:
    """Dense unitary for 1- or 2-qubit operations."""
    mat_dd = _ddpkg.from_operation(op)
    k = op.num_targets
    return np.asarray(mat_dd.get_matrix(k), copy=False)


def _embed_gate(U: np.ndarray, targets: List[int], n: int) -> np.ndarray:
    """Embed a unitary acting on the target qubits into the full n-qubit space."""
    targets = sorted(targets)
    k = len(targets)
    full = np.array([[1]], dtype=complex)
    t_idx = 0

    for q in range(n):
        if t_idx < k and q == targets[t_idx]:
            if t_idx == 0:
                full = np.kron(full, U)
            t_idx += 1
            continue
        full = np.kron(full, np.eye(2))
    return full


def run_statevector(qasm_path: str | Path) -> Tuple[List[dict], np.ndarray]:
    """Simulate the circuit using NumPy as a reference state-vector simulator."""
    qc = QuantumComputation.from_qasm(str(qasm_path))

    if qc.num_qubits > 8:
        raise ValueError("Reference simulator ist auf acht Qubits begrenzt")

    state = np.zeros(2 ** qc.num_qubits, complex)
    state[0] = 1.0

    proc  = psutil.Process()
    peak  = 0.0
    stats = []

    for op in qc:
        if not op.is_unitary():
            continue
        U = _embed_gate(_gate_matrix(op), list(op.targets), qc.num_qubits)
        t0 = time.perf_counter()
        state = U @ state
        runtime = time.perf_counter() - t0

        ram  = proc.memory_info().rss / 1e6
        peak = max(peak, ram)
        stats.append(
            dict(
                gate=str(op),
                runtime_s=runtime,
                nodes=2 ** qc.num_qubits,
                edges=2 ** qc.num_qubits,
                ram_MB=ram,
                peak_MB=peak,
                fidelity="1.0, as compared with itself",
            )
        )
    return stats, state

