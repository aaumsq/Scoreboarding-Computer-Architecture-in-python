# Scoreboarding-Computer-Architecture-in-python
Implementation of Scoreboarding, a technique for dynamically scheduling a pipeline so that the instructions can execute out of order when there are no conflicts and the hardware is available, in python
The verilog modules required for the functional units, used during the execution stage, are imported from a separate python file(functions.py). 

The input instructions are added in the instruction array in the code separated by a comma.  
ins = [ "ADD r3 r1 r2",    ## each inst.. contains space seperated operation, operands etc.      
        "ADD r4 r3 r0",      
        "LDR r0 r5",      
        "STR r5 r1"    ]            ### instruction array 
 
The output is the instruction status table, showing the clock cycles required for each stage, obtained after successful execution of every stage of instruction, the initial register array before calling the scoreboard and the same register array after the instructiuns have finished their writing to the registers. 

Sample Input:

ADD r3 r1 r2
FPM r7 r8 r9
FPA r7 r10 r8
LDR r0 r5
STR r6 r0
MUL r0 r5 r3
MUL r5 r6 r2        ### These instructions should be added in the instruction array as shown above.


Output:

inst    issue      ReadOp        Execute       WriteBack                                                                                   
1          1          2           10            11                                                                                         
2          2          3           23            24                                                                                         
3          25          26           56            57                                                                                       
4          26          27           28            29                                                                                       
5          30          31           32            33                                                                                       
6          34          35           54            55                                                                                       
7          35          36           55            56                                                                                       
