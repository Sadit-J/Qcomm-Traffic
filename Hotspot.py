import random

def get_global_qubits_per_node(network):
    num_nodes = network.get_num_nodes()
    node_qubits = {i: [] for i in range(num_nodes)}
    global_id = 0

    max_qubits = max(len(node.qubit_list) for node in network.nodes_list)

    for i in range(max_qubits * num_nodes):
        node_id = i % num_nodes
        node = network.get_node(node_id)
        local_index = len(node_qubits[node_id])

        if local_index < len(node.qubit_list) and node.qubit_list[local_index] != "Z":
            node_qubits[node_id].append(global_id)

        global_id += 1

    return node_qubits  # {node_id: [global_qubit_indices]}

def generate_hotspot_gates(network, ngates, p_one_qubit, p_two_qubit):
    gates = []
    
    #hotspot: core 5 and neighbors
    node_qubits = get_global_qubits_per_node(network)
    core5_qubits = node_qubits[5]
    neighbor_ids = [1, 4, 6, 9]
    neighbor_qubits = {nid: node_qubits[nid] for nid in neighbor_ids}


    nqubits = sum(len(node.qubit_list) for node in network.nodes_list)
    if nqubits == 0:
        # print("Error: No qubits available in network.")
        return []

    num_one_qubit = int(p_one_qubit * ngates)
    num_two_qubit = ngates - num_one_qubit

    while num_one_qubit > 0 or num_two_qubit > 0:
        insert_two_qubit = (num_two_qubit > 0) and (
            random.random() < p_two_qubit or num_one_qubit == 0
        )

        if insert_two_qubit:
            gate_type = random.randint(0, 2)

            if gate_type == 0 and len(core5_qubits) >= 2:
                q1, q2 = random.sample(core5_qubits, 2)
                gates.append((q1, q2))
                num_two_qubit -= 1

            elif gate_type == 1 and core5_qubits:
                src = random.choice(core5_qubits)
                dst_core = random.choice(neighbor_ids)
                dst_list = neighbor_qubits[dst_core]
                if dst_list:
                    dst = random.choice(dst_list)
                    gates.append((src, dst))
                    num_two_qubit -= 1

            else:
                if nqubits > 1:
                    src = random.randint(0, nqubits - 1)
                    dst = random.randint(0, nqubits - 1)
                    while src == dst:
                        dst = random.randint(0, nqubits - 1)
                    gates.append((src, dst))
                    num_two_qubit -= 1

        else:
            q = random.randint(0, nqubits - 1)
            gates.append((q, -1))
            num_one_qubit -= 1

    return gates

def hotspotGen(network, ngates, p_one_qubit, p_two_qubit, file):
    gates = generate_hotspot_gates(network, ngates, p_one_qubit, p_two_qubit)
    busy = set()
    stage = []

    def flush_stage(stage):
        if stage:
            line = []
            for g in stage:
                if g[1] == -1:
                    line.append(f"({g[0]})")
                else:
                    line.append(f"({g[0]} {g[1]})")
            file.write(" ".join(line) + "\n")

    for g in gates:
        src, dst = g
        if src not in busy and dst not in busy:
            stage.append(g)
            busy.add(src)
            if dst != -1:
                busy.add(dst)
        else:
            flush_stage(stage)
            stage = [g]
            busy = {src}
            if dst != -1:
                busy.add(dst)

    flush_stage(stage)  # print remaining stage
    
    file.close()
