#! /usr/bin/python
""" Implementation of DCPU-16 """
import sys
from values import create_value_dict
from constants import REG, OPCODE

class CPU(object):
    def __init__(self):
        self.registers = {
            REG.A: 0,
            REG.B: 0,
            REG.C: 0,
            REG.X: 0,
            REG.Y: 0,
            REG.Z: 0,
            REG.I: 0,
            REG.J: 0
        }
        self.ram = [0 for _ in range(0x10000)]
        self.SP=0xffff
        self.PC=0
        self.O=0x0
        self.BASIC_INSTRUCTIONS = {
            OPCODE.SET: self.SET,
            OPCODE.ADD: self.ADD,
            OPCODE.SUB: self.SUB,
            OPCODE.MUL: self.MUL,
            OPCODE.DIV: self.DIV,
            OPCODE.MOD: self.MOD,
            OPCODE.SHL: self.SHL,
            OPCODE.SHR: self.SHR,
            OPCODE.AND: self.AND,
            OPCODE.BOR: self.BOR,
            OPCODE.XOR: self.XOR,
            OPCODE.IFE: self.IFE,
            OPCODE.IFN: self.IFN,
            OPCODE.IFG: self.IFG,
            OPCODE.IFB: self.IFB,
        }

        self.VALUES = create_value_dict()


    def execute(self, start):
        self.PC = start
        PEACE_ON_EARTH = False
        while not PEACE_ON_EARTH:
            self.dispatch()

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
        a = self.VALUES[oper1]
        b = self.VALUES[oper2]
        a.eval(self)
        b.eval(self)
        self.BASIC_INSTRUCTIONS[op_code](a, b)

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
        if b.get(self) == 0:
            a.set(self, 0)
        aval = a.get(self)
        a.set(self, aval/b.get(self))
        self.O == ((aval<<16)/b.get(self))&0xffff

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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: cpu program'
        exit(0)
    cpu = CPU()
    import ipdb
    ipdb.set_trace()
    f = open(sys.argv[1], 'r+b')
    all_data = f.read()
    for idx, byte in zip(range(len(all_data)), all_data):
        cpu.ram[idx] = byte

    cpu.dispatch()
