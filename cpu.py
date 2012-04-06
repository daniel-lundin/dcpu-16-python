#! /usr/bin/python
""" Implementation of DCPU-16 """
import sys
from values import create_value_dict
from constants import REG, OPCODE, opcode_to_instruction

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
        self.skip_instruction = False


    def execute(self, start):
        self.PC = start
        #PEACE_ON_EARTH = False
        #while not PEACE_ON_EARTH:
        for i in range(200):
            self.dispatch()
        self.halt('Instruction limit')

    def dispatch(self):
        """ Execute instruction at [PC] """
        instruction = self.ram[self.PC]
        self.PC += 1
        op_code = instruction & 0xf
        if op_code == 0x00:
            self.non_basic(instruction)
        else:
            oper1 = (instruction & 0x3f0) >> 4
            oper2 = (instruction & 0xfd00) >> 10
            a = self.VALUES[oper1].eval(self)
            b = self.VALUES[oper2].eval(self)
            if not self.skip_instruction:
                self.BASIC_INSTRUCTIONS[op_code](a, b)
            else:
                self.skip_instruction = False

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
            self.skip_instruction = True

    def IFN(self, a, b):
        self.skip_instruction = not (a.get(self) != b.get(self))

    def IFG(self, a, b):
        if a.get(self) <= b.get(self):
            self.skip_instruction = True

    def IFB(self, a, b):
        if not (a.get(self) & b.get(self)) != 0:
            self.skip_instruction = True

    def non_basic(self, instruction):
        opcode = (instruction >> 4) & 0b111111
        if(opcode != 0x01):
            return
        oper1 = (instruction >> 10)
        a = self.VALUES[oper1].eval(self)
        if self.skip_instruction:
            self.skip_instruction = False
            return
        # Push next address to the stack
        if self.SP < 0:
            self.halt('Stack overflow')
        self.SP -= 1
        self.ram[self.SP] = self.PC
        self.PC = a.get(self)

    def halt(self, msg):
        print "**** HALT *****"
        print "what: ", msg
        self.dump_registers()
        exit(2)

    def dump_registers(self):
        print "REGISTERS:"
        print ", ".join(["%d: %d" % (k, self.registers[k]) for k in self.registers.iterkeys()])

if __name__ == '__main__':
    # Test program
    cpu = CPU()
    cpu.ram[0] = 0x7c01
    cpu.ram[1] = 0x0030
    cpu.ram[2] = 0x7de1
    cpu.ram[3] = 0x1000
    cpu.ram[4] = 0x0020
    cpu.ram[5] = 0x7803
    cpu.ram[6] = 0x1000
    cpu.ram[7] = 0xc00d
    cpu.ram[8] = 0x7dc1
    cpu.ram[9] = 0x001a
    cpu.ram[10] = 0xa861
    cpu.ram[11] = 0x7c01
    cpu.ram[12] = 0x2000
    cpu.ram[13] = 0x2161
    cpu.ram[14] = 0x2000
    cpu.ram[15] = 0x8463
    cpu.ram[16] = 0x806d
    cpu.ram[17] = 0x7dc1
    cpu.ram[18] = 0x000d
    cpu.ram[19] = 0x9031
    cpu.ram[20] = 0x7c10
    cpu.ram[21] = 0x0018
    cpu.ram[22] = 0x7dc1
    cpu.ram[23] = 0x001a
    cpu.ram[24] = 0x9037
    cpu.ram[25] = 0x61c1
    cpu.ram[26] = 0x7dc1
    cpu.ram[27] = 0x001a
    cpu.ram[28] = 0x0000
    cpu.ram[29] = 0x0000
    cpu.ram[30] = 0x0000
    cpu.ram[31] = 0000
    cpu.execute(0)
    cpu.dump_registers()
    print "PC:", format(cpu.PC, 'x')
