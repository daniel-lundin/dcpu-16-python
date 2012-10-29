
def pack_instruction(op_code, oper1, oper2):
    return op_code | (oper1 << 4) | (oper2 << 10)

def unpack_instruction(instruction):
    """ Returns tuple (opcode, oper1, oper2) """
    return (instruction & 0xf, (instruction & 0x3f0) >> 4, (instruction & 0xfd00) >> 10)


class Value(object):
    """ Convience methods for creating values """

    @staticmethod
    def reg(register):
        return register

    @staticmethod
    def addr_reg(register):
        return register + 0x8

    @staticmethod
    def addr_reg_next_word(register):
        return register + 0x10

    @staticmethod
    def push_pop():
        return 0x18

    @staticmethod
    def peek():
        return 0x19

    @staticmethod
    def stack_next_word():
        return 0x1a

    @staticmethod
    def sp():
        return 0x1b

    @staticmethod
    def pc():
        return 0x1c

    @staticmethod
    def ex():
        return 0x1d

    @staticmethod
    def next_word_addr():
        return 0x1e

    @staticmethod
    def next_word_literal():
        return 0x1f

    @staticmethod
    def literal(val):
        return val + 0x20
