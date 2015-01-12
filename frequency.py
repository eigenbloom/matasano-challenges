import collections

import transcoding as trans
import binops

capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowers   = "abcdefghijklmnopqrstuvwxyz"

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

def eval_english(string):
    length = len(string)

    count = [0] * 256

    total = 0

    extras = 0
    
    for c in string:
        count[ord(c)] += 1
                
    for i in range(0, len(count)):
        freq = float(count[i]) / length
        
        freq /= english_freq[i]
        if freq > 1:
            freq = 1 / freq

        total += freq

    return total

scoredstring = collections.namedtuple('ScoredString', ['str', 'score', 'char'])

def sorter( val ):
    if ( val < 0 ):
        return -1
    elif ( val > 0 ):
        return 1
    else:
        return 0

def xor_uncipher(string):
    best = ""
    best_score = 0
    best_char = ""

    scores = []

    for test in range(0, 256):
        xorred = binops.repeating_xor(string, chr(test))
    
        score = eval_english(xorred)

        scores.append( scoredstring( xorred, score, chr(test) ) )
        
    scores = sorted( scores, lambda a, b: sorter( b.score - a.score )  )

    return scores[0]

