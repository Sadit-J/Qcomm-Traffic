from bitlist import bitlist
import random
import math
import Network


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

def qcnnGen(network, circuit_file):
    input_size = 5
    workload_list = []


    window_size = input_size * input_size
    workload_list = select_nodes(window_size, network, circuit_file)
    print(window_size)
 
    print(workload_list)

    # encoder
    # angleEncoderZ(window_size, network, circuit_file, 1, workload_list)
    angleEncoderZZ(window_size, network, circuit_file, 1, workload_list)

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
    

# angle encoder following Qiskit's ZFeatureMap circuit implementation
def angleEncoderZ(window_size, network, circuit_file, reps, workload_list):
    circuit = ""
    slices = 2 * reps

    for slice in range(slices):
        for i in workload_list:
            circuit += f"({i}) "
        circuit += "\n"

    circuit_file.write(circuit)

# angle encoder following Qiskit's ZZFeatureMap circuit implementation (linear entanglement)
def angleEncoderZZ(window_size, network, circuit_file, reps, workload_list):
    circuit = ""
    
    for rep in range(reps):

        for slice in range(2):
            for i in workload_list:
                circuit += f"({i}) "
            circuit += "\n"

        for i in range(len(workload_list) - 1):
            current_qubit = workload_list[i]
            next_qubit = workload_list[i + 1]
            circuit += f"({next_qubit} {current_qubit}) \n"
            circuit += f"({next_qubit}) \n"
            circuit += f"({next_qubit} {current_qubit}) \n"

    circuit_file.write(circuit)

