#The number of which you are finding the factorial can be changed at 0x10010004 in the memory.txt file
#The factorial is stored in '10001' in regmem.txt
mem={}
regmem={}
def getmem():#reads inst and data mem from memory.txt
    d={}
    f=open("memory.txt","r")
    contents=f.read()
    tp=contents.split("\n")
    tp=tp[:-1]
    for i in tp:
        temp = i.split(":")
        d[int(temp[0],16)] = temp[1]
    return d
mem = getmem()
def getregmem():#reads regmem from regmem.txt
    d={}
    f=open("regmem.txt","r")
    contents=f.read()
    tp=contents.split("\n")
    tp=tp[:-1]
    for i in tp:
        temp = i.split(":")
        d[temp[0]] = temp[1]
    return d
regmem = getregmem()
# print mem
def memwrite():#writes to memory.txt after each operation
    l=[]
    
    for i in mem:
        if len(hex(i))==10:
            t=str(hex(i))+":"+str(mem[i]) + '\n';
            l.append(t)
        else:
            t=hex(i)[0:2]+"00"+hex(i)[2:8]+":"+str(mem[i])+'\n'
            l.append(t)
    l.sort()
    x=open("memory.txt","w")
    x.writelines(l)

def regmemwrite():#updates regemem.txt after each operation
    l=[]
    for i in regmem:
        
        t=i+":"+regmem[i] + '\n';
        l.append(t)
    l.sort()
    x=open("regmem.txt","w")
    x.writelines(l)

    
clock=0

pc=0x00400000 #starting pc
def signextend(x): #to make immediate values 32 bit
    if(x[0] == '1'):
        return (int(x, 2) - 2**len(x))
    z="0000000000000000"+str(x)
    return int(z,2)

def fetch_stage(pc):
    
    global clock
    clock+=1 #1 clock cycle is one fetch
    return mem[pc]

def decode_stage(inst):
    opcode=inst[0:6] # decodes each instruction according to its type 
    
    if opcode=="000000":
         
         rs=inst[6:11]
         rt=inst[11:16]
         rd=inst[16:21]
         shamt=inst[21:26]
         fn=inst[26:32]
         
         return [0,opcode,rs,rt,rd,shamt,fn]
       
    elif opcode=="000010":
        return [1,opcode,inst[6:32]]

    else:
        rs=inst[6:11]
        rt=inst[11:16]
        imm=inst[16:32]
        
        return [2,opcode,rs,rt,imm]

def execution_stage(decoded_list):
    global pc
    pc+=4
    if decoded_list[0]==0:#r-type
        if decoded_list[6]=="100000":#add
            return (2,decoded_list[4],int(regmem[decoded_list[2]],16)+int(regmem[decoded_list[3]],16))
        elif decoded_list[6]=="100010":#sub
            return (2,decoded_list[4],int(regmem[decoded_list[2]],16)-int(regmem[decoded_list[3]],16))
       
    elif decoded_list[0]==2:#i type
        if decoded_list[1]=="001000":#addi
            return (2,decoded_list[3],int(regmem[decoded_list[2]],16)+signextend(decoded_list[4]))
        elif decoded_list[1]=="000100":#beq
            if int(regmem[decoded_list[2]],16)==int(regmem[decoded_list[3]],16):
                
                pc+=signextend(decoded_list[4])*4
            return 3
            
           
        elif decoded_list[1]=="000101":#bne
            if int(regmem[decoded_list[2]], 16)!=int(regmem[decoded_list[3]], 16):
                pc+=signextend(decoded_list[4])*4 #calculation of branch target
            return 3
                
        elif decoded_list[1]=="100011":#load
            return (0,signextend(decoded_list[4])+int(regmem[decoded_list[2]],16),decoded_list[3])
        elif decoded_list[1]=="101011":#store
            
            return (1,signextend(decoded_list[4])+int(regmem[decoded_list[2]],16),decoded_list[3])
    else :#jump
        pc="{:032b}".format(pc)
        
        pc = int((pc[0:3] + decoded_list[2] + "00"),2)#calculation of jump address
        pc="{:032b}".format(pc)
        pc=int(pc,2)
        return 3

def mem_stage(mem_addr_tuple):
    
    if mem_addr_tuple==3:
        return mem_addr_tuple
    elif(mem_addr_tuple[0] == 0):
        return (0,mem_addr_tuple[2],int(mem[mem_addr_tuple[1]],2))
    elif(mem_addr_tuple[0] == 1):
        mem[mem_addr_tuple[1]]=str(regmem[mem_addr_tuple[2]])
        memwrite() #writes to main memory
    return mem_addr_tuple;

def write_back(mem_addr_tuple):
    
    if mem_addr_tuple==3:
        return 
    if type(mem_addr_tuple[2])==str:
        regmem[mem_addr_tuple[1]]=mem_addr_tuple[2]
    else:
        regmem[mem_addr_tuple[1]]=hex(mem_addr_tuple[2])
    regmemwrite()# writes to register memory



def mips():
    inst=fetch_stage(pc)
    l=decode_stage(inst)
    l1=execution_stage(l)  
    l2=mem_stage(l1)
    write_back(l2)
 
while mem[pc]!='':
    
    mips()

print (str(int(mem[0x10010004],2))+" factorial is " +str(int(regmem['10001'],16)))
print ("Total Number of cycles required to find "+str(int(mem[0x10010004],2))+" factorial is " + str(clock))
print ("\nCopyrighted by Kashif,Aravind and Anvit")







