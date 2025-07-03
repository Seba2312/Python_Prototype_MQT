"""Wrapper around MQT Core to simulate quantum circuits using DDs.
Provides `run_circuit` for loading files and returning the final state."""

from __future__ import annotations

import time
from pathlib import Path
from typing import List, Tuple
from mqt.core import dd as _dd

from mqt.core import dd

try:
    import numpy as np
except Exception:
    np = None

try:
    import psutil
except Exception:
    psutil = None

try:
    from mqt.core.ir import QuantumComputation
    import mqt.core.dd
except Exception:
    mqt = None

from . import instrumentation, utils

_ddpkg = _dd.DDPackage()


def _gate_matrix(op):
    """2×2 or 4×4 NumPy unitary for the given Operation."""
    k = op.num_targets
    mat_dd = _ddpkg.from_operation(op)
    return np.asarray(mat_dd.get_matrix(k), copy=False)


def _embed_gate(U, targets, n):
    """Embed a k-qubit gate matrix U acting on 'targets' into n-qubit space."""
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



def _fidelity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Return |⟨a|b⟩|² divided by both ‖·‖² (always ∈[0,1])."""
    norm_a = np.vdot(vec_a, vec_a).real
    norm_b = np.vdot(vec_b, vec_b).real
    if norm_a == 0 or norm_b == 0:
        return 0.0
    overlap = abs(np.vdot(vec_a, vec_b)) ** 2
    return float(overlap / (norm_a * norm_b))


class DDSimulator:
    """Minimal wrapper for the MQT Core DD simulator."""

    def __init__(self, qc: QuantumComputation) -> None:
        """Initialize the simulator with a given quantum circuit."""
        self.qc = qc
        self.dd = dd.DDPackage(qc.num_qubits)
        self.state = self.dd.zero_state(qc.num_qubits)
        self.proc = psutil.Process()
        self.log: List[instrumentation.Statistics] = []
        self.peak_ram = 0.0

        self.ref_vec = None
        if np is not None and qc.num_qubits <= 8:
            self.ref_vec = np.zeros(2 ** qc.num_qubits, complex)
            self.ref_vec[0] = 1

    def _apply_single_op(self, op) -> None:
        """Simulate one operation and collect statistics."""
        if not op.is_unitary():
            return

        start = time.perf_counter()
        new_state = self.dd.apply_unitary_operation(self.state, op)
        runtime = time.perf_counter() - start
        self.dd.garbage_collect()

        stats = instrumentation.collect_statistics(
            self.dd, new_state, str(op), runtime, self.proc
        )

        if self.ref_vec is not None:
            n = self.qc.num_qubits
            U_small = _gate_matrix(op)
            U_full = _embed_gate(U_small, list(op.targets), n)
            ref_next = U_full @ self.ref_vec

            vec_dd = np.asarray(new_state.get_vector(), copy=False)
            fidelity = _fidelity(ref_next, vec_dd)
            stats.fidelity = fidelity
            self.ref_vec = ref_next
        self.peak_ram = max(self.peak_ram, stats.ram_MB)
        stats.peak_MB = self.peak_ram
        self.log.append(stats)
        self.state = new_state

    def run(
            self
    ) -> Tuple[List[instrumentation.Statistics], "mqt.core.dd.VectorDD"]:
        """Execute all operations in the circuit and return statistics."""

        if mqt is None:
            raise RuntimeError("mqt.core is not installed")

        for op in self.qc:
            self._apply_single_op(op)

        return self.log, self.state


def run_circuit(
        path: str | Path,

        log_path: str | Path | None = None,
) -> Tuple[List[instrumentation.Statistics], "mqt.core.dd.VectorDD"]:
    """Convenience wrapper to load and run an OpenQASM circuit."""

    qc = utils.load_qasm(path)
    sim = DDSimulator(qc)

    return sim.run()
