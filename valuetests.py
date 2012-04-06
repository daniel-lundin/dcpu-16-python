import random
import unittest

from cpu import CPU
from constants import REG, OPCODE
from utils import pack_instruction

class TestValues(unittest.TestCase):

    def test_set_reg_to_literal(self):
        """ Sets a register to a literal """
        cpu = CPU()
        cpu.ram[0] = 0xc001 # SET A, 0x10
        cpu.dispatch()
        self.assertTrue(cpu.registers[REG.A] == 0x10, "Register value error")

    def test_set_addr_of_reg(self):
        """ Sets ram pointed by REG.I to value of REG.B """
        cpu = CPU()
        # Arrange
        cpu.registers[REG.I] = 0xff
        cpu.registers[REG.B] = 0x11

        # Act
        # REG.B  [REG.I] SET
        # 000001 001110  0001
        cpu.ram[0] = 0x4e1 # SET [I], B
        cpu.dispatch()

        self.assertTrue(cpu.ram[0xff] == 0x11, "Ram not updated correctly")

    def test_pop_into_reg(self):
        """ Pops from stack into register """
        cpu = CPU()
        cpu.ram[cpu.SP] = 0xdead

        # POP     REG.A  SET
        # 011000  000000 0001
        cpu.ram[0] = 0x6001 # SET A, PUSH
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG.A] == 0xdead, "Stack popping b0rked")

    def test_push_from_register(self):
        """ Pushed value in register to stack """
        cpu = CPU()
        cpu.registers[REG.A] = 0xdead

        # POP     PUSH   SET
        # 000000  011010 0001
        cpu.ram[0] = 0x1a1 # SET PUSH, A
        cpu.dispatch()

        self.assertTrue(cpu.ram[cpu.SP] == 0xdead, "Stack pushing b0rked")

    def test_peek_into_register(self):
        """ Pushed value in register to stack """
        cpu = CPU()
        cpu.ram[cpu.SP] = 0xbeef

        # PEEK   REG.A   SET
        # 011001 000000  0001
        cpu.ram[0] = 0x6401 # SET A, PEEK
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG.A] == 0xbeef, "Stack peeking b0rked")

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

        cpu.ram[0] = pack_instruction(OPCODE.SET, REG.PC, 0x25)
        cpu.dispatch()

        self.assertEqual(cpu.PC, 0x5, "PC Loading failed")

    def test_read_o(self):
        """ Reads O into register """
        cpu = CPU()
        cpu.O = 0xffff

        # O      REG.A  SET
        # 011101 000000 0001
        cpu.ram[0] = 0x7401
        cpu.dispatch()

        self.assertTrue(cpu.O == 0xffff, "O Loading failed")

    def test_next_word_register(self):
        """ [Next word + register]  into register """
        cpu = CPU()
        cpu.registers[REG.B] = 0x10
        cpu.ram[0x20] = 0xfeed

        # [next word + REG.B] REG.C     SET
        # 10001               000010    0001
        cpu.ram[0] = 0x4421
        cpu.ram[1] = 0x10
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG.C] == 0xfeed, "Register + offset failed")

    def test_next_word_register_both(self):
        """ [Next word + register] into [Next word + register] """
        cpu = CPU()
        cpu.registers[REG.B] = 0x10
        cpu.registers[REG.C] = 0x20
        cpu.ram[0x40] = 0xfeed

        # SET [0x0010 + B], [0x0020 + C]
        cpu.ram[0] = pack_instruction(op_code=0x1, oper1=0x11, oper2=0x12)
        cpu.ram[1] = 0x10
        cpu.ram[2] = 0x20
        cpu.dispatch()

        self.assertEqual(cpu.ram[0x20], 0xfeed, "Register + offset failed")
        self.assertEqual(cpu.PC, 0x3, "PC not set correctly")

    def test_ram_of_next_word(self):
        """ Reads from register to ram of next word into register"""
        cpu = CPU()
        cpu.ram[0x44] = 0x1212

        # [next word] REG.D  SET
        # 11110       000011 0001
        cpu.ram[0] = 0x7831
        cpu.ram[1] = 0x44
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG.X] == 0x1212, "Ram of next word error")

    def test_next_word_literal(self):
        """ Reads next word as a literal """
        cpu = CPU()

        # next word(literal) REG.A  SET
        # 11111              000000 0001
        cpu.ram[0] = pack_instruction(OPCODE.SET, REG.A, 0x1f)
        cpu.ram[1] = 0x1234

        cpu.dispatch()

        self.assertTrue(cpu.registers[REG.A] == 0x1234, "Next word as literal error")
if __name__ == '__main__':
    unittest.main()

