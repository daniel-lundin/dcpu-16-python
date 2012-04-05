import random
import unittest

from cpu import CPU
from constants import *
from utils import pack_instruction

class TestInstructions(unittest.TestCase):

    def test_add(self):
        """ Sets REG_A to REG_A + REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x12
        cpu.registers[REG_B] = 0x34

        cpu.ram[0] = pack_instruction(op_code=0x2, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x46, "Add failed")
        self.assertTrue(cpu.O == 0x0, "Overflow flag not reset")

    def test_add_overflow(self):
        """ Sets REG_A to REG_A + REG_B, overflows """
        cpu = CPU()
        cpu.registers[REG_A] = 0xffff
        cpu.registers[REG_B] = 0x0001

        cpu.ram[0] = pack_instruction(op_code=0x2, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x0000, "Add failed")
        self.assertTrue(cpu.O == 0xffff, "Overflow flag not reset")

    def test_sub(self):
        """ Sets REG_A to REG_A - REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0xffff
        cpu.registers[REG_B] = 0x0001

        cpu.ram[0] = pack_instruction(op_code=0x3, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xfffe, "Sub failed")
        self.assertTrue(cpu.O == 0x0, "Overflow flag not reset")

    def test_sub_underflow(self):
        """ Sets REG_A to REG_A - REG_B, underflows """
        cpu = CPU()
        cpu.registers[REG_A] = 0x0001
        cpu.registers[REG_B] = 0x0002

        cpu.ram[0] = pack_instruction(op_code=0x3, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x0001, "Sub failed")
        self.assertTrue(cpu.O == 0xffff, "Overflow flag not set")

    def test_mul(self):
        """ Sets REG_A to REG_A * REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x0002
        cpu.registers[REG_B] = 0x0003

        cpu.ram[0] = pack_instruction(op_code=0x4, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x6, "Mul failed")
        self.assertTrue(cpu.O == 0x0, "Overflow flag not reset")

    def test_mul_overflows(self):
        """ Sets REG_A to REG_A * REG_B, overflows """
        cpu = CPU()
        cpu.registers[REG_A] = 0xffff
        cpu.registers[REG_B] = 0x0002

        cpu.ram[0] = pack_instruction(op_code=0x4, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xfffe, "Mul failed")
        self.assertTrue(cpu.O == 0x1, "Overflow flag not set")

    def test_div(self):
        """ Sets REG_A to REG_A / REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x0009
        cpu.registers[REG_B] = 0x0002

        cpu.ram[0] = pack_instruction(op_code=0x5, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x4, "Div failed")

    def test_mod(self):
        """ Sets REG_A to REG_A % REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x0009
        cpu.registers[REG_B] = 0x0002

        cpu.ram[0] = pack_instruction(op_code=0x6, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x1, "Mod failed")

    def test_shl(self):
        """ Sets REG_A to REG_A << REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x0008
        cpu.registers[REG_B] = 0x0002

        cpu.ram[0] = pack_instruction(op_code=0x7, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x20, "shl failed")

    def test_shr(self):
        """ Sets REG_A to REG_A >> REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x0008
        cpu.registers[REG_B] = 0x0002

        cpu.ram[0] = pack_instruction(op_code=0x8, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0x2, "shr failed")

    def test_and(self):
        """ Sets REG_A to REG_A & REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x000f

        cpu.ram[0] = pack_instruction(op_code=0x9, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xf, "and failed")

    def test_bor(self):
        """ Sets REG_A to REG_A | REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x000f

        cpu.ram[0] = pack_instruction(op_code=0xa, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xff, "bor failed")

    def test_xor(self):
        """ Sets REG_A to REG_A ^ REG_B """
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x000f

        cpu.ram[0] = pack_instruction(op_code=0xb, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.registers[REG_A] == 0xf0, "xor failed")

    def test_ife_equal(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ff

        cpu.ram[0] = pack_instruction(op_code=0xc, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 1, "PC not set right")

    def test_ife_notequal(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ef

        cpu.ram[0] = pack_instruction(op_code=0xc, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 2, "PC not set right")

    def test_ifn_false(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ff

        cpu.ram[0] = pack_instruction(op_code=0xd, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 2, "PC not set right")

    def test_ifn_true(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ef

        cpu.ram[0] = pack_instruction(op_code=0xd, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 1, "PC not set right")

    def test_ifg_false(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ff

        cpu.ram[0] = pack_instruction(op_code=0xe, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 2, "PC not set right")

    def test_ifg_true(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ef

        cpu.ram[0] = pack_instruction(op_code=0xe, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 1, "PC not set right")

    def test_ifb_true(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x00ff

        cpu.ram[0] = pack_instruction(op_code=0xf, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 1, "PC not set right")

    def test_ifb_notequal(self):
        cpu = CPU()
        cpu.registers[REG_A] = 0x00ff
        cpu.registers[REG_B] = 0x0000

        cpu.ram[0] = pack_instruction(op_code=0xf, oper1=0x0, oper2=0x1)
        cpu.dispatch()

        self.assertTrue(cpu.PC == 2, "PC not set right")

if __name__ == '__main__':
    unittest.main()


