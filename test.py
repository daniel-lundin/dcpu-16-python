import random
import unittest

from cpu import CPU
from constants import *

class TestValues(unittest.TestCase):

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

    def test_pop_into_reg(self):
        """ Pops from stack into register """
        cpu = CPU()
        cpu.ram[cpu.SP] = 0xdead

        # POP     REG_A  SET
        # 011000  000000 0001
        cpu.ram[0] = 0x6001 # SET A, PUSH
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xdead, "Stack popping b0rked")

    def test_push_from_register(self):
        """ Pushed value in register to stack """
        cpu = CPU()
        cpu.registers[REG_A] = 0xdead

        # POP     PUSH   SET
        # 000000  011010 0001
        cpu.ram[0] = 0x1a1 # SET PUSH, A
        cpu.dispatch()

        self.assertTrue(cpu.ram[cpu.SP] == 0xdead, "Stack pushing b0rked")

    def test_peek_into_register(self):
        """ Pushed value in register to stack """
        cpu = CPU()
        cpu.ram[cpu.SP] = 0xbeef

        # PEEK   REG_A   SET
        # 011001 000000  0001
        cpu.ram[0] = 0x6401 # SET A, PEEK
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xbeef, "Stack peeking b0rked")

    def test_set_sp(self):
        """ Sets SP """
        cpu = CPU()
        
        # 0x2    SP     SET
        # 100010 011011 0001
        cpu.ram[0] = 0x89b1
        cpu.dispatch()

        self.assertTrue(cpu.SP == 0x2, "SP Loading failed")

    def test_set_pc(self):
        """ Sets PC """
        cpu = CPU()
        
        # 0x2    PC     SET
        # 100010 011100 0001
        cpu.ram[0] = 0x89c1
        cpu.dispatch()

        self.assertTrue(cpu.PC == 0x2, "PC Loading failed")

    def test_read_o(self):
        """ Reads O into register """
        cpu = CPU()
        cpu.O = 0xffff
        
        # O      REG_A  SET
        # 011101 000000 0001
        cpu.ram[0] = 0x7401
        cpu.dispatch()

        self.assertTrue(cpu.O == 0xffff, "O Loading failed")

if __name__ == '__main__':
    unittest.main()

