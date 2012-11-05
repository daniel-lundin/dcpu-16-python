from ctypes import c_uint16
from constants import REG, regidx_to_name


class MemoryCell(object):
    """ For debugging, keeps track of where the cell is """
    def __init__(self, value, hint=''):
        self.value = c_uint16(value)
        self.hint = hint

    def __repr__(self):
        return '<%s> %d' % (self.hint, self.value)

class CPU(object):
    def __init__(self, memory_type=c_uint16):
        self.registers = {
            REG.A: memory_type(0),
            REG.B: memory_type(0),
            REG.C: memory_type(0),
            REG.X: memory_type(0),
            REG.Y: memory_type(0),
            REG.Z: memory_type(0),
            REG.I: memory_type(0),
            REG.J: memory_type(0)
        }
        self.ram = [memory_type(0) for x in range(0x10000)]
        self.SP = memory_type(0xffff)
        self.PC = memory_type(0)
        self.EX = memory_type(0)
        self.skip_instruction = False

    def dump_registers(self):
        print "REGISTERS:"
        print ", ".join(["%s: %d" % (regidx_to_name[k], self.registers[k])
                        for k in self.registers.iterkeys()])
