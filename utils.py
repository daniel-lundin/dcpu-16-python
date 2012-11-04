
def pack_instruction(op_code, a, b):
    return op_code | (a << 5) | (b << 10)

def pack_special_instruction(op_code, a):
    return (op_code << 5) | (a << 10)

def unpack_instruction(instruction):
    """ Returns tuple (opcode, b, a) """
    return (instruction & 0x1f, (instruction & 0x3e0) >> 5, (instruction & 0xfd00) >> 10)

def unpack_special_instruction(instruction):
    return ((instruction & 0x03e0) >> 5, (instruction & 0xfd00) >> 10)

# Hint for constructing instructions
#  aaaa aabb bbbo oooo
#a 1111 1100 0000 0000 0xfd00
#b 0000 0011 1110 0000 0x03e0
#9 0000 0000 0001 1111 0x1f

# Hint for constructing special instructions
#  aaaa aaoo ooo0 0000
#a 1111 1100 0000 0000 0xfd00
#b 0000 0011 1110 0000 0x03e0


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
