from bitlist import bitlist
from Butterfly import butterfly_traffic
import random
import math


# Class defines the mesh network containing the nodes
class Network():
    def __init__(self, nodes, node_qubits, total_qubits):
        self.qubit_per_node = node_qubits
        self.total_qubits = total_qubits
        self.nodes_list = nodes

    def available_nodes(self):
        free_nodes = []

        for node in self.nodes_list:
            if node.current_occupation():
                free_nodes.append(node)

        return free_nodes

    def free_all_nodes(self):
        for node in self.nodes_list:
            node.reset_occupation()

    # Returns a specific node in the network regardless of occupation
    def get_node(self, node_address):
        for node in self.nodes_list:
            if node_address == node.get_address():
                return node

        return None

    def get_per_qubits(self):
        return self.qubit_per_node

    def get_total_qubits(self):
        return self.total_qubits

    def get_num_nodes(self):
        return len(self.nodes_list)


class Node():
    def __init__(self, address, num_qubits, length):
        self.address = bitlist(address, length)
        self.num_qubits = num_qubits
        self.qubit_list = []

        # Assigns the qubit "0" to define the idle qubits
        for i in range(num_qubits):
            self.qubit_list.append("0")

    def add_qubits(self, add_num):
        for i in range(add_num):
            self.qubit_list.append("0")

    def get_available_qubits(self):

        # Returns a list of the all the available qubits within
        # the node
        available_qubits = []
        for qubit_availability in self.qubit_list:
            if qubit_availability == "0":
                available_qubits.append(qubit_availability)

        return available_qubits

    def occupy_qubits(self):

        # If there are no available qubits returns a -1
        available_qubit = -1
        unoccupied_qubit = False

        # When multiple idle qubits exists, returns the qubit with the lowest number of
        # utilisation and set its the element to "1" to indicate it's being utilised
        if "0" in self.qubit_list:
            available_qubit = self.qubit_list.index("0")
            self.qubit_list[available_qubit] = "1"
            unoccupied_qubit = True

        return available_qubit

    def get_address(self):
        return self.address

    # Resets all qubits to become idle
    def reset_occupation(self):
        i = 0
        while i < self.num_qubits:
            if "1" in self.qubit_list:
                occupied_qubit = self.qubit_list.index("1")
                self.qubit_list[occupied_qubit] = "0"
            else:
                break

            i += 1

    # Returns true if there are qubits available, otherwise false
    def current_occupation(self):
        if "0" not in self.qubit_list:
            return False

        return True

    # Discards a qubit from use, will not be detected by other functions
    def discard_qubits(self, discarded_qubits, num_nodes):

        self.qubit_list[(discarded_qubits - int(self.address)) // num_nodes] = "Z"


def createNetwork(nodes_num, qubits_per, total_qubits):
    node_list = []
    iteration = 0

    for i in range(nodes_num):
        node_list.append(Node(i, 0, 4))

    while (total_qubits > 0):
        node_list[iteration % 16].add_qubits(1)
        iteration += 1
        total_qubits -= 1

    current_network = Network(node_list, qubits_per, total_qubits)
    return current_network


def getUserInput():
    # read and extract parameters from architecture.txt
    arch = open("samples/architecture.txt", "r")
    read_arch = arch.readlines()
    mesh_x = int(read_arch[0].strip("mesh_x "))
    mesh_y = int(read_arch[1].strip("mesh_y "))

    number_of_cores = mesh_x * mesh_y
    qubits_per_core = int(read_arch[3].strip("qubits_per_core "))
    number_of_qubits = qubits_per_core * number_of_cores
    number_of_gates = int(input("Number of gates: "))

    usable_qubits = number_of_qubits  # initializes variable for while loop

    while usable_qubits >= number_of_qubits:
        usable_qubits = int(input(f"Number of logical qubits (must be <{number_of_qubits} qubits): "))

    probabilities = []  # initialize list for storing probabilities
    total_prob = 0  # initialize total probability tracker
    n = 1  # initialize count for n-qubits

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

        probabilities.append(n_qubit_gate_prob)  # add probability to list

    # ask user for the name of the file the generated circuit will be outputted on
    file_name = ""
    while ".txt" not in file_name:
        file_name = input("Test circuit file name (include .txt): ")

    return (number_of_cores, qubits_per_core, number_of_qubits, number_of_gates, usable_qubits, probabilities,
            file_name)  # returns tuple


def main():
    # circuit_parameters = getUserInput()

    circuit_parameters = (16, 6, 160, 1000, 100, [1], "circuit.txt")

    current_network = createNetwork(circuit_parameters[0], circuit_parameters[1], circuit_parameters[4])
    node_list = current_network.available_nodes()
    for i in node_list:
        print("Core:", int(i.get_address()))
        print("Qubits:", len(i.get_available_qubits()))

    return


main()