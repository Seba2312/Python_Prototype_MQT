# DD Playground

Einfacher Einstieg zur Nutzung des Decision-Diagram-Backends von MQT Core.

## Zweck

Dieses kleine Projekt bietet einen leichten Einstieg in die
Entscheidungsdiagramm-Simulation von `mqt.core`.
Es stellt Hilfsfunktionen sowie ein Notebook bereit, um mit
Beispielschaltkreisen zu experimentieren und dabei Statistiken des
Simulators zu sammeln.

### Gesammelte Statistiken

Pro angewendetem Gatter werden u.a. folgende Werte erfasst:

- **gate** – Name des ausgeführten Gatters
- **nodes** – Anzahl der DD-Knoten nach dem Gatter
- **edges** – Anzahl der Kanten im DD
- **runtime_ms** – Laufzeit des Gatters in Millisekunden
- **ram_MB** – aktueller Speicherverbrauch
- **peak_MB** – bisher gemessener Höchstverbrauch
- **fidelity** – optionaler Vergleich mit einer Referenzsimulation


## Quickstart

1. Python 3.11 installieren.
2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python3.11 -m venv venv
   source -venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   pip install -e .

   ```
4. Notebook starten:
   ```bash
   jupyter lab
   ```


## Notebook online starten

Das Notebook kann auch ohne lokale Installation über

im Browser geöffnet werden.

## Notebook ausführen

Das Notebook `notebooks/dd_playground.ipynb` enthält Beispiele für das
Laden und Simulieren von Quantenprogrammen. Eine kleine Auswahl an
QASM-Dateien liegt im Ordner `circuits/`.
