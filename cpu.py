from constants import REG, regidx_to_name


class MemoryCell(object):
    def __init__(self, value):
        self.value = value


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
        self.ram = [MemoryCell(0) for _ in range(0x10000)]
        self.SP = 0xffff
        self.PC = 0
        self.O = 0x0
        self.skip_instruction = False

    def dump_registers(self):
        print "REGISTERS:"
        print ", ".join(["%s: %d" % (regidx_to_name[k], self.registers[k])
                        for k in self.registers.iterkeys()])
