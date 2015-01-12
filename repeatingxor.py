import collections
import math

capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowers   = "abcdefghijklmnopqrstuvwxyz"

scoredstring = collections.namedtuple('ScoredString', ['str', 'score', 'char'])

# English letter frequency
letter_freq = [
    0.082, # A
    0.015, # B
    0.028, # C
    0.043, # D
    0.130, # E
    0.022, # F
    0.020, # G
    0.061, # H
    0.070, # I
    0.002, # J
    0.077, # K
    0.040, # L
    0.024, # M
    0.067, # N
    0.075, # O
    0.019, # P
    0.001, # Q
    0.060, # R
    0.063, # S
    0.091, # T
    0.028, # U
    0.010, # V
    0.024, # W
    0.002, # X
    0.020, # Y
    0.001 # Z
]

# Score most ASCII characters negatively
# Letters (and punctuation) are the positive exception
english_freq = [-1] * 256

# Lowercase letters
for i in range(0, len(lowers)):
    english_freq[ord(lowers[i])] = letter_freq[i]

# Capitals
pct_capitals = 0.05
for i in range(0, len(capitals)):
    english_freq[ord(capitals[i])] = letter_freq[i] * pct_capitals

# Space frequency
# 5.1 letters/word --> ~1 space per 6.1 characters
english_freq[ord(" ")] = 0.164

# Uncommon characters to ignore
english_freq[ord("\n")] = -10000
english_freq[ord("'")] = -10000
english_freq[ord(",")] = -10000
english_freq[ord("-")] = -10000
english_freq[ord(".")] = -10000

# Decrypt a file encrypted under repeating-key XOR
def repeating_key_XOR_crack( filename ):
    # Assume base64 encoding
    with open(filename, "r") as f:
        text = f.read()

    # Strip out whitespace leaving only the base64
    text = text.replace("\n", "")

    # GIT THE BITS
    text = base64_to_binary(text)

    # Parts of the file to sample, bigger is better but takes longer
    length_sample = text[0:400]
    key_sample = text[0:900]

    # Knowing the text was repeating-key-XORed, find
    # a key length that results in the lowest edit distance
    #
    # Do this by comparing edit distance of successive pairs of bytes
    lengths = rank_lengths(length_sample, 2, 20)

    lengths = sorted(lengths, key=lambda length: length[1])

    # Look at the best 4 possible key lengths
    for j in range(0, 4):
        key = ""
        key_length = lengths[j][0]
        
        # Divide the encrypted strings into blocks the same length as the key
        # Make new strings consisting of all the first characters of these blocks, all the second characters, ...
        # Each of these new strings has been XOR'ed against a single character (since the key is repeating)
        for i in range(0, key_length):
            string = every_nth_char(key_sample, key_length, i)
            unc = single_character_XOR_crack(string)

            key += unc.char

        # Display the decrypted message
        print "Key Length " + str(key_length) + ": " + key
        print "Result: " + repeating_xor(text[0:100], key)

# Attempt to decipher a string that was XOR'ed against a single repeating character
# Do this by trying every character and seeing which one spits out the most English-like letter frequency 
def single_character_XOR_crack(string):
    best = ""
    best_score = 0
    best_char = ""

    scores = []

    for test in range(0, 256):
        xorred = repeating_xor(string, chr(test))
    
        score = eval_english(xorred)

        scores.append( scoredstring( xorred, score, chr(test) ) )
        
    scores = sorted( scores, lambda a, b: sorter( b.score - a.score )  )

    return scores[0]

# Rate a string on how it's letter frequency compares to English
# The longer, the better
def eval_english(string):
    length = len(string)

    count = [0] * 256

    total = 0

    extras = 0
    
    # Count instances of each character in the string
    for c in string:
        count[ord(c)] += 1
    
    # Divide by string length to get frequency
    # Then divide frequency by expected frequency, and add that to the score (higher is better)
    #
    # Example: Letter K
    # Expected frequency 0.077
    # Frequency close to expected (0.071) scores high (0.071/0.077 = 0.92)
    # Frequency far from expected in either direction (0.01, 0.22) scores low (0.01/0.077 = 0.12, 1 / 0.22/.077 = 0.35)
    for i in range(0, len(count)):
        freq = float(count[i]) / length
        
        freq /= english_freq[i]
        if freq > 1:
            freq = 1 / freq

        total += freq

    return total

def sorter( val ):
    if ( val < 0 ):
        return -1
    elif ( val > 0 ):
        return 1
    else:
        return 0

# Find probably key lengths by comparing bit differences between blocks of encrypted characters
# This operation of encryption leaves artifacts in a predictable pattern
def rank_lengths(string, minlen, maxlen):
    result = []

    for length in range(minlen, maxlen):
        if len(string) < length*2:
            break

        normalized_dist = 0.0

        for i in range(0, len(string)-length*2, length):
            block1 = string[i:i+length]
            block2 = string[i+length:i+length*2]
            normalized_dist += edit_distance(block1, block2)/float(length)
        
        normalized_dist /= math.floor(len(string)/length)

        result.append((length, normalized_dist))

    return result

# return a string consisting of every nth character in a given string, with some offset
#
# For example, extracting every 4th character, with a starting offset of 1
#
# FRANKLIN DELANO ROOSEVELT
#  |   |   |   |   |   |   
#
# RLDNOV
 

def every_nth_char(string, n, offset):
	output = ""

	for i in range(0, len(string)/n*n, n):
	    output += string[i + offset]

	return output

# Apply the XOR operation to each character of a string, with a repeating key
#
# input string ULYSSES SIMPSON GRANT
# key MONK
# xor string   MONKMONKMONKMONKMONKM
#
# each pair of letters is XOR'ed together
def repeating_xor(string, key):
    output = ""

    for i in range(0, len(string), len(key)):
        for j in range(0, len(key)):
            if i+j < len(string):
                output += chr(ord(string[i+j]) ^ ord(key[j]))

    return output

# Calculate the number of bit flips required to change one string into another
def edit_distance(string1, string2):
    if len(string1) != len(string2):
        print "edit_distance: strings not equal length"
        return 0

    count = 0
    
    for i in range(0, len(string1)):
        val = ord(string1[i]) ^ ord(string2[i])

        for j in range(0, 8):
            if val & 0x1:
                count += 1
            val >>= 1
    
    return count

base64Char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def base64_to_binary(string):
    encoded = ""
    bits = 0
    numbits = 0

    for i in range(0, len(string)):
        try:
            index = base64Char.index(string[i])
        except ValueError:
            if string[i] != "=":
                print "Unknown character " + str(ord(string[i]))
            continue
        
        bits <<= 6

        bits += index
            
        numbits += 6

        if ( numbits >= 8 ): # We made a byte!
            # Copy out the eight highest bits 
            encoded += chr(bits >> (numbits - 8))

            # Isolate and retain the rest of the bits
            bits &= 2 ** (numbits-8) - 1
            numbits -= 8

    return encoded