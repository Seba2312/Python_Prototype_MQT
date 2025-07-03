OPENQASM 2.0;
include "qelib1.inc";

// Grover with n = 2, marks state |11>
qreg q[2];
creg c[2];

// initialise equal superposition
h q[0];
h q[1];

// oracle O |11> = -|11>
cz q[0], q[1];

// diffusion (inversion about the mean)
h q[0];
h q[1];
x q[0];
x q[1];
h q[1];
cx q[0], q[1];
h q[1];
x q[0];
x q[1];

// measure result
measure q -> c;
