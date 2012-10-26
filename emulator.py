from values import create_value_dict
from constants import OPCODE


class Emulator(object):
    def __init__(self, cpu):
        self.cpu = cpu

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

    def execute(self, start, limit=None):
        self.cpu.PC = start
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
        instruction = self.cpu.ram[self.cpu.PC]
        self.cpu.PC += 1
        op_code = instruction & 0xf
        if op_code == 0x00:
            self.non_basic(instruction)
        else:
            oper1 = (instruction & 0x3f0) >> 4
            oper2 = (instruction & 0xfd00) >> 10
            a = self.VALUES[oper1].eval(self.cpu)
            b = self.VALUES[oper2].eval(self.cpu)
            if not self.cpu.skip_instruction:
                self.BASIC_INSTRUCTIONS[op_code](a, b)
            else:
                self.cpu.skip_instruction = False

    def SET(self, a, b):
        a.set(self.cpu, b.get(self.cpu))

    def ADD(self, a, b):
        sum = a.get(self.cpu) + b.get(self.cpu)
        self.cpu.O = 0xffff if sum > 0xffff else 0
        sum = sum & 0xffff
        a.set(self.cpu, sum)

    def SUB(self, a, b):
        res = a.get(self.cpu) - b.get(self.cpu)
        self.cpu.O = 0x0
        if res < 0:
            self.cpu.O = 0xffff
            res = -1 * res
        a.set(self.cpu, res)

    def MUL(self, a, b):
        res = a.get(self.cpu) * b.get(self.cpu)
        self.cpu.O = (res >> 16) & 0xffff
        res = res & 0xffff
        a.set(self.cpu, res)

    def DIV(self, a, b):
        if b.get(self.cpu) == 0:
            a.set(self.cpu, 0)
        aval = a.get(self.cpu)
        a.set(self.cpu, aval / b.get(self.cpu))
        self.cpu.O == ((aval << 16) / b.get(self.cpu)) & 0xffff

    def MOD(self, a, b):
        a.set(self.cpu, a.get(self.cpu) % b.get(self.cpu))

    def SHL(self, a, b):
        a.set(self.cpu, a.get(self.cpu) << b.get(self.cpu))
        self.cpu.O = (a.get(self.cpu) << b.get(self.cpu) >> 16) & 0xfff

    def SHR(self, a, b):
        a.set(self.cpu, a.get(self.cpu) >> b.get(self.cpu))
        self.cpu.O = (a.get(self.cpu) << 16) >> b.get(self.cpu) & 0xfff

    def AND(self, a, b):
        a.set(self.cpu, a.get(self.cpu) & b.get(self.cpu))

    def BOR(self, a, b):
        a.set(self.cpu, a.get(self.cpu) | b.get(self.cpu))

    def XOR(self, a, b):
        a.set(self.cpu, a.get(self.cpu) ^ b.get(self.cpu))

    def IFE(self, a, b):
        if a.get(self.cpu) != b.get(self.cpu):
            self.cpu.skip_instruction = True

    def IFN(self, a, b):
        self.cpu.skip_instruction = not (a.get(self.cpu) != b.get(self.cpu))

    def IFG(self, a, b):
        if a.get(self.cpu) <= b.get(self.cpu):
            self.cpu.skip_instruction = True

    def IFB(self, a, b):
        if not (a.get(self.cpu) & b.get(self.cpu)) != 0:
            self.cpu.skip_instruction = True

    def non_basic(self, instruction):
        opcode = (instruction >> 4) & 0b111111
        if(opcode != 0x01):
            return
        oper1 = (instruction >> 10)
        a = self.VALUES[oper1].eval(self.cpu)
        if self.cpu.skip_instruction:
            self.cpu.skip_instruction = False
            return
        # Push next address to the stack
        if self.cpu.SP < 0:
            self.halt('Stack overflow')
        self.cpu.SP -= 1
        self.cpu.ram[self.cpu.SP] = self.cpu.PC
        self.cpu.PC = a.get(self.cpu)

    def halt(self, msg):
        print "**** HALT *****"
        print "what: ", msg
        self.cpu.dump_registers()
        exit(2)
