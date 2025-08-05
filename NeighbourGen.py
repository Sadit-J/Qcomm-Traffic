import numpy as np
import math as m
from numpy import random

def adjacentCore(i, width, length):
    noc_array = []
    count = width # helper variable
    
    # creates 2D array of cores in sequential order in rows then columns
    for y in range(length):
        noc_array.append([])
        x = count - width
        while x < count:
            noc_array[y].append(x)
            x += 1
        count += width

    row_number = 0 # track row index

    # determines the coordinate of the core
    for row in noc_array:
        column_number = 0 # track column index
        for column in row:
            if column == i:
                source_coord = [row_number, column_number]
                break
            column_number += 1
        row_number += 1

    # determines destination (adjacent) coordinate
    while True:
        destination_coord = source_coord.copy() # so that when modifying destination coordinate it doesn't point to the source coordinate

        # randomly generates addition or subtraction operation to column or row number of source coordinate
        add_or_subtract = random.randint(0, 2)
        row_or_column = random.randint(0, 2)
        
        if add_or_subtract == 0:
            # add to row number
            if row_or_column == 0:
                destination_coord[0] += 1
            # add to column number
            if row_or_column == 1:
                destination_coord[1] += 1

        if add_or_subtract == 1:
            # subtract to row number
            if row_or_column == 0:
                destination_coord[0] -= 1
            # substract to column number
            if row_or_column == 1:
                destination_coord[1] -= 1

        # breaks the loop if the generated coordinates is within bounds of the array
        if 0 <= destination_coord[0] < len(noc_array) and 0 <= destination_coord[1] < len(noc_array[0]):
            break
    
    j = noc_array[destination_coord[0]][destination_coord[1]]

    return j

def intToList(i):
    my_list = []
    for number in range(1, i + 1):
        my_list.append(number)
    return my_list

def findCore(dictionary, desired_value):
    for key, number in dictionary.items():
        if desired_value in number:
            return key

def neighbourGen(a, b, c, d, q, r, s, t, u):
    cores = a
    qpc = b
    qubits = c
    gates = d
    usable = q
    probs = r
    file = s
    x = t
    y = u

    # number of bits to perform bit reversal on depends on the amount of cores
    bits = m.log(cores, 2)
    bits = m.ceil(bits)

    gate_list = intToList(len(probs)) # convert number of gates to list of n-qubit gates

    random_size_gate_list = np.random.choice(gate_list, p = probs, size = (gates)).tolist() # list of 1, 2 ... n-qubit gates; probability of each; size of final list which is total amount of gates

    with open(file, "w") as test_circuit:
        mapper = {} # maps qubits to cores
        qubit_list = [] # list for qubits in current core

        for core in range(cores):
            mod = core

            # adds qubits to a list in a certain multiple that satisfies the qubits per core
            while mod < usable:
                qubit_list.append(mod)
                mod += int(qubits / qpc)
            
            # map and reset for next set of qubits
            mapper[core] = qubit_list
            qubit_list = []

        current_slice = [] # tracks qubits used in current time slice

        gate_index = 0

        for gate in random_size_gate_list:
            
            if gate == 1:
                string = "G1("
            elif gate == 2:
                string = "G2("

            track_gate = [] # tracks qubits within a gate

            # bit reversal if 2-qubit gate
            if gate == 2:
                source_qubit = random.randint(usable)
                corresponding_core = findCore(mapper, source_qubit)


                adjacent_core = adjacentCore(corresponding_core, x, y)

                # makes sure qubits are not repeated within the same 2-qubit gate
                while True:
                    destination_qubit = np.random.choice(mapper[adjacent_core])
                    if destination_qubit != source_qubit:
                        break
                
                current_slice.append(source_qubit)
                current_slice.append(destination_qubit)
                string += f"{source_qubit} {destination_qubit} "
            
            else:
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
                index = string.rfind("G")
                string = string[:index - 1] + f"\n"

                # reset qubit tracker and current slice
                current_slice = []

            gate_index += 1
            test_circuit.write(string)