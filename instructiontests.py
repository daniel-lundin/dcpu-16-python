import random
import unittest

from cpu import CPU
from emulator import Emulator
from constants import REG, OPCODE
from utils import pack_instruction

class TestInstructions(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()
        self.emulator = Emulator(self.cpu)

    def test_add(self):
        """ Sets REG.A to REG.A + REG.B """
        self.cpu.registers[REG.A].value = 0x12
        self.cpu.registers[REG.B].value = 0x34

        self.cpu.ram[0].value = pack_instruction(op_code=0x2, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x46, "Add failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_add_overflow(self):
        """ Sets REG.A to REG.A + REG.B, overflows """
        self.cpu.registers[REG.A].value = 0xffff
        self.cpu.registers[REG.B].value = 0x0001

        self.cpu.ram[0].value = pack_instruction(op_code=0x2, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x0000, "Add failed")
        self.assertTrue(self.cpu.EX.value == 0xffff, "Ex flag not reset")

    def test_sub(self):
        """ Sets REG.A to REG.A - REG.B """
        self.cpu.registers[REG.A].value = 0xffff
        self.cpu.registers[REG.B].value = 0x0001

        self.cpu.ram[0].value = pack_instruction(op_code=0x3, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xfffe, "Sub failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_sub_underflow(self):
        """ Sets REG.A to REG.A - REG.B, underflows """
        self.cpu.registers[REG.A].value = 0x0001
        self.cpu.registers[REG.B].value = 0x0002

        self.cpu.ram[0].value = pack_instruction(op_code=0x3, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x0001, "Sub failed")
        self.assertTrue(self.cpu.EX.value == 0xffff, "Ex flag not set")

    def test_mul(self):
        """ Sets REG.A to REG.A * REG.B """
        self.cpu.registers[REG.A].value = 0x0002
        self.cpu.registers[REG.B].value = 0x0003

        self.cpu.ram[0].value = pack_instruction(op_code=0x4, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x6, "Mul failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_mul_overflows(self):
        """ Sets REG.A to REG.A * REG.B, overflows """
        self.cpu.registers[REG.A].value = 0xffff
        self.cpu.registers[REG.B].value = 0x0002

        self.cpu.ram[0].value = pack_instruction(op_code=0x4, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xfffe, "Mul failed")
        self.assertTrue(self.cpu.EX.value == 0x1, "Ex flag not set")

    def test_div(self):
        """ Sets REG.A to REG.A / REG.B """
        self.cpu.registers[REG.A].value = 0x0009
        self.cpu.registers[REG.B].value = 0x0002

        self.cpu.ram[0].value = pack_instruction(op_code=0x5, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x4, "Div failed")

    def test_mod(self):
        """ Sets REG.A to REG.A % REG.B """
        self.cpu.registers[REG.A].value = 0x0009
        self.cpu.registers[REG.B].value = 0x0002

        self.cpu.ram[0].value = pack_instruction(op_code=0x6, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x1, "Mod failed")

    def test_shl(self):
        """ Sets REG.A to REG.A << REG.B """
        self.cpu.registers[REG.A].value = 0x0008
        self.cpu.registers[REG.B].value = 0x0002

        self.cpu.ram[0].value = pack_instruction(op_code=0x7, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x20, "shl failed")

    def test_shr(self):
        """ Sets REG.A to REGREG.> REG.B """
        self.cpu.registers[REG.A].value = 0x0008
        self.cpu.registers[REG.B].value = 0x0002

        self.cpu.ram[0].value = pack_instruction(op_code=0x8, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x2, "shr failed")

    def test_and(self):
        """ Sets REG.A to REG.A & REG.B """
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x000f

        self.cpu.ram[0].value = pack_instruction(op_code=0x9, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xf, "and failed")

    def test_bor(self):
        """ Sets REG.A to REG.A | REG.B """
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x000f

        self.cpu.ram[0].value = pack_instruction(op_code=0xa, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xff, "bor failed")

    def test_xor(self):
        """ Sets REG.A to REG.A ^ REG.B """
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x000f

        # XOR REG_A, REG_B
        self.cpu.ram[0].value = pack_instruction(op_code=0xb, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xf0, "xor failed")

    def test_ife_equal(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ff

        self.cpu.ram[0].value = pack_instruction(op_code=0xc, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.PC.value == 1, "PC not set right")

    def test_ife_notequal(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ef

        self.cpu.ram[0].value = pack_instruction(op_code=0xc, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifn_false(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ff

        self.cpu.ram[0].value = pack_instruction(op_code=0xd, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifn_true(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ef

        self.cpu.ram[0].value = pack_instruction(op_code=0xd, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "Skip error")

    def test_ifg_false(self):
        self.cpu.registers[REG.A].value = 0x00fe
        self.cpu.registers[REG.B].value = 0x00ff

        self.cpu.ram[0].value = pack_instruction(op_code=0xe, oper1=0x1, oper2=0x0)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifg_true(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ef

        self.cpu.ram[0].value = pack_instruction(op_code=0xe, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertTrue(self.cpu.PC.value == 1, "PC not set right")

    def test_ifb_true(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ff

        self.cpu.ram[0].value = pack_instruction(op_code=0xf, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "Skip error")

    def test_ifb_notequal(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x0000

        self.cpu.ram[0].value = pack_instruction(op_code=0xf, oper1=0x0, oper2=0x1)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_jsr(self):
        self.cpu.registers[REG.I].value = 0x2323 # PC should be set to this

        # JSR D
        self.cpu.ram[0].value = (0b1 << 4) | (REG.I << 10)
        self.emulator.dispatch()
        
        self.assertEqual(self.cpu.PC.value, 0x2323, "PC not right")
        self.assertEqual(self.cpu.ram[self.cpu.SP.value].value, 0x1, "Stack not right")

if __name__ == '__main__':
    unittest.main()

