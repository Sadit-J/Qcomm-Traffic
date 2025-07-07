def attainParamaters():
    with open ("architecture","r") as file:
        numbers = [int(word) for line in file for word in line.split() if word.isdigit()]
    return numbers[1],numbers[3]

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

def encoder(network,initial_size, compressed_size):
        outputSplice = []
        result = []
        network_size = len(network.getNodes())*len(network.getNodes())
        for i in range(network_size * initial_size):
            outputSplice.append(f"({i})")
        result.append(outputSplice)
        outputSplice = []
        reps = 7
        for i in range(reps):
            x = 3
            if (i == reps - 1):
                x = 2
            
            for layer in range(x):
                
                if layer == 0:
                    if  i == 0:
                        for j in range(network_size):
                            outputSplice.append(f"({j} {j+network_size})")
                    elif i == (reps - 1 ):
                        for j in range(network_size):
                            outputSplice.append(f"({j+network_size*2}) ({j+network_size*3} {j+network_size*4})")
                    else:
                        for j in range(network_size):
                            outputSplice.append(f"({j+network_size*0} {j+network_size*1}) ({j+network_size*2}) ({j+network_size*3} {j+network_size*4})")

                if layer  == 1:
                    if i == 0:
                        for j in range(network_size):
                                outputSplice.append(f"({j}) ({j+network_size*1} {j+network_size*2})")
                    elif i == (reps - 1 ):
                        for j in range(network_size):
                                    outputSplice.append(f"({j+network_size*3}) ({j+network_size*4})")
                    else:
                        for j in range(network_size):
                                outputSplice.append(f"({j}) ({j+network_size*1} {j+network_size*2}) ({j+network_size*3}) ({j+network_size*4})")


                if layer == 2:
                    for j in range(network_size):
                        outputSplice.append(f"({j+network_size*1}) ({j+network_size*2} {j+network_size*3})")
           
                result.append(outputSplice)
                outputSplice = []
    
        return result

def swap_test(network,initial_size, compressed_size):
    outputSplice = []
    result = []
    auxilQubitNumber = initial_size + (initial_size - compressed_size)
    total_size = initial_size + (initial_size - compressed_size) + 1
    network_size = len(network.getNodes())*len(network.getNodes())
    for i in range(network_size):
        outputSplice.append(f"({auxilQubitNumber*network_size+i})")
    result.append(outputSplice)
    outputSplice = []
    for i in range(initial_size - compressed_size):
        for node in range (network_size):
            outputSplice.append(f"({auxilQubitNumber*network_size+node} {auxilQubitNumber*network_size+node-(network_size)*(i+1)} {compressed_size*network_size+node+(network_size)*(i)})")
        result.append(outputSplice)
        outputSplice = []   

    for i in range(network_size):
        outputSplice.append(f"({auxilQubitNumber*network_size+i})")
    result.append(outputSplice)
    outputSplice = []

    return result

#Lets say I have 160 qubits total
#lets say on each node 7 qubits of data is being used
#and I want to compress that down to 5 qubits of data
#My reference space will be 7-5 = 2 and the last bit will be an auxil qubit for performing swap tests

class Node:
    def __init__(self, nodeNumber,qbAmount,coordinates,):
        self.nodeNumber = nodeNumber
        self.qbAmount = qbAmount
        self.coordinates = coordinates
        
    def getNodeNumber(self):
        return self.nodeNumber
    
    def getQbAmount(self):
        return self.qbAmount

    def getCoords(self):
        return self.coordinates
    
    def __str__(self):
        return f"ID: {self.nodeNumber} , Coords: {self.coordinates}"


class Network:
    def __init__(self,nodes,size):
        self.nodes = [[None for _ in range(size)] for _ in range(size)]
        self.size = size

    def addNode(self,node,x,y):
        self.nodes[x][y] = node

    def getNodes(self):
        return self.nodes


def qaeGen(size, qubits_per_core,numOfQubits,file_name):
    initial_size = qubits_per_core - 3
    compressed_size = initial_size - 2 
    reference_space = initial_size - compressed_size


    #Create Network
    network = Network([],size)
    for i in range(size):
        for j in range(size):
            network.addNode(Node(i*size+j,size,(i,j)),i,j)
    qubits = [0] * numOfQubits * size*size 

    workload_list = []
    for i in range(initial_size*size*size):
        workload_list.append(i)

    with open(file_name, "w") as f:
        angleEncoderZZ(initial_size*size*size,network,f,1,workload_list)

        encoder_layer = encoder(network,initial_size,compressed_size)
        for layer in encoder_layer:
            f.write(" ".join(layer) + "\n")

    # swap_test = swap_test(network,initial_size,compressed_size)
    # with open(f"{name}.txt", "a") as f:
    #     for layer in swap_test:
    #         f.write(" ".join(layer) + "\n")

    with open(file_name, "a") as f:
        for layer in reversed(encoder_layer):
            f.write(" ".join(layer) + "\n")