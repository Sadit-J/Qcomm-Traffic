from bitlist import bitlist
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

        print("HERE: ", len(self.nodes_list))
        for node in self.nodes_list:
            if node.current_occupation():
                free_nodes.append(node)

        return free_nodes

    def free_all_nodes(self):
        for node in self.nodes_list:
            node.reset_occupation()

    #Returns a specific node in the network regardless of occupation
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

        #Assigns the qubit "0" to define the idle qubits
        for i in range(num_qubits):
            self.qubit_list.append("0")

    def add_qubits(self, add_num):
        for i in range(add_num):
            self.qubit_list.append("0")

        self.num_qubits += add_num

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

    def occupy_random(self):
        available_qubit = -1
        unoccupied_qubit = False

        # When multiple idle qubits exists, returns the qubit with the lowest number of
        # utilisation and set its the element to "1" to indicate it's being utilised
        while not unoccupied_qubit:
            available_qubit = random.randrange(len(self.qubit_list))

            if self.qubit_list[available_qubit] == "0":
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
            # SOME FUNNY BUSINESS IS GOING ON, WHY IS THERE ONLY 1 FREE NODE
            return False

        return True

    # Discards a qubit from use, will not be detected by other functions
    def discard_qubits(self, discarded_qubits, num_nodes):

        self.qubit_list[(discarded_qubits - int(self.address) ) // num_nodes] = "Z"