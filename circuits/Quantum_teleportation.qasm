OPENQASM 2.0;
include "qelib1.inc";

// Teleport one arbitrary qubit state from q0 to q2
qreg q[3];
creg c[3];

// prepare an arbitrary single–qubit state, for example |ψ> = |1>
x q[0];

// create Bell pair between q1 and q2
h q[1];
cx q[1], q[2];

// Bell-measurement on q0 and q1
cx q[0], q[1];
h q[0];
measure q[0] -> c[0];
measure q[1] -> c[1];

// classically controlled corrections
if (c[1] == 1) { x q[2]; }
if (c[0] == 1) { z q[2]; }

// verify
measure q[2] -> c[2];
