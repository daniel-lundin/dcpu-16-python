#! /usr/bin/python
""" Implementation of DCPU-16 """
import sys
import optparse
import struct
from values import create_value_dict
from constants import REG, OPCODE, opcode_to_instruction, regidx_to_name

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


    def execute(self, start, limit=None):
        self.PC = start
        if limit:
            for i in range(limit):
                self.dispatch()
            self.halt('Instruction limit reached')
        else:
            PEACE_ON_EARTH = False
            while not PEACE_ON_EARTH:
                self.dispatch()

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
        print ", ".join(["%s: %d" % (regidx_to_name[k], self.registers[k]) for k in self.registers.iterkeys()])

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option('-f', '--file', dest="file", help="Program file")
    optparser.add_option('-l', '--limit', dest="limit", help="Max number of instructions to execute")
    (options, args) = optparser.parse_args(sys.argv)
    
    if not options.file:
        optparser.print_help()
        exit(1)

    cpu = CPU()
    limit = None
    if options.limit:
        limit = int(options.limit, 0) # Guess base
    f = open(options.file)
    data = f.read()
    words = struct.unpack('>%dH' % (len(data)/2), data)
    for word, idx in zip(words, range(len(words))):
        cpu.ram[idx] = word
        

    cpu.execute(0, limit)

