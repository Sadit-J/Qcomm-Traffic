from bitlist import bitlist
from Network import Network, Node
import math
import random
import subprocess
from UniformGen import uniformGen 
from ComplementGen import complementGen
from ReversalGen import reversalGen
from ShuffleGen import shuffleGen
from NearestNeighbourGen import neighbourGen
from TransposeGen import transposeGen
from Hotspot import hotspotGen, generate_hotspot_gates
from Butterfly import butterflyGen
from QCNN import qcnnGen
# from QAE import qaeGen

def createNetwork(nodes_num, qubits_per, total_qubits):
    node_list = []
    iteration = 0
    leftover_qubits = total_qubits

    for i in range(nodes_num):
        node_list.append(Node(i, 0, 4))

    while (leftover_qubits > 0):
        node_list[iteration % 16].add_qubits(1)
        iteration += 1
        leftover_qubits -= 1


    current_network = Network(node_list, qubits_per, total_qubits)    
    return current_network

def getUserInput():
    # read and extract parameters from architecture.txt
    arch = open("architecture.txt", "r")
    read_arch = arch.readlines()
    mesh_x = int(read_arch[0].strip("mesh_x "))
    mesh_y = int(read_arch[1].strip("mesh_y "))

    number_of_cores = mesh_x * mesh_y
    qubits_per_core = int(read_arch[3].strip("qubits_per_core "))
    number_of_qubits = qubits_per_core * number_of_cores
    number_of_gates = int(input("Number of gates: "))

    usable_qubits = number_of_qubits # initializes variable for while loop

    while usable_qubits >= number_of_qubits:
        usable_qubits = int(input(f"Number of logical qubits (must be <{number_of_qubits} qubits): "))

    probabilities = [] # initialize list for storing probabilities
    total_prob = 0 # initialize total probability tracker
    n = 1 # initialize count for n-qubits
    
    # loops until total probability equals 1 or the number probabilities exceeds the number of gates
    while total_prob != 1 and n <= number_of_gates:
        n_qubit_gate_prob = float(input(f"{n}-qubit gate probability: "))

        if not (0 <= n_qubit_gate_prob <= 1):
            print(f"{n}-qubit gate probability must be less between or equal to 0 and 1.")
            return
        
        # increment
        total_prob += n_qubit_gate_prob
        n += 1
        
        if total_prob > 1:
            print("Total probability must be 0 or 1.")
            return
        
        probabilities.append(n_qubit_gate_prob) # add probability to list

    # ask user for the name of the file the generated circuit will be outputted on
    patterns = ["uniform.txt", "complement.txt", "reversal.txt", "shuffle.txt", "neighbour.txt", "transpose.txt", "hotspot.txt", "butterfly.txt", "qcnn.txt", "qae.txt"]
    file_name = ""
    while file_name not in patterns:
        print("Choices:")
        for pattern in patterns:
            print("- "+ pattern)
        file_name = input("Test circuit file name: ")

    return(number_of_cores, qubits_per_core, number_of_qubits, number_of_gates, usable_qubits, probabilities, file_name, mesh_x, mesh_y) # returns tuple

def main():
    circuit_parameters = getUserInput()
    
    # circuit_parameters = (16, 6, 100, 1000, 100, [0.25, 0.75], "circuit.txt");

    circuit_path = f"circuits/{circuit_parameters[6]}"
    simulation_path = f"simulations/{circuit_parameters[6]}"

    file = open(circuit_path, "w")
    current_network = createNetwork(circuit_parameters[0], circuit_parameters[1], circuit_parameters[4])
    node_list = current_network.available_nodes()

    cmd = ["./qcomm", "-a", "architecture.txt", "-p", "parameters.txt", "-c", circuit_path]
    
    match circuit_parameters[6]:
        case "uniform.txt":
            uniformGen(circuit_parameters[0], circuit_parameters[1], circuit_parameters[2], circuit_parameters[3], circuit_parameters[4], circuit_parameters[5], circuit_path)
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "complement.txt":
            complementGen(current_network, circuit_parameters[3], file)
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "reversal.txt":
            reversalGen(circuit_parameters[0], circuit_parameters[1], circuit_parameters[2], circuit_parameters[3], circuit_parameters[4], circuit_parameters[5], circuit_path)
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "shuffle.txt":
            shuffleGen(current_network, circuit_path, circuit_parameters[5][0], circuit_parameters[5][1], circuit_parameters[3])
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "neighbour.txt":
            neighbourGen(circuit_parameters[0], circuit_parameters[1], circuit_parameters[2], circuit_parameters[3], circuit_parameters[4], circuit_parameters[5], circuit_path, circuit_parameters[7], circuit_parameters[8])
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "transpose.txt":
            transposeGen(current_network, circuit_path, circuit_parameters[5][0], circuit_parameters[5][1], circuit_parameters[3])
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "hotspot.txt":
            hotspotGen(generate_hotspot_gates(current_network, circuit_parameters[3], circuit_parameters[5][0], circuit_parameters[5][1]), file)
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "butterfly.txt":
            butterflyGen(current_network, circuit_parameters[3], circuit_parameters[6])
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "qcnn.txt":
            qcnnGen(current_network, file)
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)

        case "qae.txt":
            with open(simulation_path, "w") as outfile:
                subprocess.run(cmd, stdout = outfile, stderr = subprocess.STDOUT)
    

    return


main()