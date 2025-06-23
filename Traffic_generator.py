from bitlist import bitlist
import random
import math

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
        for i in range(num_qubits):
            self.qubit_list.append("0")

    def get_available_qubits(self):
        available_qubits = []
        for qubit_availability in self.qubit_list:
            if qubit_availability == "0":
                available_qubits.append(qubit_availability)

        return available_qubits

    def occupy_qubits(self):

        available_qubit = -1
        unoccupied_qubit = False

        if "0" in self.qubit_list:
            available_qubit = self.qubit_list.index("0")
            self.qubit_list[available_qubit] = "1"
            unoccupied_qubit = True
        
        return available_qubit


    def get_address(self):
        return self.address

    def reset_occupation(self):
        i = 0
        while i < self.num_qubits:
            if "1" in self.qubit_list:
                occupied_qubit = self.qubit_list.index("1")
                self.qubit_list[occupied_qubit] = "0"
            else:
                break

            i += 1

    def current_occupation(self):
        if "0" not in self.qubit_list:
            return False

        return True

    def discard_qubits(self, discarded_qubits, num_nodes):

        self.qubit_list[(discarded_qubits - int(self.address) ) // num_nodes] = "Z"

def getUserInput():
    return

def main():
    return

main()
