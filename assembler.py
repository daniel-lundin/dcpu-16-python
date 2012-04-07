#!/usr/bin/python
import re
import sys
import struct

basic_pattern = re.compile('(:\w+){0,1}\s*(\w{3})\s(.+?), (\S+)')
nonbasic_pattern = re.compile('(:\w+){0,1}\s*(\w{3})\s(\S+)')
register_pattern = re.compile('(A|B|C|X|Y|Z|I|J)')
addr_of_register_pattern = re.compile('\[(A|B|C|X|Y|Z|I|J)\]')
next_word_add_register_pattern = re.compile('\[(\S+)\+(A|B|C|X|Y|Z|I|J)\]')
addr_of_next_word_pattern = re.compile('\[(\S+)\]')
label_pattern = re.compile('([a-z]+)')


op_map = { "SET": 0x1, "ADD": 0x2, "SUB": 0x3, "MUL": 0x4, "DIV": 0x5, "MOD": 0x6, "SHL": 0x7, "SHR": 0x8, "AND": 0x9, "BOR": 0xa, "XOR": 0xb, "IFE": 0xc, "IFN": 0xd, "IFG": 0xe, "IFB": 0xf }
reg_map = { 'A': 0x0, 'B': 0x1, 'C': 0x2, 'X': 0x3, 'Y': 0x4, 'Z': 0x5, 'I': 0x6, 'J': 0x7 }

labels = {}

def encode_value(value):
    match = re.match(register_pattern, value)
    if match:
        return (reg_map[match.groups()[0]], None)

    match = re.match(addr_of_register_pattern, value) 
    if match:
        return (0x08 + reg_map[match.groups()[0]], None)

    match = re.match(next_word_add_register_pattern, value) 
    if match:
        literal, register = match.groups()
        return (0x10 + reg_map[register], int(literal, 0))

    match = re.match(addr_of_next_word_pattern, value)
    if match:
        return (0x1e, int(match.groups()[0], 0))

    if value == 'POP':
        return (0x18, None)
    if value == 'PEEK':
        return (0x19, None)
    if value == 'PUSH':
        return (0x1a, None)
    if value == 'SP':
        return (0x1b, None)
    if value == 'PC':
        return (0x1c, None)
    if value == 'O':
        return (0x1d, None)

    match = re.match(label_pattern, value)
    if match:
        return (0x1f, match.groups()[0])

    literal = int(value, 0)
    if literal <= 0x1f:
        return (literal + 0x20, None)
    return (0x1f, literal)

def encode_basic(op, a, b):
    if not op in op_map:
        raise Exception('Unrecognized instruction')
    opcode = op_map[op]
    value1, next_word1 = encode_value(a)
    value2, next_word2 = encode_value(b)
    instruction = [opcode + (value1 << 4) + (value2 << 10)]
    if next_word1:
        instruction.append(next_word1)
    if next_word2:
        instruction.append(next_word2)
    return instruction

def encode_non_basic(op, a):
    if op != "JSR":
        raise Exception('Unrecognized instruction')

    value, next_word = encode_value(a)
    instruction = [(0x1 << 4) + (value << 10)]
    if next_word:
        instruction.append(next_word)
    return instruction

def assemble(prog):
    compiled_code = []
    PC = 0
    lines = prog.split("\n")
    for line, lineno in zip(lines, range(1, len(lines)+1)):
        stripped = line.strip()

        basic_match = re.match(basic_pattern, stripped)
        non_basic_match = re.match(nonbasic_pattern, stripped)
        try:
            if basic_match != None:
                label, op, a, b = basic_match.groups()
                if label != None:
                    labels[label[1:]] = PC
                instruction = encode_basic(op, a, b)
            elif non_basic_match != None:
                label, op, a = non_basic_match.groups()
                if label != None:
                    labels[label[1:]] = PC
                instruction = encode_non_basic(op, a)
            else:
                continue
        except Exception, e:
            print 'Error at line %d: %s' % (lineno, str(e))
            exit(1)
        PC += len(instruction)
        compiled_code += instruction

    # Evaluate labels
    for idx in range(len(compiled_code)):
        if compiled_code[idx].__class__ == str:
            compiled_code[idx] = labels[compiled_code[idx]]
    return struct.pack(">%dH" % len(compiled_code), *compiled_code)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: ./assembler.py file binary"
        exit(1)
    fi = open(sys.argv[1], 'r')
    fo = open(sys.argv[2], 'w')
    fo.write(assemble(fi.read()))
    fi.close()
    fo.close()
