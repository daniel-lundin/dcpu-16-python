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
        self.ram = [0 for _ in range(0x10000)]
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
        op_code = instruction & 0xf
        oper1 = (instruction & 0x3f0) >> 4
        oper2 = (instruction & 0xfd00) >> 10
        if op_code == 0x00:
            print "Only basic instructions supported"
            exit(1)
        a = self.VALUES[oper1]
        b = self.VALUES[oper2]
        a.eval(self)
        b.eval(self)
        self.BASIC_INSTRUCTIONS[op_code](a, b)
        self.PC += 1

    def SET(self, a, b):
        a.set(self, b.get(self))

    def ADD(self, a, b):
        sum = a.get(self) + b.get(self)
        self.O = 0xffff if sum > 0xffff else 0
        sum = sum & 0xffff
        a.set(self, sum)

    def SUB(self, a, b):
        res = a.get(self) - b.get(self)
        self.O = 0x0
        if res < 0:
            self.O = 0xffff
            res = -1*res
        a.set(self, res)

    def MUL(self, a, b):
        res = a.get(self) * b.get(self)
        self.O = (res>>16)&0xffff
        res = res & 0xffff
        a.set(self, res)

    def DIV(self, a, b):
        bval = b.get(self)
        if bval == 0:
            a.set(self, 0)
        aval = a.get(self)
        a.set(self, aval/bval)
        self.O == ((aval<<16)/bval)&0xffff

    def MOD(self, a, b):
        a.set(self, a.get(self) % b.get(self))

    def SHL(self, a, b):
        a.set(self, a.get(self) << b.get(self))
        self.O = (a.get(self) << b.get(self) >> 16) & 0xfff

    def SHR(self, a, b):
        a.set(self, a.get(self) >> b.get(self))
        self.O = (a.get(self) << 16) >> b.get(self) & 0xfff


    def AND(self, a, b):
        a.set(self, a.get(self) & b.get(self))

    def BOR(self, a, b):
        a.set(self, a.get(self) | b.get(self))

    def XOR(self, a, b):
        a.set(self, a.get(self) ^ b.get(self))

    def IFE(self, a, b):
        if a.get(self) != b.get(self):
            self.PC += 1

    def IFN(self, a, b):
        if a.get(self) == b.get(self):
            self.PC += 1

    def IFG(self, a, b):
        if a.get(self) <= b.get(self):
            self.PC += 1

    def IFB(self, a, b):
        if not (a.get(self) & b.get(self)) != 0:
            self.PC += 1

