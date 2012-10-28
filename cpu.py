from constants import REG, regidx_to_name


# Do operating overload to get rid of get/set?
class MemoryCell(object):
    def __init__(self, value, hint=''):
        self.value = value
        self.hint = hint

    def __repr__(self):
        return '<%s> %d' % (self.hint, self.value)

class CPU(object):
    def __init__(self):
        self.registers = {
            REG.A: MemoryCell(0, 'REG A'),
            REG.B: MemoryCell(0, 'REG B'),
            REG.C: MemoryCell(0, 'REG C'),
            REG.X: MemoryCell(0, 'REG X'),
            REG.Y: MemoryCell(0, 'REG Y'),
            REG.Z: MemoryCell(0, 'REG Z'),
            REG.I: MemoryCell(0, 'REG I'),
            REG.J: MemoryCell(0, 'REG J')
        }
        self.ram = [MemoryCell(0, 'MEM %d' % x) for x in range(0x10000)]
        self.SP = MemoryCell(0xffff, 'SP')
        self.PC = MemoryCell(0, 'PC')
        self.EX = MemoryCell(0, 'EX')
        self.skip_instruction = False

    def dump_registers(self):
        print "REGISTERS:"
        print ", ".join(["%s: %d" % (regidx_to_name[k], self.registers[k])
                        for k in self.registers.iterkeys()])
