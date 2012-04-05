import random
import unittest

from cpu import CPU
from constants import *

class TestSequenceFunctions(unittest.TestCase):

    def test_set_reg_to_literal(self):
        """ Sets a register to a literal """
        cpu = CPU()
        cpu.ram[0] = 0xc001 # SET A, 0x10
        cpu.dispatch()
        self.assertTrue(cpu.registers[REG_A] == 0x10, "Register value error")

    def test_set_addr_of_reg(self):
        """ Sets ram pointed by REG_I to value of REG_B """
        cpu = CPU()
        # Arrange
        cpu.registers[REG_I] = 0xff
        cpu.registers[REG_B] = 0x11

        # Act
        # REG_B  [REG_I] SET
        # 000001 001110  0001
        cpu.ram[0] = 0x4e1 # SET [I], B
        cpu.dispatch()

        self.assertTrue(cpu.ram[0xff] == 0x11, "Ram not updated correctly")


if __name__ == '__main__':
    unittest.main()

