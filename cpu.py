""" Implementation of DCPU-16 """
from values import RegisterValue, RegisterRamValue

# REGISTERS
A=0
B=1
C=2
X=3
Y=4
Z=5
I=6
J=7

class CPU(object):
    def __init__(self):
        self.registers = { A: 0, B: 0, C: 0, X: 0, Y: 0, Z: 0, I: 0, J: 0 } 
        self.ram = range(0x10000)
        self.SP=0xffff
        self.PC=0
        self.O=False
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

        self.VALUES = {
            0x0:  RegisterValue(A),
            0x1:  RegisterValue(B),
            0x2:  RegisterValue(C),
            0x3:  RegisterValue(X),
            0x4:  RegisterValue(Y),
            0x5:  RegisterValue(Z),
            0x6:  RegisterValue(I),
            0x7:  RegisterValue(J),

            0x8:  RegisterRamValue(A),
            0x9:  RegisterRamValue(B),
            0xa:  RegisterRamValue(C),
            0xb:  RegisterRamValue(X),
            0xc:  RegisterRamValue(Y),
            0xd:  RegisterRamValue(Z),
            0xe:  RegisterRamValue(I),
            0xf:  RegisterRamValue(J),
            # ----------------------
            # [Next word + register]
            # ----------------------
            #0x18: self.pop, 
            #0x19: self.peek, 
            #0x1a: self.push, 
            #0x1b: lambda: self.SP,
            #0x1c: lambda: self.PC,
            #0x1d: lambda: self.O,
            #0x1e: lambda: self.O,
        }


    def dispatch(self):
        """ Execute instruction at [PC] """
        word = self.ram[self.PC]
        print word

    def SET(self, a, b):
        self.values[a].set(self.values[b].get())

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

