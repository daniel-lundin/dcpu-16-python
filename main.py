import struct
import sys
import optparse

from cpu import CPU
from emulator import Emulator

optparser = optparse.OptionParser()
optparser.add_option('-f', '--file', dest="file", help="Program file")
optparser.add_option('-l',
                     '--limit',
                     dest="limit",
                     help="Max number of instructions to execute")
(options, args) = optparser.parse_args(sys.argv)

if not options.file:
    optparser.print_help()
    exit(1)

cpu = CPU()
limit = None
if options.limit:
    limit = int(options.limit, 0)  # Guess base
f = open(options.file)
data = f.read()
words = struct.unpack('>%dH' % (len(data) / 2), data)
for word, idx in zip(words, range(len(words))):
    cpu.ram[idx] = word

emulator = Emulator(cpu)
emulator.execute(0, limit)
