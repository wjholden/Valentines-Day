py_multiplier = 0x5DEECE66D
py_mask = (1 << 48) - 1
py_addend = 0xB

def initialScramble(seed):
	return (seed ^ py_multiplier) & py_mask

def nextSeed(seed):
    return (seed * py_multiplier + py_addend) & py_mask

for x in range(9):
    i = 10 ** x
    seed = initialScramble(10 ** x)
    for y in range(3):
        seed = nextSeed(seed)
        value = seed >> 16
        print(i,bin(value),hex(value),value)

# We have reconstructed the random numbers returned by Random.nextInt().
# Now let's see if we can coerce a specific message from successive 
# java.util.Random invocations.

# This is completely derivative from the legendary
# https://yurichev.com/writings/SAT_SMT_by_example.pdf

from z3 import *
s = Solver()

multiplier = BitVec('multiplier', 64)
mask = BitVec('mask', 64)
addend = BitVec('addend', 64)
s.add(multiplier == 0x5DEECE66D, mask == (1 << 48) - 1, addend == 0xB)

seed = BitVec('seed', 64)
state0 = BitVec('state0', 64)
state1 = BitVec('state1', 64)
state2 = BitVec('state2', 64)
state3 = BitVec('state3', 64)
state4 = BitVec('state4', 64)
state5 = BitVec('state5', 64)
state6 = BitVec('state6', 64)
state7 = BitVec('state7', 64)

s.add(state0 == (seed ^ multiplier) & mask)
s.add(state1 == (state0 * multiplier + addend) & mask)
s.add(state2 == (state1 * multiplier + addend) & mask)
s.add(state3 == (state2 * multiplier + addend) & mask)
s.add(state4 == (state3 * multiplier + addend) & mask)
s.add(state5 == (state4 * multiplier + addend) & mask)
s.add(state6 == (state5 * multiplier + addend) & mask)
s.add(state7 == (state6 * multiplier + addend) & mask)

ch1 = BitVec('ch1', 64)
ch2 = BitVec('ch2', 64)
ch3 = BitVec('ch3', 64)
ch4 = BitVec('ch4', 64)
ch5 = BitVec('ch5', 64)
ch6 = BitVec('ch6', 64)
ch7 = BitVec('ch7', 64)

s.add(ch1 == ((state1 >> 16) % 128) & (0xff - 0x20))
s.add(ch2 == ((state2 >> 16) % 128) & (0xff - 0x20))
s.add(ch3 == ((state3 >> 16) % 128) & (0xff - 0x20))
s.add(ch4 == ((state4 >> 16) % 128) & (0xff - 0x20))
s.add(ch5 == ((state5 >> 16) % 128) & (0xff - 0x20))
s.add(ch6 == ((state6 >> 16) % 128) & (0xff - 0x20))
s.add(ch7 == ((state7 >> 16) % 128) & (0xff - 0x20))

# This is where all the fun happens. Put some uppercase
# letters into these fields. If it is possible for the PRNG
# to spell this string then you can take the seed from the model.
s.add(ch1 == ord('A'))
s.add(ch2 == ord('L'))
s.add(ch3 == ord('E'))
s.add(ch4 == ord('X'))
# s.add(ch5 == ord('S'))
#s.add(ch6 == ord('O'))
#s.add(ch7 == ord('U'))

print(s.check())
print(s.model())

reproduce = [initialScramble(s.model()[seed].as_long())]
for j in range(4):
    reproduce.append(nextSeed(reproduce[-1]))
print([hex(i >> 16) for i in reproduce[1:]])
print([(((i >> 16) % 128) & (0xff - 0x20)) for i in reproduce[1:]])
print([chr(((i >> 16) % 128) & (0xff - 0x20)) for i in reproduce[1:]])