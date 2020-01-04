from z3 import *

def find_message_seed(msg, start):
    # Instantiate a new Z3 solver.
    s = Solver()

    # Java's PRNG uses the following three constants.
    multiplier = BitVec('multiplier', 64)
    mask = BitVec('mask', 64)
    addend = BitVec('addend', 64)
    s.add(multiplier == 0x5DEECE66D, mask == (1 << 48) - 1, addend == 0xB)

    # The seed is the answer we are looking for.
    # To word backwards from our intended message to the seed, the PRNG
    # will have to cycle through one or more states.
    # I kind of doubt we will ever find a lucky enough streak of PRNG
    # results to get past eight states.
    seed = BitVec('seed', 64)
    states = [BitVec("state{n}".format(n = i), 64) for i in range(0,7)]

    # Again, we don't know the seed, but we do not know the seed will be used
    # to generate the initial state of the PRNG. Also, yes the
    # multiplier gets "anded" to the seed, not multiplied.
    # http://hg.openjdk.java.net/jdk10/jdk10/jdk/file/777356696811/src/java.base/share/classes/java/util/Random.java#l145
    s.add(states[0] == (seed ^ multiplier) & mask)

    # Specify state transitions. This reproduces the behavior of
    # http://hg.openjdk.java.net/jdk10/jdk10/jdk/file/777356696811/src/java.base/share/classes/java/util/Random.java#l203
    # Note that the magic value "addend" is added here but was
    # not used to get to state[0] above.
    for j in range(1,7):
        s.add(states[j] == (states[j - 1] * multiplier + addend) & mask)
    
    # Z3 also needs to know that we are trying to relate the PRNG
    # states to letters. For this, we will use up to seven characters.
    # Note that state 0 does not correspond to a character. State 0 is
    # the initalized state that can never be directly used to generate
    # a returnable value from the PRNG.
    characters = [BitVec("ch{n}".format(n = i), 64) for i in range(1,7)]   

    # Ok, we've got our PRNG states and characters. Now we need to marry
    # them somehow. In this program, the relation between a PRNG state
    # and a character is that we:
    # 1) Shift the seed by 16 bits just like java.util.Random.next(32),
    # 2) Extract only the last seven bits from this value using a mask,
    # 3) Always set the fifth bit (0x20) to make the letter uppercase.
    #
    # This program can handle spaces.
    # Leaving the fifth bit free will allow you to work with more 
    # characters, but you might not be able to find solutions for your input.
    #
    # I tried making this an "or" statement so that the solver could
    # branch with the fifth bit set or unset. Bad idea.
    for k in range(0,6):
        s.add(characters[k] == ((states[k + 1] >> 16) & 0x7f) | 0x20)
    
    # Now we can constrain the value for these characters.
    # We walk from left to right, adding constraints letters to our
    # string until the solver determines no such sequence is possible.    
    longest_seed = -1
    i = 0
    # You don't have to constrain i to just 3. In my experience, though,
    # you won't find many outputs that produce more than 3 characters,
    # while you can fairly reliably find three-character sequences.
    # The program completes much faster with this constraint.
    while i < 3 and start + i < len(msg):
        s.add(characters[i] == ord(msg[start + i]))
        if s.check() == sat:
            i = i + 1
            longest_seed = s.model()[seed].as_long()
            #print(s)
        else:
            break

    # Return the value of the longest seed as a long with the
    # number of characters constructed.
    return (longest_seed, i)

def find_message_seeds(msg):
    position = 0
    result = []
    while position < len(msg):
        (seed, msg_length) = find_message_seed(msg, position)
        result.append((seed, msg_length))
        position += msg_length
    return result

m = find_message_seeds("happy valentines day mayflor love")
for (k,v) in m:
    print(k,v)

# Same output, but easier to paste for further analysis.
print([m[i][0] for i in range(len(m))])
