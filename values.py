from constants import REG

class Literal(object):
    def __init__(self, value):
        self.value = value


def value_lookup(cpu, val, as_a):
    # register value
    if 0x0 <= val <= 0x7:
        return cpu.registers[val]

    # RAM at address of register value
    if 0x8 <= val <= 0xf:
        return cpu.ram[cpu.registers[val - 0x8].value]

    # RAM at address of register value + next word
    if 0x10 <= val <= 0x17:
        value = cpu.ram[cpu.registers[val - 0x10].value +
                        cpu.ram[cpu.PC.value].value]
        cpu.PC.value += 1
        return value

    # Stack push/pop depending on if it's first or second value
    if val == 0x18:
        if as_a: #POP
            value = cpu.ram[cpu.SP.value]
            cpu.SP.value += 1
            return value
        else: #PUSH
            cpu.SP.value -= 1
            return cpu.ram[cpu.SP.value]

    if val == 0x19:
        return cpu.ram[cpu.SP.value]

    # Ram at address of stack value + next word
    if val == 0x1a:
        value =  cpu.ram[cpu.SP.value + cpu.ram[cpu.PC.value].value]
        cpu.PC.value += 1
        return value

    # SP
    if val == 0x1b:
        return cpu.SP

    # PC
    if val == 0x1c:
        return cpu.PC

    # EX
    if val == 0x1d:
        return cpu.PC

    # Ram at address of next word
    if val == 0x1e:
        value = cpu.ram[cpu.ram[cpu.PC.value].value]
        cpu.PC.value += 1
        return value

    # Next word as literal
    if val == 0x1f:
        val = cpu.ram[cpu.PC.value]
        cpu.PC.value += 1
        return val

    # Literal value
    if 0x20 <= val <= 0x3f:
        return Literal(val - 0x20)
