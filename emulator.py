from ctypes import c_int16, c_uint16
from values import value_lookup
from constants import OPCODE
from utils import unpack_instruction, unpack_special_instruction


class Emulator(object):
    def __init__(self, cpu):
        self.cpu = cpu

        self.BASIC_INSTRUCTIONS = {
            OPCODE.SET: self.SET,
            OPCODE.ADD: self.ADD,
            OPCODE.SUB: self.SUB,
            OPCODE.MUL: self.MUL,
            OPCODE.MLI: self.MLI,
            OPCODE.DIV: self.DIV,
            OPCODE.DVI: self.DVI,
            OPCODE.MOD: self.MOD,
            OPCODE.MDI: self.MDI,
            OPCODE.AND: self.AND,
            OPCODE.BOR: self.BOR,
            OPCODE.XOR: self.XOR,
            OPCODE.SHR: self.SHR,
            OPCODE.ASR: self.ASR,
            OPCODE.SHL: self.SHL,
            OPCODE.IFB: self.IFB,
            OPCODE.IFC: self.IFC,
            OPCODE.IFE: self.IFE,
            OPCODE.IFN: self.IFN,
            OPCODE.IFG: self.IFG,
            OPCODE.IFA: self.IFA,
            OPCODE.IFL: self.IFL,
            OPCODE.IFU: self.IFU,
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
        op_code, b_val, a_val = unpack_instruction(instruction)
        if op_code == 0x00:
            self.non_basic(instruction)
        else:
            b = value_lookup(self.cpu, b_val, as_a=False)
            a = value_lookup(self.cpu, a_val, as_a=True)
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
        b.value = res

    def MLI(self, b, a):
        a_signed = c_int16(a.value)
        b_signed = c_int16(b.value)
        res = c_uint16(b_signed.value * a_signed.value)
        self.cpu.EX.value = ((res.value >> 16) & 0xffff)
        b.value = res.value

    def DIV(self, b, a):
        if a.value == 0:
            b.value = 0
        bval = b.value
        b.value = bval / a.value
        self.cpu.EX.value = ((bval << 16) / a.value) & 0xffff

    def DVI(self, b, a):
        if a.value == 0:
            b.value = 0
        b_signed = c_int16(b.value)
        a_signed = c_int16(a.value)
        b.value = b_signed.value / a_signed.value
        self.cpu.EX.value = ((b_signed.value << 16) / a.value) & 0xffff

    def MOD(self, b, a):
        if a.value == 0:
            b.value = 0
        b.value = b.value % a.value

    def MDI(self, b, a):
        if c_int16(b.value).value < 0:
            b.value = b.value
        else:
            b.value = b.value % a.value

    def AND(self, b, a):
        b.value = b.value & a.value

    def BOR(self, b, a):
        b.value = b.value | a.value

    def XOR(self, b, a):
        b.value = b.value ^ a.value

    def SHR(self, b, a):
        b.value = b.value >> a.value
        self.cpu.EX.value = (b.value << 16) >> a.value & 0xffff

    def ASR(self, b, a):
        b_signed = c_int16(b.value)
        b.value = b_signed.value >> a.value
        self.cpu.EX.value = (b_signed.value << 16) >> a.value & 0xffff

    def SHL(self, b, a):
        b.value = b.value << a.value
        self.cpu.EX.vale = (b.value << a.value >> 16) & 0xffff

    def IFB(self, b, a):
        if not (a.value & b.value) != 0:
            self.cpu.skip_instruction = True

    def IFC(self, b, a):
        if not (a.value & b.value) == 0:
            self.cpu.skip_instruction = True

    def IFE(self, b, a):
        if a.value != b.value:
            self.cpu.skip_instruction = True

    def IFN(self, b, a):
        self.cpu.skip_instruction = not (a.value != b.value)

    def IFG(self, b, a):
        if b.value <= a.value:
            self.cpu.skip_instruction = True

    def IFA(self, b, a):
        if c_int16(b.value).value <= c_int16(a.value).value:
            self.cpu.skip_instruction = True

    def IFL(self, b, a):
        if b.value >= a.value:
            self.cpu.skip_instruction = True

    def IFU(self, b, a):
        if c_int16(b.value).value >= c_int16(a.value).value:
            self.cpu.skip_instruction = True

    def non_basic(self, instruction):
        opcode, a_val = unpack_special_instruction(instruction)
        if(opcode != OPCODE.JSR):
            return
        a = value_lookup(self.cpu, a_val, as_a=True)
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
