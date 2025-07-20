# DD Playground

A practical introduction to the decision‑diagram simulation backend of **MQT Core**.

## Purpose

This small project makes it easy to get started with decision‑diagram simulation using `mqt.core`. It provides helper functions and a Jupyter notebook so you can experiment with sample circuits while collecting statistics from the simulator.

### Collected statistics

For every gate executed, the following values are recorded:

* **gate** – name of the executed gate  
* **nodes** – number of nodes in the decision diagram after the gate  
* **edges** – number of edges in the decision diagram  
* **runtime_ms** – runtime of the gate in milliseconds  
* **ram_MB** – current main‑memory usage  
* **peak_MB** – peak memory usage measured so far  
* **fidelity** – optional comparison with a reference simulation  

## Quickstart

1. Install Python3.11.  
2. Create and activate a virtual environment:

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
   ```
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. Start the notebook:

   ```bash
   jupyter lab
   ```

## Run the notebook online

You can open the notebook directly in your browser—no local installation required:

<https://mybinder.org/v2/gh/Seba2312/Python_Prototype_MQT/HEAD?urlpath=lab>

## Working with the notebook

The notebook `notebooks/dd_playground.ipynb` demonstrates how to load and simulate quantum programs. A small selection of QASM files is located in the `circuits/` folder.


## Citation

```bibtex
@article{burgholzer2025MQTCore,
    title     = {{{MQT Core}}: {{The}} Backbone of the {{Munich Quantum Toolkit (MQT)}}},
    author    = {Lukas Burgholzer and Yannick Stade and Tom Peham and Robert Wille},
    year      = {2025},
    journal   = {Journal of Open Source Software},
    publisher = {The Open Journal},
    volume    = {10},
    number    = {108},
    pages     = {7478},
    doi       = {10.21105/joss.07478},
    url       = {https://doi.org/10.21105/joss.07478},
}
```

## Further information

Detailed documentation for **MQT Core** is available at  
<https://github.com/munich-quantum-toolkit/core?tab=readme-ov-file>

More example decision‑diagram visualisations can be explored and manually added to `circuits/` from
<https://www.cda.cit.tum.de/app/ddvis/>