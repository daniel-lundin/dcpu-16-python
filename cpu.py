""" Implementation of DCPU-16 """
from values import create_value_dict
from constants import REG_A, REG_B, REG_C, REG_X, REG_Y, REG_Z, REG_I, REG_J

class CPU(object):
    def __init__(self):
        self.registers = { 
            REG_A: 0, 
            REG_B: 0, 
            REG_C: 0, 
            REG_X: 0, 
            REG_Y: 0, 
            REG_Z: 0, 
            REG_I: 0, 
            REG_J: 0 
        } 
        self.ram = range(0x10000)
        self.SP=0xffff
        self.PC=0
        self.O=0x0
        self.BASIC_INSTRUCTIONS = {
            0x1: self.SET,
            0x2: self.ADD,
            0x3: self.SUB,
            0x4: self.MUL,
            0x5: self.DIV,
            0x6: self.MOD,
            0x7: self.SHL,
            0x8: self.SHR,
            0x9: self.AND,
            0xa: self.BOR,
            0xb: self.XOR,
            0xc: self.IFE,
            0xd: self.IFN,
            0xe: self.IFG,
            0xf: self.IFB,
        }

        self.VALUES = create_value_dict()


    def dispatch(self):
        """ Execute instruction at [PC] """
        instruction = self.ram[self.PC]
        self.PC += 1
        op_code = instruction & 0xf
        oper1 = (instruction & 0x3f0) >> 4
        oper2 = (instruction & 0xfd00) >> 10
        if op_code == 0x00:
            print "Only basic instructions supported"
            exit(1)
        self.BASIC_INSTRUCTIONS[op_code](oper1, oper2)

    def SET(self, a, b):
        self.VALUES[a].set(self, self.VALUES[b].get(self))

    def ADD(self, a, b):
        pass

    def SUB(self, a, b):
        pass

    def MUL(self, a, b):
        pass

    def DIV(self, a, b):
        pass

    def MOD(self, a, b):
        pass

    def SHL(self, a, b):
        pass

    def SHR(self, a, b):
        pass

    def AND(self, a, b):
        pass

    def BOR(self, a, b):
        pass

    def XOR(self, a, b):
        pass

    def IFE(self, a, b):
        pass

    def IFN(self, a, b):
        pass

    def IFG(self, a, b):
        pass

    def IFB(self, a, b):
        pass

if __name__ == '__main__':
    cpu = CPU()
    cpu.ram[0] = 0x7c01
    cpu.dispatch()
    #cpu.ram[0] = 0xa861
    #cpu.dispatch()
