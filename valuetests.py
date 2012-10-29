import random
import unittest

from cpu import CPU
from emulator import Emulator
from constants import REG, OPCODE
from utils import pack_instruction, Value

class TestValues(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()
        self.emulator = Emulator(self.cpu)

    def test_set_reg_to_literal(self):
        """ Sets a register to a literal """
        # SET A, 0x10
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.A),
                                                 oper2=Value.literal(0x10))
        self.emulator.dispatch()
        self.assertTrue(self.cpu.registers[REG.A].value == 0x10, "Register value error")

    def test_set_addr_of_reg(self):
        """ Sets ram pointed by REG.I to value of REG.B """
        # Arrange
        self.cpu.registers[REG.I].value = 0xff
        self.cpu.registers[REG.B].value = 0x11

        # SET [I] B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.addr_reg(REG.I),
                                                 oper2=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.ram[0xff].value == 0x11, "Ram not updated correctly")

    def test_pop_into_reg(self):
        """ Pops from stack into register """
        self.cpu.ram[self.cpu.SP.value].value = 0xdead

        # SET A POP
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.A),
                                                 oper2=Value.push_pop())
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xdead, "Stack popping b0rked")

    def test_push_from_register(self):
        """ Pushed value in register to stack """
        self.cpu.registers[REG.A].value = 0xdead

        # SET PUSH, A
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.push_pop(),
                                                 oper2=Value.reg(REG.A))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.ram[self.cpu.SP.value].value == 0xdead, "Stack pushing b0rked")

    def test_peek_into_register(self):
        """ Pushed value in register to stack """
        self.cpu.ram[self.cpu.SP.value].value = 0xbeef

        # SET A, PEEK
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.A),
                                                 oper2=Value.peek())
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xbeef, "Stack peeking b0rked")

    def test_set_sp(self):
        """ Sets SP """

        # SET SP, 0x02
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.sp(),
                                                 oper2=Value.literal(0x02))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.SP.value == 0x2, "SP Loading failed")

    def test_set_pc(self):
        """ Sets PC """

        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.pc(),
                                                 oper2=Value.literal(0x5))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.PC.value, 0x5, "PC Loading failed")

    def test_read_ex(self):
        """ Reads O into register """
        self.cpu.EX.value = 0xffff

        # SET A, EX
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.A),
                                                 oper2=Value.reg(REG.EX))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.EX.value == 0xffff, "O Loading failed")

    def test_next_word_register(self):
        """ [Next word + register]  into register """
        self.cpu.registers[REG.B].value = 0x10
        self.cpu.ram[0x20].value = 0xfeed

        # SET C, [B + next word]
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.C),
                                                 oper2=Value.addr_reg_next_word(REG.B))
        self.cpu.ram[1].value = 0x10
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.C].value == 0xfeed, "Register + offset failed")

    def test_next_word_register_both(self):
        """ [Next word + register] into [Next word + register] """
        self.cpu.registers[REG.B].value = 0x10
        self.cpu.registers[REG.C].value = 0x20
        self.cpu.ram[0x40].value = 0xfeed

        # SET [0x0010 + B], [0x0020 + C]
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.addr_reg_next_word(REG.B),
                                                 oper2=Value.addr_reg_next_word(REG.C))
        self.cpu.ram[1].value = 0x10
        self.cpu.ram[2].value = 0x20
        self.emulator.dispatch()

        self.assertEqual(self.cpu.ram[0x20].value, 0xfeed, "Register + offset failed")
        self.assertEqual(self.cpu.PC.value, 0x3, "PC not set correctly")

    def test_ram_of_next_word(self):
        """ Reads from register to ram of next word into register"""
        self.cpu.ram[0x44].value = 0x1212

        # SET X [next word]
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.X),
                                                 oper2=Value.next_word_addr())
        self.cpu.ram[1].value = 0x44
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.X].value == 0x1212, "Ram of next word error")

    def test_next_word_literal(self):
        """ Reads next word as a literal """

        # SET A 0x1f
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SET,
                                                 oper1=Value.reg(REG.A),
                                                 oper2=Value.next_word_literal())
        self.cpu.ram[1].value = 0x1234

        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x1234, "Next word as literal error")

if __name__ == '__main__':
    unittest.main()
