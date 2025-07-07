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