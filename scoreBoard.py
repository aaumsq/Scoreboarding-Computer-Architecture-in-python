#### implementation of ScoreBoard in python...

import functions as f  #### importing the verilog modules
class fStatus:         ### class for the functional unit
    def __init__(self, busy = False, op = None, fi = None, fj = None, fk = None, qj = None, qk = None, rj = None, rk = None):
        self.busy = busy
        self.op = op
        self.fi = fi
        self.fj = fj
        self.fk = fk
        self.qj = qj
        self.qk = qk
        self.rj = rj
        self.rk = rk


   
class iSt:          ### class for the instruction status
    def __init__(self, issue = 0, rdOp = 0, exe = 0, wb = 0):
        self.issue = issue
        self.rdOp = rdOp
        self.exe = exe
        self.wb = wb

    def __str__(self):
        return str(str(self.issue)+"          "+str(self.rdOp)+"           "+str(self.exe)+"            "+str(self.wb ))

'''"ADD r0 r1 r2",
       "ADD r3 r4 r5",
        "LDR r2 r9",
       "ADD r6 r7 r5",
       "MUL r1 r6 r2"'''

'''"ADD r0 r1 r2",
       "ADD r3 r4 r5",
        "LDR r2 r9",
       "ADD r6 r7 r5",
       "MUL r1 r6 r2" '''

pc = 0                                  ## initializing pc to point first instruction
clk = 1
total = 1
mem = [i for i in range(1024)]          ## initializing main memory with zeros
reg = {'r0':4 ,'r1':5 ,'r2':9 ,'r3':7 ,'r4':1 ,'r5':17 ,'r6':10 ,'r7':0.0 ,'r8':12.67 ,'r9': 18.5 ,'r10':16.99 ,'r11':0 ,'r12':0 }       ### initializing registers
regSt = {'r0':'' ,'r1':'' ,'r2':'' ,'r3':'' ,'r4':'' ,'r5':'' ,'r6':'' ,'r7':'' ,'r8':'' ,'r9':'' ,'r10':'' ,'r11':'' ,'r12':'' } ##regStatus
ins = [
      "ADD r3 r1 r2",    ## each inst.. contains space seperated operation, operands etc.
      "FPM r7 r8 r9",
      "FPA r7 r10 r8",
      "LDR r0 r5",
      "STR r6 r0",
      "MUL r0 r5 r3",
      "MUL r5 r6 r2"
       ]            ### instruction array

stts = ['' for i in range(len(ins))]    ## check for other op in same clock
insF = ['' for i in range(len(ins))]    ## functional units assigned for each instructions
val = [0 for i in range(len(ins))]      ## array to store result of each instruction after its execution state
a = [0 for i in range(len(ins))]        ## storing the decoded values from the registers of each instruction
b = [0 for i in range(len(ins))]
#i1 = []
iSplit = []                             ## array to store substings(operation, operands) of each instruction

cycles = { 'INT' : 1 , 'MUL' : 19 , 'MUL1' : 19 , 'ADD' : 8, 'FPA': 30,'FPM':20}            ## clock cycles for each operation
count = { 'INT' : 0 , 'MUL' : 0 , 'MUL1' : 0 , 'ADD' : 0, 'DIV' : 0, 'FPA' : 0 , 'FPM' : 0} ## intial count for each operation
flag = [0 for i in range(len(ins))]
itbl = {i : '' for i in range(len(ins))}        ## instruction table(ScoreBoard)
for i in range(len(ins)):
    itbl[i] = iSt(0,0,0,0)
#print(itbl[0])
map = { 'INT' : fStatus() , 'MUL' : fStatus() , 'MUL1' : fStatus() , 'ADD' : fStatus(), 'DIV' : fStatus(), 'FPA' : fStatus(), 'FPM' : fStatus() }  ## list of all functional units present
#print(map[0].busy)
def prnt():                 ## to print the current scoreboard
    global pc
    print("inst    issue      ReadOp        Execute       WriteBack")
    for i in range(len(ins)):
        print(str(i+1)+"          "+str(itbl[i]))


def fetch():                ## to fetch the instruction at pc
    global pc,clk
    if pc < len(ins):
        i1 = []
        i1 = ins[pc].split()
        #print(i1)
        iSplit.append(i1)  ##issue
        # print(i1)
        if i1[0] == 'LDR' or i1[0] == 'STR':
            z = 'INT'
        elif i1[0] == 'MUL':
            if map['MUL'].busy == False:
                z = 'MUL'
            elif map['MUL1'].busy == False:
                z = 'MUL1'
            else:
                z = ''
        else:
            z = i1[0]
        insF[pc] = z
        # print(map[z].busy)
        if i1[0] != 'STR':
            #print("chk",regSt[i1[1]])
            if z != '' and map[z].busy == False and regSt[i1[1]] == '':         ## checking for structural hazards and WAW hazards
                #print('hii')
                map[z].busy = True
                map[z].op = i1[0]
                map[z].fi = i1[1]
                if i1[2][0] == 'r':
                    map[z].fj = i1[2]                                           ## assigning the flags for the registers of pc instruction based on their availability
                    if regSt[i1[2]] == '':
                        map[z].rj = True
                    else:
                        map[z].rj = False
                        map[z].qj = regSt[i1[2]]

                    #print(map[z].rj)
               # print(i1)
                if len(i1) > 3 and i1[3][0] == 'r':
                    map[z].fk = i1[3]
                    if regSt[i1[3]] == '':
                        map[z].rk = True
                    else:
                        map[z].rk = False
                        map[z].qk = regSt[i1[3]]
                regSt[i1[1]] = i1[0]
               # print("stts", regSt)
                itbl[pc].issue = clk                                            ## assigning the current clock for the issue stage of pc instruction
                stts[pc] = 'issue'
                prnt()
                #print(regSt[i1[1]])
                pc = pc + 1                                                     ## incrementing pc

        else:
           if map[z].busy == False and regSt[i1[2]] == '':
               map[z].busy = True
               map[z].op = i1[0]
               map[z].fi = i1[2]
               map[z].fj = i1[1]
               #print(i1[2])
               #print("hii",regSt[i1[1]])
               if regSt[i1[1]] == '':
                   map[z].rj = True
               else:
                   map[z].rj = False
                   map[z].qj = regSt[i1[1]]
               #print(map[z].rj)
               regSt[i1[2]] = i1[0]                                                 ## updating the destination register status with the operation of that instruction

                #regSt[i1[2]] = i1[0]  ##reStats update
              # print("stts",regSt)
               itbl[pc].issue = clk
               stts[pc] = 'issue'
               prnt()
               #print(regSt[i1[1]])
               pc = pc + 1



def decode():                                                                       ## decoding the instructions if their registers are available
    global pc, clk, a, b
    flag = 0
    f1 = 0
    f2 = 0
    store = -1
    for x in itbl:
        #print('i=', x, " ",clk)

        if itbl[x].issue != 0 and itbl[x].rdOp == 0 and stts[x] != 'issue':         ## proceeding to decode stage only if the instruction has finished its issue state
            #print(clk)
            #print(map[insF[x]].rk)
            #print(map[insF[x]].rj)

            #print(regSt[map[insF[x]].fk],"kkk")
            if map[insF[x]].rj == False and regSt[map[insF[x]].fj] == '':
                map[insF[x]].rj = True
            if map[insF[x]].rk == None:
                map[insF[x]].rk = True
            elif map[insF[x]].rk == False and regSt[map[insF[x]].fk] == '':
                map[insF[x]].rk = True                                              ## checking for RAW hazards and availability of registers

            #print(map[insF[x]].rk)
           # print(map[insF[x]].rj)
            #if map[insF[x]].op != regSt[map[insF[x]].fi]:
            for i in range(x+1, len(ins)):                                          ## checking if the next instructions are preventing the decoding of current instructions
                #print('vl ', x, " ",i)                                                due to their fetch happening earlier than the current instruction decode in the same clock
               # print("fkk",map[insF[x]].fj )                                         cycle
                if  insF[i] != '' and insF[x] != '' and map[insF[i]].fi == map[insF[x]].fj and itbl[i].issue == clk  and map[insF[x]].rj != True:
                    f1 = 1
                    store = i
                if insF[i] != '' and insF[x] != '' and map[insF[i]].fi == map[insF[x]].fk and itbl[i].issue == clk and map[insF[x]].rk != True:
                    f2 = 1
                    store = i
                if f1 == 1 or f2 == 1:
                    #itbl[i].issue = 0
                    #pc = pc -1
                   # print(insF[i],"dfg")
                    #print("i= ", i)
                   # print("str", store)
                    if insF[i] != '':
                        regSt[map[insF[i]].fi] = ''         ## giving access to current instruction to finish its decode by releasing the lock on the register
                    if f1==1:
                        map[insF[x]].rj = True
                    if f2 ==1:
                        map[insF[x]].rk = True



            if (map[insF[x]].rk == True or map[insF[x]].rk == None) and (map[insF[x]].rj == True or map[insF[x]].rj == None):
                if iSplit[x][0] != 'STR' and iSplit[x][0] != 'LDR':  ##decode
                    if iSplit[x][2][0] == '#':
                        a[x] = str(iSplit[x][2][1:])
                    elif iSplit[x][2][0] == 'r':                                            ### reading the operands from the source registers
                        a[x] = str(reg[iSplit[x][2]])
                    else:
                        a[x] = str(input("Enter a:"))

                    if iSplit[x][3][0] == '#':
                        b[x] = str(iSplit[x][3][1:])
                    elif iSplit[x][3][0] == 'r':
                        b[x] = str(reg[iSplit[x][3]])
                    else:
                        b[x] = str(input("Enter b:"))
                else:
                    if iSplit[x][0] != 'LDR':
                        a[x] = reg[iSplit[x][2]]
                    elif iSplit[x][0] != 'STR':
                        a[x] = reg[iSplit[x][1]]


                itbl[x].rdOp = clk                                                          ## assigning the current clock for the Read Operands stage of the instruction
                #print(store,"srttrr")
                if store != -1:
                    regSt[iSplit[store][1]] = iSplit[store][0]                              ## if a WAR hazard, reassigning the destination register status of that
                #print("store" , regSt[iSplit[store][1]])                                    # particular instrucion with its operation
                stts[x] = 'decode'
                prnt()


def execute():
    global pc, clk, val
    for x in itbl:
        if itbl[x].issue != 0 and itbl[x].rdOp != 0 and itbl[x].exe == 0 and stts[x] != 'decode':   ## checking if instruction has finished its
            if flag[x] == 0:                                                                         # decode stage but not its execution stage
                count[insF[x]] = cycles[insF[x]] - 1
                flag[x] = 1
                if count[insF[x]] == 0:
                    itbl[x].exe = clk
                    flag[x] = 0
                    if insF[x] == 'LDR':
                        val[x] = mem[a[x]]
                    if insF[x] == 'STR':
                        val[x] = a[x]
                    stts[x] = 'execute'
                    prnt()

            else:
                count[insF[x]] = count[insF[x]] - 1                                             ## counting the clock cycles for each instruction once it started execution
                if count[insF[x]] == 0:
                    itbl[x].exe = clk
                    flag[x] = 0
                    #print(insF[x])
                    if insF[x] == 'ADD':                                                            ## executing the instrucion by calling corresponding verilog module
                        val[x] = f.cla(str(a[x]), str(b[x]))
                       # print(val[x])
                    elif insF[x] == 'MUL':
                        val[x] = f.mul(str(a[x]), str(b[x]))
                    elif insF[x] == 'FPA':
                        #print(a[x], b[x],"hiibye")
                        val[x] = f.fpa(str(a[x]), str(b[x]))
                       # print(val[x])
                    elif insF[x] == 'FPM':
                        val[x] = f.fpm(str(a[x]), str(b[x]))
                    stts[x] = 'execute'
                    prnt()



def writebk():
    global pc, clk, total
    flg1 = 1
    flg2 = 1
    flg = 0
    tmp = 0
    for x in itbl:
        if itbl[x].issue != 0 and itbl[x].rdOp != 0 and itbl[x].exe != 0 and itbl[x].wb == 0 and stts[x] != 'execute' :     ## checking if the instruction has finished
            #print(clk)                                                                                                      # its exec stage and if ready to write the
            #print(x)                                                                                                        # result back

            for i in range(x):
                #print(map[insF[i]].fj)
                #print(map[insF[i]].fk)
                if itbl[i].rdOp != 0  :           ## checking if the previous instructions have finished their decode stage so that the current inst.. can finish its writeback
                    flg = 1                       ## checking for WAR hazards
                    if tmp != clk:
                        tmp = itbl[i].rdOp
                else:
                    flg = 0
                    if (map[insF[i]].fj == None):# map[insF[i]].rj == True):    ## checking for WAR hazards
                        flg1 = 1
                    elif map[insF[i]].fj == map[insF[x]].fi:
                        flg1 = 0
                    if iSplit[x][0] != 'STR':
                        if (map[insF[i]].fk == None):# or (map[insF[i]].fk == map[insF[x]].fi and itbl[i].rdOp != 0)  or(map[insF[i]].fk != map[insF[x]].fi):#map[insF[i]].rk == True):
                            flg2 = 1
                        elif map[insF[i]].fk == map[insF[x]].fi:
                            flg2 = 0
                    else:
                        flg2 = flg1

            '''if iSplit[x][0] == 'STR':
                flg2 = 1
                flg1 = 1'''
            #print(flg1)
            if (flg1 == 1 and flg2 == 1) or x == 0 or flg == 1:     ## writing the result back to the registers if no WAR hazard found
                if iSplit[x][0] == 'LDR':
                    reg[map[insF[x]].fi] = val[x]
                    #print(reg)
                    print(iSplit[x]," ",reg[map[insF[x]].fi])
                elif iSplit[x][0] == 'STR':
                    print("str", val[x])
                    mem[int(reg[map[insF[x]].fj])] = val[x]
                    #print(reg)
                    print(iSplit[x], " ", mem[int(reg[map[insF[x]].fj])])
                    #reg[map[insF[x]].fi] = val[x]
                else:
                    reg[map[insF[x]].fi] = val[x]
                    #print(reg)
                    print(iSplit[x], " ", reg[map[insF[x]].fi])
               # print(map[insF[x]].fi)
                regSt[map[insF[x]].fi] = ''                         ## releasing the lock for the destination register once it has been modified
                map[insF[x]] = fStatus()                            ## flushing the corresponding functional unit entry of that instruction ones it finishes writeback
                #print(map[insF[x]].fi)
                if tmp != clk:
                    itbl[x].wb = clk
                else:
                    itbl[x].wb = clk+1
                prnt()
                #print(stts[x])
                total = total + 1                                   ## counting the total no of instructions that finished their writeback(loop ending condition)
                #print(total,"total")
                stts[x] = 'writebk'


print(reg)
while total < len(ins)+1:
    fetch()
    decode()
    execute()
    writebk()
    for i in  range(len(ins)):
        stts[i] = ''
    clk = clk + 1
print(reg)
for i in ins:
    print(i)
