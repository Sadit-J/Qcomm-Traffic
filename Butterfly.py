import random
import math
from zoneinfo import available_timezones

from bitlist import bitlist

dec_to_bin = lambda d : str(bitlist(d, 4))[9:13]
bin_to_dec = lambda d : int(str(d)[9:13], 2)

def find_butterfly(network, num):
    mesh_size = int(math.sqrt(network.get_num_nodes()))
    dest = 0
    binary_dest = ""
    binary_src = str(bitlist(num, mesh_size))[9:13]
    #print("SRC: ", num % 16)
    #print("Binary SRC: ", binary_src)

    # If the first and last digit are the same, the same number is returned
    if binary_src[0] == binary_src[-1]:
        #print("DEST unbutterfliable:", num % 16, "\n")
        return num % 16

    #finds the butterflied binary
    for i in range(0, mesh_size):
        if i == 0 or i == (mesh_size - 1):
            binary_dest += str(int(binary_src[i]) + (1 + (-2 * int(binary_src[i]))))
        else:
            binary_dest += binary_src[i]
    #print("Binary Dest: ", binary_dest)

    # converts the binary back to decimal
    for d in range(0, len(binary_dest)):
        dest += int(binary_dest[d]) * (2**(len(binary_dest) - d - 1))

    # Returns the decimal
    #print("DEST", dest, "\n")
    return dest



def butterflyGen(network, no_gates, file):
    file.write("(0) ")
    two_gate_chance = 0.5
    restart_chance = 0.1
    dec_av_nodes = []
    src = 0

    for i in range(0, no_gates):
        print("\nNEW GATE: " + str(src) + " %16: " + str(src%16) + " Gate No: " + str(i))

        for i in range(0, len(network.available_nodes())):
            dec_av_nodes.append(bin_to_dec(network.available_nodes()[i].get_address()))
            #print(network.available_nodes()[i].get_available_qubits())
        print("Available Nodes: " + str(dec_av_nodes))

        while src%16 not in dec_av_nodes:
            print("NODE " + str(src%16) + " IS NOT AVAILABLE")
            print("Available Nodes: " + str(dec_av_nodes))
            src = random.randint(0, 99)
        dec_av_nodes = []

        if random.random() < two_gate_chance:
            print("Two qubit gate")
            dest = find_butterfly(network, src)
            print("Original SRC: " + str(src) + " %16: " + str(src%16))
            print("Original DST: "  + str(dest) + " %16: " + str(dest%16))
            src = (src % 16) + (16 * network.get_node(src%16).occupy_qubits())
            dest = (dest % 16) + (16 * network.get_node(dest%16).occupy_qubits())
            print("NEW SRC: " + str(src))
            print("NEW DST: " + str(dest))
            file.write(f"({src} {dest}) ")
        else:
            print("one qubit gate")
            network.get_node(src%16).occupy_qubits()
            file.write(f"({src}) ")
        print(network.get_node(src % 16).qubit_list)

        if len(network.available_nodes()) == 0 or random.random() < restart_chance:
            print("reset happened!!!!!!!!!!!!!!!!")
            file.write("\n")
            network.free_all_nodes()

        src = random.randint(0, 99)



