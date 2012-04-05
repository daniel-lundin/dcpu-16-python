from constants import REG_A, REG_B, REG_C, REG_X, REG_Y, REG_Z, REG_I, REG_J

class RegisterValue(object):

    def __init__(self, register):
        self.register = register

    def set(self, cpu, val):
        cpu.registers[self.register] = val

    def get(self, cpu):
        return cpu.registers[self.register]

class RegisterRamValue(object):

    def __init__(self, register):
        self.register = register

    def set(self, cpu, val):
        cpu.ram[cpu.registers[self.register]] = val

    def get(self, cpu):
        return cpu.ram[cpu.registers[self.register]]

class RegisterRamNextWordOffset(object):
    def __init__(self, register):
        self.register = register

    def set(self, cpu, val):
        cpu.PC += 1
        cpu.ram[cpu.registers[self.register] + cpu.ram[cpu.PC]] = val

    def get(self, cpu):
        return cpu.ram[cpu.registers[self.register] + cpu.ram[cpu.PC]]

class Literal(object):
    def __init__(self, value):
        self.value = value

    def get(self, cpu):
        return self.value

    def set(self, cpu, value):
        print "Illegal set on literal"

class StackPop(object):
    def get(self, cpu):
        val = cpu.ram[cpu.SP]
        cpu.SP += 1
        return val

    def set(self, cpu, value):
        print 'stack pop put?'

class StackPush(object):
    def get(self, cpu):
        print 'error: reading push'

    def set(self, cpu, value):
        cpu.SP -= 1
        cpu.ram[cpu.SP] = value

class StackPeek(object):
    def get(self, cpu):
        return cpu.ram[cpu.SP]

    def set(self, cpu, value):
        cpu.ram[cpu.SP] = value

class SPValue(object):
    def get(self, cpu):
        return CPU.SP

    def set(self, cpu, value):
        cpu.SP = value

class PCValue(object):
    def get(self, cpu):
        return CPU.PC

    def set(self, cpu, value):
        cpu.PC = value

class OValue(object):
    def get(self, cpu):
        return cpu.O

    def set(self, cpu, value):
        cpu.O = value

def create_value_dict():
        return {
            0x0:  RegisterValue(REG_A),
            0x1:  RegisterValue(REG_B),
            0x2:  RegisterValue(REG_C),
            0x3:  RegisterValue(REG_X),
            0x4:  RegisterValue(REG_Y),
            0x5:  RegisterValue(REG_Z),
            0x6:  RegisterValue(REG_I),
            0x7:  RegisterValue(REG_J),

            0x8:  RegisterRamValue(REG_A),
            0x9:  RegisterRamValue(REG_B),
            0xa:  RegisterRamValue(REG_C),
            0xb:  RegisterRamValue(REG_X),
            0xc:  RegisterRamValue(REG_Y),
            0xd:  RegisterRamValue(REG_Z),
            0xe:  RegisterRamValue(REG_I),
            0xf:  RegisterRamValue(REG_J),
            0x10: RegisterRamNextWordOffset(REG_A),
            0x11: RegisterRamNextWordOffset(REG_B),
            0x12: RegisterRamNextWordOffset(REG_C),
            0x13: RegisterRamNextWordOffset(REG_X),
            0x14: RegisterRamNextWordOffset(REG_Y),
            0x15: RegisterRamNextWordOffset(REG_Z),
            0x16: RegisterRamNextWordOffset(REG_I),
            0x17: RegisterRamNextWordOffset(REG_J),
            0x18: StackPop(),
            0x19: StackPeek(),
            0x1a: StackPush(),
            0x1b: SPValue(),
            0x1c: PCValue(),
            0x1d: OValue(),
            #0x1e: lambda: self.O,
            # Literals
            0x20: Literal(0x00),
            0x21: Literal(0x01),
            0x22: Literal(0x02),
            0x23: Literal(0x03),
            0x24: Literal(0x04),
            0x25: Literal(0x05),
            0x26: Literal(0x06),
            0x27: Literal(0x07),
            0x28: Literal(0x08),
            0x29: Literal(0x09),
            0x2a: Literal(0x0a),
            0x2b: Literal(0x0b),
            0x2c: Literal(0x0c),
            0x2d: Literal(0x0d),
            0x2e: Literal(0x0e),
            0x2f: Literal(0x0f),
            0x30: Literal(0x10),
            0x31: Literal(0x11),
            0x32: Literal(0x12),
            0x33: Literal(0x13),
            0x34: Literal(0x14),
            0x35: Literal(0x15),
            0x36: Literal(0x16),
            0x37: Literal(0x17),
            0x38: Literal(0x18),
            0x39: Literal(0x19),
            0x3a: Literal(0x1a),
            0x3b: Literal(0x1b),
            0x3c: Literal(0x1c),
            0x3d: Literal(0x1d),
            0x3e: Literal(0x1e),
            0x3f: Literal(0x1f)
        }
