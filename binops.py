import math
import random
import padding as pad
from Crypto.Cipher import AES

def visual_compare(string1, string2):
    if string1 == string2:
        print "Strings are equal"
            
        return True
    else:
        length = len(string1)
        if (len(string2) < length):
            length = len(string2)

        output = ""

        print string1

        for i in range(0, length):
            if string1[i] == string2[i]:
                output += " "
            else:
                output += "x"

        print output
        print string2

        return False

def bytewise(string1, string2, func):
    length = len(string1)
    if (len(string2) < length):
        length = len(string2)

    output = ""

    for i in range(0, length):
        output += chr(func(ord(string1[i]), ord(string2[i])))
    
    return output

def add(string1, string2):
    return bytewise(string1, string2, lambda x, y: (x + y) % 256)

def sub(string1, string2):
    return bytewise(string1, string2, lambda x, y: (x - y) % 256)

def xor(string1, string2):
    length = len(string1)
    if (len(string2) < length):
        length = len(string2)

    output = ""

    for i in range(0, length):
        output += chr( (ord(string1[i]) ^ ord(string2[i])) )
    
    return output

def repeating_xor(string, key):
    output = ""

    for i in range(0, len(string), len(key)):
        for j in range(0, len(key)):
            if i+j < len(string):
                output += chr(ord(string[i+j]) ^ ord(key[j]))

    return output

def ord_string( string ):
    output = ""

    for i in range( 0, len(string) ):
        output += str( ord( string[i] ) ) + " "

    return output

def random_char():
    return chr( random.randint( 0, 255 ) )

def random_string( length ):
    output = ""

    for i in range( 0, length ):
        output += random_char()

    return output

def random_encrypt( string ):
    startbytes = random.randint( 5, 10 )
    for i in range(0, startbytes ):
        string = random_char() + string

    endbytes = random.randint( 5, 10 )
    for i in range( 0, endbytes ):
        string += random_char()

    key = random_string( 16 )

    output = ""

    if ( random.randint( 0, 1 ) == 0 ):
        # ECB
        print "ECB"
        string = pad.PCKS7( string, 16 )
        output = ecb_encrypt( string, key )
    else:
        # CBC
        print "CBC"
        string = pad.PCKS7( string, 16 )
        output = cbc_encrypt( string, random_string( 16 ), key )

    return output    

def ecb_encrypt(string, key):
    cipher = AES.new( key, AES.MODE_ECB, "" )

    return cipher.encrypt( string )

def cbc_encrypt(string, iv, key):
    output = ""

    prev = iv

    cipher = AES.new( key, AES.MODE_ECB, "" )

    for i in range(0, len(string), len(key)):
        block = string[i:i+len(key)]

        block = xor(block, prev)
        block = cipher.encrypt( block )

        prev = block

        output += block

    return output 

def splice( string, index, toRemove, newString ):
    return string[:index] + newString + string[index+toRemove:]

def cbc_decrypt(string, iv, key):
    output = ""

    prev = iv

    next = ""

    cipher = AES.new(key, AES.MODE_ECB, "")

    for i in range(0, len(string), len(key)):
        block = string[i:i+len(key)]
            
        next = block

        block = cipher.decrypt( block )
        block = xor( block, prev )

        prev = next

        output += block

    return output 

def read_file(filename):
    with open(filename, "r") as f:
        text = f.read()

        f.close()

    return text

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

def every_nth_char(string, n, offset):
    output = ""

    for i in range(0, len(string)/n*n, n):
        if i+offset >= len(string):
            print i
            print offset
            print n
            print len(string)
        
        output += string[i + offset]

    return output
        
def count_repeated_blocks(string, length):
    count = 0

    for i in range(0, len(string) // length * length, length):
        for j in range(i + length, len(string) // length * length, length):
            if string[i:i+length] == string[j:j+length]:
                count += 1

    return count
        
def average_col( array, col ):
        result = 0;

        if ( len( array ) == 0 ):
                return 0

        for elem in array:
                result += elem[col]

        return result / len( array )

def little_endian_string( counter, length ):
    output = ""

    for i in range( 0, length / 2 ):
        output += chr( counter & 0xFF )
        counter >>= 8

    return output

#def block_oracle( string ):
