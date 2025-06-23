from bitlist import bitlist
import random
import math
import itertools

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

        """
        while not unoccupied_qubit:
            available_qubit = random.randrange(len(self.qubit_list))

            if self.qubit_list[available_qubit] == "0":
                self.qubit_list[available_qubit] = "1"
                unoccupied_qubit = True
        """

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


def write_circuit(circuit, f):

    for src in circuit:

        if len(src) == 1:
            f.write(f"({src[0]}) ")
            print(f"Node {int(src[0])}")
        else:

            print(f"Node {int(src[0])} → Node {int(src[1])}")
            # print(f"{i}. Qubit {int(src[0].get_address()) * num_qubits + src[0].occupy_qubits()} → Qubit {int(src[1].get_address()) * num_qubits + src[0].occupy_qubits()}")
            f.write(f"({src[0]} {src[1]}) ")

    return

def conv_param_circuit(qubit_one, qubit_two, circuit_file):
    return [(qubit_two,), (qubit_two, qubit_one), (qubit_one, qubit_two), (qubit_two,), (qubit_two, qubit_one), (qubit_one,)]

def convolution_operations(occupied_qubits, node_address, circuit_file):

    num_qubits = len(occupied_qubits)
    if (num_qubits > 2):
        qubit_combinations = [(occupied_qubits[i], occupied_qubits[(i+1) % num_qubits]) for i in range(num_qubits)]
    else:
        qubit_combinations = [(occupied_qubits[0], occupied_qubits[1])]

    print(qubit_combinations)

    for i in qubit_combinations:
        conv_circuit = conv_param_circuit(i[0], i[1], circuit_file)
        write_circuit(conv_circuit, circuit_file)

    circuit_file.write("\n")

    return

def pool_param_circuit(qubit_one, qubit_two, circuit_file ):
    return [(qubit_two,), (qubit_two, qubit_one), (qubit_one,), (qubit_two,), (qubit_one, qubit_two), (qubit_two,)]

def pooling_operation(occupied_qubits, network, circuit_file):

    random.shuffle(occupied_qubits)

    pairs = []
    for i in range(0, len(occupied_qubits) - 1, 2):
        pairs.append((occupied_qubits[i], occupied_qubits[i + 1]))

    #circuit_file.write("Pool Layer: ")
    for pair in pairs:
        pool_circuit = pool_param_circuit(pair[0], pair[1], circuit_file)
        current_node = pair[0] %  16
        network.get_node(current_node).discard_qubits(pair[0], network.get_num_nodes())
        occupied_qubits.remove(pair[0])

        write_circuit(pool_circuit, circuit_file)

    circuit_file.write("\n")
    return

def select_nodes(window_size, network, file):
    available_nodes = network.available_nodes()
    leftover_neurons = window_size * window_size
    workload = []

    if leftover_neurons <= network.get_total_qubits():
        current_node = available_nodes[0]
        available_nodes.remove(current_node)

        for i in range(leftover_neurons):
            if not current_node.current_occupation():
                current_node = random.choice(available_nodes)
                available_nodes.remove(current_node)


            workload.append(int(current_node.get_address()) + network.get_num_nodes() * current_node.occupy_qubits())
            print("Address:", int(current_node.get_address()), "Qubit", ((workload[len(workload) - 1] - int(current_node.get_address()) ) // 16), "Qubit Number", workload[-1:])

    else:
        print("Not enough cores for largest slice")


    return workload

def cnn_traffic(num_qubits, network, circuit_file):
    maximum_grouping = num_qubits
    kernel_size = 2
    input_size = 5

    workload_list = []
    layer_len = []
    layer_pos = 0

    stride_conv = 1
    stride_pool = 2
    padding = 0

    i = 0

    window_size = math.floor(((input_size - kernel_size + 2 * padding) / stride_conv) + 1)
    workload_list = select_nodes(window_size, network, circuit_file)
    print(window_size)
    #(workload_list)
    while len(workload_list) > 2:

        if (i % 2) == 0:
            #conv layer
            print("Conv layer")
            convolution_operations(workload_list, network, circuit_file)
        else:
            #pool layer
            print("Pool layer")
            pooling_operation(workload_list, network, circuit_file)

        print(workload_list)
        i += 1



def main():
    f = open("QCNN_traffic.txt", "w")
    num_qubits = 6
    node_list = []
    num_nodes = 16

    node_list.append(Node(0, num_qubits + 1, int(math.sqrt(num_nodes))))
    node_list.append(Node(1, num_qubits + 1, int(math.sqrt(num_nodes))))
    node_list.append(Node(2, num_qubits + 1, int(math.sqrt(num_nodes))))
    node_list.append(Node(3, num_qubits + 1, int(math.sqrt(num_nodes))))

    for i in range(4, num_nodes):
        node_list.append(Node(i, num_qubits, int(math.sqrt(num_nodes))))

    current_Network = Network(node_list, num_qubits, 100)


    cnn_traffic(num_qubits, current_Network, f)

main()