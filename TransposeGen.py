import math
import random
import bitlist
from bitlist import bitlist
from Network import Network, Node

def create_splice(current_network, oneInputGates,twoInputGates, oneInputChance):
    
    spliceCoeff = random.randint(1,5)
    test = 0
    outputSplice = []
    node_list = current_network.available_nodes()

    
    while (test != spliceCoeff and len(node_list) != 0):
        src_node = random.choice(node_list)
        src_qubit = src_node.occupy_random()
        chance = random.random()

        if (chance < oneInputChance and oneInputGates != 0):
            outputSplice.append(f"({src_qubit})")
            oneInputGates -= 1

        elif (twoInputGates != 0):

            src_address = src_node.get_address()

            # print(f"Source : {src_address}")
            #dst_address = src_address[-1:] + src_address[:-1]  

            dst_address = src_address[2:] + src_address[:2] 
            # print(src_address[2:])
            # print(src_address[:2]) 

            # print(f"Target : {dst_address} ")
            dst_node = current_network.get_node(dst_address) 
            if (dst_node.current_occupation()):
                    dst_qubit = dst_node.occupy_random()
                    # print(f"({src_qubit*current_network.get_num_nodes() + int(src_address)} {dst_qubit*current_network.get_num_nodes() + int(dst_address)})")

                    outputSplice.append(f"({src_qubit*current_network.get_num_nodes() + int(src_address)} {dst_qubit*current_network.get_num_nodes() + int(dst_address)})")    
                    twoInputGates -= 1
            elif (dst_node in node_list):
                node_list.remove(dst_node)



        if src_node in node_list and not src_node.current_occupation():
            node_list.remove(src_node)

        test = random.randint(1,5)
    


    return twoInputGates,oneInputGates,outputSplice

def generateCircuit(current_network, oneInputGates,twoInputGates, oneInputChance, name):
    with open(name,"w") as file:
        while(twoInputGates != 0 or oneInputGates != 0):
            twoInputGates,oneInputGates,outputSplice = create_splice(current_network, oneInputGates,twoInputGates, oneInputChance)
            current_network.free_all_nodes()          

            if outputSplice:
                file.write(" ".join(outputSplice))
                file.write(" \n")

def transposeGen(current_network, file_name, oneInputChance, twoInputChance, numOfGates):
    oneInputGates = math.floor(oneInputChance*numOfGates)
    twoInputGates = math.floor(twoInputChance*numOfGates)
    generateCircuit(current_network, oneInputGates,twoInputGates, oneInputChance, file_name)



  