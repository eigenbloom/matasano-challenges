import math

base64Char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
hexChar = "0123456789abcdef"

def binary_to_base64(string):
    bitPosition = 0
    encoded = ""

    while ( bitPosition < len(string) * 8 ): # Grab 6 bits

        # Get the 8-bit character our 6 bits start in
        index = int(math.floor( bitPosition / 8 ))
        val = ord(string[index])
    
        val <<= 8

        # Grab the next character if we're not at the end, and combine it with the first
        if index < len(string) - 1:
            val += ord(string[index+1])

        # Two characters = 16 bits. The 6 bits we want are inside, so get them out
        val >>= 16-((bitPosition % 8) + 6)
        val &= 0x3F

        encoded += base64Char[val]

        bitPosition += 6

    leftovers = len(string) % 3

    if leftovers == 1:
        encoded += "=="

    if leftovers == 2:
        encoded += "="

    return encoded

def hex_to_binary(string):
    encoded = ""

    # Combine pairs of hex characters into single bytes
    for i in range( 0, len(string), 2 ):
        val = int(string[i],16) << 4
        if i < len(string)-1:
            val += int(string[i+1],16)

        encoded += chr(val)

    return encoded

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

def binary_to_hex(string):
    encoded = ""

    for i in range(0, len(string)):
        val = ord(string[i])

        encoded += hexChar[val >> 4] # Top 4 bits
        encoded += hexChar[val & 0xF] # Bottom 4 bits

    return encoded
