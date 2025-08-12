# Qcomm Traffic
This repository showcases an all-in-one script to simultaneously generate and simulate Qcomm-compatible circuit files of synthetic traffic and neural network workloads on multi-core quantum architectures. Synthetic traffics include: uniform, bit complement, bit reversal, bit shuffle, neighbour, transpose, hotspot, and butterfly. NN workloads include: quantum convolutional neural network (QCNN) and quantum auto encoder (QAE). Included is also a .txt to .csv script to convert the simulation outputs of these circuits into organized tables for data visualization and analysis.

The content in this repository was developed by [Sadit-J](https://github.com/Sadit-J), [danielpkot](https://github.com/danielpkot), [rahafalost](https://github.com/rahafalost), [justinthdang](https://github.com/justinthdang), and [Ewcw17](https://github.com/Ewcw17) as part of our Summer 2025 undergraduate research assistantship on quantum computing. Feel free to check out the results and findings from our research through [this paper]() we produced (currently in progress)!

## Generating and Simulating Circuits
Qcomm must first be set up locally before using the scripts in this repository. Please first refer to the installation and quick start guide from the [Qcomm repository](https://github.com/mpalesi/qcomm). Once Qcomm is set up, navigate to Traffic_generator.py. Change the path of the architecture.yaml file on **`line 36`** and the executable path of Qcomm on **`line 102`** accordingly to where Qcomm was installed.

To begin, run the Traffic_generator.py script. The user will first be prompted for the amount of gates, qubits, the probability of 1-qubit gates, and the probability of 2-qubit gates. The user can then choose to simulate all 10 traffics at once by clicking enter or just 1 specific traffic by typing in its name, followed by ".txt". The generated circuits can be found under the folder defined on **`line 96`**, while the simulation data can be found in the outputted file defined on **`line 106`**, which can both be edited to the user's liking.

## Converting Circuit Simulation Data From .txt to .csv
Simulate the circuits of variable parameters in sequential order (e.g., 1 LTM port, 2 LTM ports, ..., n LTM ports). txt_to_csv.py essentially reads the simulation data file and splits each circuit simulation into a list element. For each table of a single variable parameter, the user will be prompted a title for the parameter, and the start and end indexes of it in the list.

The program will continue to loop for more tables until the user presses the enter key when prompted a title for the parameter. The first column of the generated tables will contain the name of the variable parameter (e.g, LTM ports), while the following columns will contain the corresponding statistics (e.g., communication time, coherence, etc.,).

An example of how a single generated table would look like:

| LTM Ports | Communication Time | ... | Coherence |
|-----------|--------------------|-----|-----------|
| 1         | 1e-2               | ... | 3e-4      |
| 2         | 5e-6               | ... | 7e-8      |
| ...       | ...                | ... | ...       |
| n         | 9e-1               | ... | 2e-3      |

## Citations
Maurizio Palesi, Enrico Russo, Davide Patti, Giuseppe Ascia, and Vincenzo Catania, "_Assessing the Role of Communication in Scalable Multi-Core Quantum Architectures_," in _2024 IEEE 17th International Symposium on Embedded Multicore/Many-core Systems-on-Chip (MCSoC)_, Kuala Lumpur, Malaysia, 2024, pp. 482-489, doi: 10.1109/MCSoC64144.2024.00085.
