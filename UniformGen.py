import numpy as np
from numpy import random

def intToList(i):
    my_list = []
    for number in range(1, i + 1):
        my_list.append(number)
    return my_list

def generator(a, b, c, d, q, r, s):
    cores = a
    qpc = b
    qubits = c
    gates = d
    usable = q
    probs = r
    file = s

    gate_list = intToList(len(probs)) # convert number of gates to list of n-qubit gates

    random_size_gate_list = np.random.choice(gate_list, p = probs, size = (gates)).tolist() # list of 1, 2 ... n-qubit gates; probability of each; size of final list which is total amount of gates

    with open(file, "w") as test_circuit:
        current_slice = [] # tracks qubits used in current time slice

        gate_index = 0

        for gate in random_size_gate_list:

            string = "("

            track_gate = [] # tracks qubits within a gate
            
            # generates random qubit within specified size of gate
            for i in range(1, gate + 1):
                def rng(n, qrand, q):
                    # makes sure all numbers within a single gate are random                        
                    while True:
                        number = random.randint(n)
                        if number not in qrand:
                            qrand.append(number)
                            q.append(number)
                            return number
                
                # generate qubit and add to gate
                generated_qubit = rng(usable, track_gate, current_slice)
                string += f"{generated_qubit} "

            string = string[:-1] + ") "

            # check if any numbers have been repeated
            repeating = [element for element in set(current_slice) if current_slice.count(element) > 1]    

            # new line if qubit is repeating or the random number generated is greater than 0.5
            if repeating or (random.random() > 0.5 and gate_index != 0):
                index = string.rfind("(")
                string = string[:index] + "\n(" + string[index + 1:]

                # reset qubit tracker and current slice
                current_slice = []

            gate_index += 1
            test_circuit.write(string)

if __name__ == "__main__":
    generator()