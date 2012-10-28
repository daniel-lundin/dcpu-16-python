from values import value_lookup
from constants import OPCODE
from utils import unpack_instruction


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
        instruction = self.cpu.ram[self.cpu.PC.value].value
        self.cpu.PC.value = self.cpu.PC.value + 1
        op_code, b, a = unpack_instruction(instruction)
        if op_code == 0x00:
            self.non_basic(instruction)
        else:
            b = value_lookup(self.cpu, b, as_a=False)
            a = value_lookup(self.cpu, a, as_a=True)
            if not self.cpu.skip_instruction:
                self.BASIC_INSTRUCTIONS[op_code](b, a)
            else:
                self.cpu.skip_instruction = False

    def SET(self, b, a):
        b.value = a.value

    def ADD(self, b, a):
        sum = a.value + b.value
        self.cpu.EX.value = 0xffff if sum > 0xffff else 0
        sum = sum & 0xffff
        b.value = sum

    def SUB(self, b, a):
        res = b.value - a.value
        self.cpu.EX.value = 0x0
        if res < 0:
            self.cpu.EX.value = 0xffff
            res = -1 * res
        b.value = res

    def MUL(self, b, a):
        res = b.value * a.value
        self.cpu.EX.value = ((res >> 16) & 0xffff)
        res = res & 0xffff
        b.value = res

    def DIV(self, b, a):
        if a.value == 0:
            b.value = 0
        bval = b.value
        b.value = bval / a.value
        self.cpu.EX.value = ((bval << 16) / a.value) & 0xffff

    def MOD(self, b, a):
        b.value = b.value % a.value

    def SHL(self, b, a):
        b.value = b.value << a.value
        self.cpu.EX.vale = (b.value << a.value >> 16) & 0xfff

    def SHR(self, b, a):
        b.value = b.value >> a.value
        self.cpu.EX.value = (b.value << 16) >> a.value & 0xfff

    def AND(self, b, a):
        b.value = b.value & a.value

    def BOR(self, b, a):
        b.value = b.value | a.value

    def XOR(self, b, a):
        b.value = b.value ^ a.value

    def IFE(self, b, a):
        if a.value != b.value:
            self.cpu.skip_instruction = True

    def IFN(self, b, a):
        self.cpu.skip_instruction = not (a.value != b.value)

    def IFG(self, b, a):
        if b.value > a.value:
            self.cpu.skip_instruction = True

    def IFB(self, b, a):
        if not (a.value & b.value) != 0:
            self.cpu.skip_instruction = True

    def non_basic(self, instruction):
        opcode = (instruction >> 4) & 0b111111
        if(opcode != 0x01):
            return
        oper1 = (instruction >> 10)
        a = value_lookup(self.cpu, oper1, as_a=True)
        if self.cpu.skip_instruction:
            self.cpu.skip_instruction = False
            return
        # Push next address to the stack
        if self.cpu.SP.value < 0:
            self.halt('Stack overflow')
        self.cpu.SP.value -= 1
        self.cpu.ram[self.cpu.SP.value].value = self.cpu.PC.value
        self.cpu.PC.value = a.value

    def halt(self, msg):
        print "**** HALT *****"
        print "what: ", msg
        self.cpu.dump_registers()
        exit(2)
