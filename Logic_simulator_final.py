inp_vector=[]
inp_nodes=[]
out_nodes=[]
cktfile = "ckt_netlist.txt"
inp_vector_str = "11100"
#conversion to integer       
inp_vector = [int(val) for val in inp_vector_str]
netlist_file = open(cktfile,"r")
last_node=0 
#Counting the lines in the file and store
no_of_lines = 0
for line in netlist_file:
    line = line.strip()
    word = line.split()
    oper = word[0]
    Nodenum_str = word[1:-1]
    if oper =='node_inp':
        inp_nodes = list(map(int, Nodenum_str))
    if oper == 'node_out':
        out_nodes = list(map(int, Nodenum_str))
    Nodenum = list(map(int, Nodenum_str))
    if(last_node < max(Nodenum)):
            last_node = max(Nodenum)
    #Count no. of lines in the ckt file.
    no_of_lines = no_of_lines + 1
netlist_file.close()
interconnect = [0]*(last_node)
# defining gates
def INV(w):
    interconnect[w[1]-1] = int(not interconnect[w[0]-1])
def NAND(w):
    interconnect[w[2]-1] = int(not (interconnect[w[0]-1] and interconnect[w[1]-1]))
def OR(w):
    interconnect[w[2]-1] = int( interconnect[w[0]-1] or interconnect[w[1]-1])
def AND(w):
    interconnect[w[2]-1] = int(interconnect[w[0]-1] and  interconnect[w[1]-1])
def NOR(w):
    interconnect[w[2]-1] = int(not ((interconnect[w[0]-1])or ( interconnect[w[1]-1])))
def node_out(w):
    output_vector = [interconnect[indx-1] for indx in w]
    return output_vector     
def node_inp(w):
    for i in range(len(w)):
        interconnect[w[i]-1] = inp_vector[i]
Netlist_Sim = open(cktfile,"r")
lines = Netlist_Sim.readlines()
Netlist_Sim.close()
# Nodes that have a valid output
Nodenum_processed = []
line_number= 0
finished = [0]*(no_of_lines)
node_inp(inp_nodes)
#Iterating for max no. of lines to tackle worst case and the logical values of all nodes are evaluated
level = 1
for itter_no in range(no_of_lines):
    for line in lines:
        word = line.split()
        oper = word[0]
        Nodenum = []
        Nodenum_str = []
        if(oper =='node_inp' or oper =='node_out'):
            Nodenum_str = word[1:-1]
            Nodenum = list(map(int, Nodenum_str))
        else:
            Nodenum_str = word[1:]
            Nodenum = list(map(int, Nodenum_str))
        Nodenum_processed = inp_nodes
    #  Logical operations to be performed
        if oper=='INV':
            if (Nodenum[0] in Nodenum_processed) and ( finished[line_number] == 0):
                INV(Nodenum)
                finished[line_number]=1
                Nodenum_processed.append(Nodenum[1])
                if (Nodenum[0] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[0])
                print("",oper, "processed and level of the gate is ", level)
        if oper=='AND':
            if(Nodenum[0] in Nodenum_processed) and (Nodenum[1] in Nodenum_processed) and (finished[line_number]==0):
                AND(Nodenum)
                finished[line_number]=1
                Nodenum_processed.append(Nodenum[2])
                if (Nodenum[0] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[0])
                if (Nodenum[1] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[1])
                print("",oper, "processed and level of the gate is ", level)
        if oper=='NOR':
            if(Nodenum[0] in Nodenum_processed) and (Nodenum[1] in Nodenum_processed) and (finished[line_number]==0):
                NOR(Nodenum)
                finished[line_number]=1
                Nodenum_processed.append(Nodenum[2])
                if (Nodenum[0] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[0])
                if (Nodenum[1] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[1])
                print("",oper, "processed and level of the gate is ", level)
        if oper=='NAND':
            if(Nodenum[0] in Nodenum_processed) and (Nodenum[1] in Nodenum_processed) and (finished[line_number]==0):
                finished[line_number]=1
                NAND(Nodenum)
                Nodenum_processed.append(Nodenum[2])
                if (Nodenum[0] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[0])
                if (Nodenum[1] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[1])
                print("",oper, "processed and level of the gate is ", level)
        if oper=='OR':
            if(Nodenum[0] in Nodenum_processed) and (Nodenum[1] in Nodenum_processed) and (finished[line_number]==0):
                finished[line_number]=1
                OR(Nodenum)
                Nodenum_processed.append(Nodenum[2])
                if (Nodenum[0] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[0])
                if (Nodenum[1] not in Nodenum_processed):
                    Nodenum_processed.append(Nodenum[1])
                print("",oper, "processed and level of the gate is ", level)
        if oper=='node_inp':
            finished[line_number]=1
        if oper=='node_out':
            finished[line_number]=1
        line_number+=1
        if line_number== (no_of_lines):
            line_number=0 
    level+=1
    #stop if all lines are processes from ckt file
    if finished.count(1)==(no_of_lines):
       print("\nLogic Simulation has finished\n\n") 
       break
output = node_out(out_nodes)
print(" node_numbers of Output nodes", out_nodes,"and there corresponding outputs are", output)