
def pack_instruction(op_code, oper1, oper2):
    return op_code | (oper1 << 4) | (oper2 << 10)

def unpack_instruction(instruction):
    """ Returns tuple (opcode, oper1, oper2) """
    return (instruction & 0xf, (instruction & 0x3f0) >> 4, (instruction & 0xfd00) >> 10)
