import random
import math

def bit_complement(network, src, src_qubit, traffic, available_list):
    two_gate_chance = 0.25
    if (random.random() < two_gate_chance):
        dst_address = ~src.get_address()
        if network.get_node(dst_address) is not None and network.get_node(dst_address).current_occupation():
            print("SRC:", src.get_address(), "DST:", dst_address)
            dst_qubit = network.get_node(dst_address).occupy_random()
            traffic.append((int(src.get_address()) + network.get_num_nodes() * src_qubit, int(dst_address) + network.get_num_nodes() * dst_qubit))
        else:
            print("No Destination")

        available_list = network.available_nodes()

        return traffic

    traffic.append((int(src.get_address()) + network.get_num_nodes() * src_qubit,))
    available_list = network.available_nodes()
    return traffic

def generate_traffic(num_nodes, network, slice_complexity, selection, seed=None):

    splice_end_prob = 0.2
    if seed is not None:
        random.seed(seed)

    if slice_complexity == 0:
        slice_complexity = num_nodes

    traffic = []
    possible_nodes = network.available_nodes()
    src = possible_nodes[0]
    chosen_qubit = src.occupy_qubits()

    for i in range(slice_complexity):

            possible_nodes = network.available_nodes()

            bit_complement(network, src, chosen_qubit, traffic, possible_nodes)

            if len(network.available_nodes()) == 0:
                print("No more available nodes")
                break

            if random.random() < splice_end_prob:
                break

            src = random.choice(possible_nodes)
            chosen_qubit = src.occupy_random()

    return traffic

def complementGen(current_network, user_gates, file):
    total_gates = 1
    traffic_pattern = []
    possible_nodes = current_network.available_nodes()
    src = possible_nodes[0]
    src_qubit = src.occupy_qubits()
    bit_complement(current_network, src, src_qubit, traffic_pattern, possible_nodes)
    current_network.free_all_nodes()


    while total_gates < user_gates:

        traffic_pattern += generate_traffic(current_network.get_num_nodes(), current_network, 100, "complement")
        current_network.free_all_nodes()
        total_gates = len(traffic_pattern)

    for src in traffic_pattern:

        if len(src) == 1:
            file.write(f"({src[0]}) ")
        else:
            file.write(f"({src[0]} {src[1]}) ")
        total_gates += 1

        if (total_gates >=  user_gates):
            break

    file.write("\n")
        
    
#Uniform Traffic Pattern

'''
def uniform_traffic(network, src, src_qubit, destination_list, traffic):
    two_gate_chance = 0.25
    dst = src
    if (random.random() < two_gate_chance):
        while dst == src and len(destination_list) > 0:
            chosen_node = random.choice(destination_list)
            if chosen_node.current_occupation() and chosen_node != src:
                dst = chosen_node
                dst_qubit = chosen_node.occupy_random()
                print(int(dst.get_address()))
                traffic.append((int(src.get_address()) + network.get_num_nodes() * src_qubit, int(dst.get_address()) + network.get_num_nodes() * dst_qubit))
                return

            elif len(destination_list) == 1:
                 dst = chosen_node
                 break

    traffic.append((int(src.get_address()) + network.get_num_nodes() * src_qubit,))
    destination_list = network.available_nodes()
    return dst
    '''
