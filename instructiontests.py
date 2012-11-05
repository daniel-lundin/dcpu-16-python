import random
import unittest
from ctypes import c_int16

from cpu import CPU
from emulator import Emulator
from constants import REG, OPCODE
from utils import (pack_instruction,
        pack_special_instruction, unpack_instruction,
        unpack_special_instruction, Value)

class TestInstructions(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()
        self.emulator = Emulator(self.cpu)

    def test_add(self):
        """ Sets REG.A to REG.A + REG.B """
        self.cpu.registers[REG.A].value = 0x12
        self.cpu.registers[REG.B].value = 0x34

        # ADD A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.ADD,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x46, "Add failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_add_overflow(self):
        """ Sets REG.A to REG.A + REG.B, overflows """
        self.cpu.registers[REG.A].value = 0xffff
        self.cpu.registers[REG.B].value = 0x0001

        # ADD A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.ADD,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x0000, "Add failed")
        self.assertTrue(self.cpu.EX.value == 0xffff, "Ex flag not reset")

    def test_sub(self):
        """ Sets REG.A to REG.A - REG.B """
        self.cpu.registers[REG.A].value = 0xffff
        self.cpu.registers[REG.B].value = 0x0001

        # SUB A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SUB,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xfffe, "Sub failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_sub_underflow(self):
        """ Sets REG.A to REG.A - REG.B, underflows """
        self.cpu.registers[REG.A].value = 0x0001
        self.cpu.registers[REG.B].value = 0x0002

        # SUB A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SUB,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x0001, "Sub failed")
        self.assertTrue(self.cpu.EX.value == 0xffff, "Ex flag not set")

    def test_mul(self):
        """ Sets REG.A to REG.A * REG.B """
        self.cpu.registers[REG.A].value = 0x0002
        self.cpu.registers[REG.B].value = 0x0003

        # MUL A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.MUL,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x6, "Mul failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_mul_overflows(self):
        """ Sets REG.A to REG.A * REG.B, overflows """
        self.cpu.registers[REG.A].value = 0xffff
        self.cpu.registers[REG.B].value = 0x0002

        # MUL A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.MUL,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xfffe, "Mul failed")
        self.assertTrue(self.cpu.EX.value == 0x1, "Ex flag not set")

    def test_mli(self):
        """ Sets REG.A to REG.A * REG.B, treats A,B as signed """
        self.cpu.registers[REG.A].value = -5
        self.cpu.registers[REG.B].value = -4

        # MLI A, B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.MLI,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        signed_result = c_int16(self.cpu.registers[REG.A].value)
        self.assertEqual(signed_result.value, 20, "MLI failed")
        self.assertTrue(self.cpu.EX.value == 0x0, "Ex flag not reset")

    def test_div(self):
        """ Sets REG.A to REG.A / REG.B """
        self.cpu.registers[REG.A].value = 0x0009
        self.cpu.registers[REG.B].value = 0x0002

        # DIV A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.DIV,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x4, "Div failed")

    def test_dvi(self):
        """ Sets REG.A to REG.A / REG.B """
        self.cpu.registers[REG.A].value = -4
        self.cpu.registers[REG.B].value = -2

        # DVI A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.DVI,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 2, "Div failed")

    def test_mod(self):
        """ Sets REG.A to REG.A % REG.B """
        self.cpu.registers[REG.A].value = 0x0009
        self.cpu.registers[REG.B].value = 0x0002

        # MOD A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.MOD,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x1, "Mod failed")

    def test_mdi(self):
        """ Sets REG.A to REG.A % REG.B """
        self.cpu.registers[REG.A].value = -7
        self.cpu.registers[REG.B].value = 16

        # MDI A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.MDI,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        signed_result = c_int16(self.cpu.registers[REG.A].value)
        self.assertEqual(signed_result.value, -7, "MDI failed")

    def test_shl(self):
        """ Sets REG.A to REG.A << REG.B """
        self.cpu.registers[REG.A].value = 0x0008
        self.cpu.registers[REG.B].value = 0x0002

        # SHL A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SHL,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x20, "shl failed")

    def test_asr(self):
        """ Sets REG.A to REG.A << REG.B """
        self.cpu.registers[REG.A].value = -3
        self.cpu.registers[REG.B].value = 2

        # ASR A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.ASR,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        signed_result = c_int16(self.cpu.registers[REG.A].value)
        self.assertEqual(signed_result.value, -1, "ASR failed")

    def test_shr(self):
        """ Sets REG.A to REGREG.> REG.B """
        self.cpu.registers[REG.A].value = 0x0008
        self.cpu.registers[REG.B].value = 0x0002

        # SHR A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SHR,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0x2, "shr failed")

    def test_and(self):
        """ Sets REG.A to REG.A & REG.B """
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x000f

        # AND A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.AND,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xf, "and failed")

    def test_bor(self):
        """ Sets REG.A to REG.A | REG.B """
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x000f

        # BOR A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.BOR,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xff, "bor failed")

    def test_xor(self):
        """ Sets REG.A to REG.A ^ REG.B """
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x000f

        # XOR A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.XOR,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.registers[REG.A].value == 0xf0, "xor failed")

    def test_ife_equal(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ff

        # IFE A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFE,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertTrue(self.cpu.PC.value == 1, "PC not set right")

    def test_ife_notequal(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ef

        # IFE A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFE,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifc_equal(self):
        self.cpu.registers[REG.A].value = 0x0000
        self.cpu.registers[REG.B].value = 0x00ff

        # IFC A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFC,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "PC not set right")


    def test_ifn_false(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ff

        # IFN A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFN,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifn_true(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ef

        # IFN A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFN,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "Skip error")

    def test_ifg_false(self):
        self.cpu.registers[REG.A].value = 0x00fe
        self.cpu.registers[REG.B].value = 0x00ff

        # IFG A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFG,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifg_true(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ef

        # IFG A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFG,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "Skip error")

    def test_ifb_true(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x00ff

        # IFB A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFB,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "Skip error")

    def test_ifb_notequal(self):
        self.cpu.registers[REG.A].value = 0x00ff
        self.cpu.registers[REG.B].value = 0x0000

        # IFB A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFB,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "Skip error")

    def test_ifa_true(self):
        self.cpu.registers[REG.A].value = 3
        self.cpu.registers[REG.B].value = -4

        # IFN A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFA,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "IFA failed")

    def test_ifl(self):
        self.cpu.registers[REG.A].value = 3
        self.cpu.registers[REG.B].value = -4

        # IFL A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFA,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, False, "IFL failed")

    def test_ifu(self):
        self.cpu.registers[REG.A].value = 3
        self.cpu.registers[REG.B].value = -4

        # IFU A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.IFU,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.skip_instruction, True, "IFU failed")

    def test_adx(self):
        self.cpu.registers[REG.A].value = 0xfffe
        self.cpu.registers[REG.B].value = 0x0002
        self.cpu.EX.value = 0

        # ADX A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.ADX,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.EX.value, 1, "ADX failed")

    def test_sbx(self):
        self.cpu.registers[REG.A].value = 0x0003
        self.cpu.registers[REG.B].value = 0x0008
        self.cpu.EX.value = 0

        # SBX A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.SBX,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.EX.value, 1, "SBX failed")

    def test_sti(self):
        self.cpu.registers[REG.A].value = 0x0003
        self.cpu.registers[REG.B].value = 0x0008
        self.cpu.registers[REG.I].value = 0x000a
        self.cpu.registers[REG.J].value = 0x000b

        # STI A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.STI,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.registers[REG.A].value, 0xb, "STI fail")
        self.assertEqual(self.cpu.registers[REG.I].value, 0xb, "STI fail")
        self.assertEqual(self.cpu.registers[REG.J].value, 0xc, "STI fail")

    def test_std(self):
        self.cpu.registers[REG.A].value = 0x0003
        self.cpu.registers[REG.B].value = 0x0008
        self.cpu.registers[REG.I].value = 0x000a
        self.cpu.registers[REG.J].value = 0x000b

        # STD A,B
        self.cpu.ram[0].value = pack_instruction(op_code=OPCODE.STD,
                                                 a=Value.reg(REG.A),
                                                 b=Value.reg(REG.B))
        self.emulator.dispatch()

        self.assertEqual(self.cpu.registers[REG.A].value, 0xb, "STD fail")
        self.assertEqual(self.cpu.registers[REG.I].value, 0x9, "STD fail")
        self.assertEqual(self.cpu.registers[REG.J].value, 0xa, "STD fail")

    def test_jsr(self):
        self.cpu.registers[REG.I].value = 0x2323 # PC should be set to this

        # JSR I
        self.cpu.ram[0].value = pack_special_instruction(op_code=OPCODE.JSR,
                                                         a=REG.I)
        self.emulator.dispatch()

        self.assertEqual(self.cpu.PC.value, 0x2323, "PC not right")
        self.assertEqual(self.cpu.ram[self.cpu.SP.value].value, 0x1, "Stack not right")

    def test_pack_unpack(self):
        packed = pack_instruction(op_code=OPCODE.IFG,
                                  a=Value.reg(REG.A),
                                  b=Value.reg(REG.B))
        op_code, b, a = unpack_instruction(packed)

        self.assertEqual(op_code, OPCODE.IFG)
        self.assertEqual(b, Value.reg(REG.A))
        self.assertEqual(a, Value.reg(REG.B))

    def test_pack_unpack_special(self):
        packed = pack_special_instruction(op_code=OPCODE.JSR,
                                          a=Value.reg(REG.A))
        op_code, a = unpack_special_instruction(packed)

        self.assertEqual(op_code, OPCODE.JSR)
        self.assertEqual(a, Value.reg(REG.A))

if __name__ == '__main__':
    unittest.main()

