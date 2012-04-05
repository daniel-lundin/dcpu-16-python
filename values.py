class RegisterValue(object):

    def __init__(self, register):
        self.register = register

    def set(self, cpu, val):
        cpu.register[self.register] = val 

    def get(self, cpu, val):
        return cpu.register[self.register]

class RegisterRamValue(object):

    def __init__(self, register):
        self.register = register

    def set(self, cpu, val):
        cpu.ram[cpu.register[self.register]] = val 

    def get(self, cpu, val):
        return cpu.ram[cpu.register[self.register]]
