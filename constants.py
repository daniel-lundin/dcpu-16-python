class REG(object):
    A = 0x0
    B = 0x1
    C = 0x2
    X = 0x3
    Y = 0x4
    Z = 0x5
    I = 0x6
    J = 0x7

    SP = 0x1b
    PC = 0x1c
    EX  = 0x1d

class OPCODE(object):
    SET = 0x1 
    ADD = 0x2 
    SUB = 0x3 
    MUL = 0x4 
    DIV = 0x5 
    MOD = 0x6 
    SHL = 0x7 
    SHR = 0x8 
    AND = 0x9 
    BOR = 0xa 
    XOR = 0xb 
    IFE = 0xc 
    IFN = 0xd 
    IFG = 0xe 
    IFB = 0xf 

opcode_to_instruction = {
    0x1: 'SET',
    0x2: 'ADD',
    0x3: 'SUB',
    0x4: 'MUL',
    0x5: 'DIV',
    0x6: 'MOD',
    0x7: 'SHL',
    0x8: 'SHR',
    0x9: 'AND',
    0xa: 'BOR',
    0xb: 'XOR',
    0xc: 'IFE',
    0xd: 'IFN',
    0xe: 'IFG',
    0xf: 'IFB',
}
regidx_to_name = {
    0x0: 'A',
    0x1: 'B',
    0x2: 'C',
    0x3: 'X',
    0x4: 'Y',
    0x5: 'Z',
    0x6: 'I',
    0x7: 'J',
}
