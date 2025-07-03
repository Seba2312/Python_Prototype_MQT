OPENQASM 2.0;
include "qelib1.inc";

// 5-qubit Quantum Fourier Transform (QFT)
qreg q[5];
creg c[5];

/* optional: prepare an input basis state, e.g.
x q[0];
x q[1];
x q[2];
x q[3];
x q[4];
*/

// stage 1  – qubit 4
h  q[4];
cs q[4], q[3];        // controlled-S   (phase π/2)
ct q[4], q[2];        // controlled-T   (phase π/4)
cp(pi/8)  q[4], q[1]; // controlled-R₃ (phase π/8)
cp(pi/16) q[4], q[0]; // controlled-R₄ (phase π/16)
barrier q;

// stage 2  – qubit 3
h  q[3];
cs q[3], q[2];
ct q[3], q[1];
cp(pi/8)  q[3], q[0];
barrier q;

// stage 3  – qubit 2
h  q[2];
cs q[2], q[1];
ct q[2], q[0];
barrier q;

// stage 4  – qubit 1
h  q[1];
cs q[1], q[0];
barrier q;

// stage 5  – qubit 0
h  q[0];
barrier q;

// swap to reverse qubit order
swap q[0], q[4];
swap q[1], q[3];

// read-out
measure q -> c;
