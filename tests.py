import transcoding as trans
import binops
import frequency as freq
from Crypto.Cipher import AES

def part1():
    wordhex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    word64 = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    print "===Hex to Base-64==="
    print "hex: " + wordhex

    binary = trans.hex_to_binary(wordhex)
    print "hex to binary: " + binary
    print "binary to base64: " + trans.binary_to_base64(binary)


    print "\n\n===Base-64 to Hex==="
    print "base64: " + word64

    binary = trans.base64_to_binary(word64)
    print "base64 to bin: " + binary
    print "binary to hex: " + trans.binary_to_hex(binary)

def part2():
    print "\n\n===XOR==="
    hex1 = "1c0111001f010100061a024b53535009181c"
    hex2 = "686974207468652062756c6c277320657965"

    result = binops.xor(trans.hex_to_binary(hex1), trans.hex_to_binary(hex2))
    print trans.binary_to_hex(result)

def part3():
    print "\n\n===Single-character XOR==="
    encoded = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    binenc = trans.hex_to_binary(encoded)
    print freq.xor_uncipher(binenc)

def part4():
    print "\n\n===Detecting Single-character XOR==="
    f = open("part4_strings", "r")

    done = False
    lineno = 1

    while not done:
        line = f.readline().strip()

        if len(line) == 0:
            done = True
        else:
            unciphered = freq.xor_uncipher(trans.hex_to_binary(line))

            if unciphered.score > 10:
                print str(lineno) + " " + unciphered.str + " " + str(unciphered.score) + " " + unciphered.char

        lineno += 1

def part5():
    print "\n\n===Repeating-key XOR cipher==="
    string = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    print string
    result = trans.binary_to_hex(binops.repeating_xor(string, "ICE"))
    expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

    binops.visual_compare(result, expected)

def part6():
    print "\n\n===Breaking repeating-key XOR==="
    with open("part6_text", "r") as f:
        text = f.read()

    # Strip out whitespace leaving only the base64
    text = text.replace("\n", "")

    # GIT THE BITS
    text = trans.base64_to_binary(text)

    # Parts of the file, bigger is better but takes longer
    length_sample = text[0:400]
    key_sample = text[0:900]

    # Knowing the text was repeating-key-XORed, find
    # a key length that results in the lowest edit distance
    #
    # Do this by comparing edit distance of successive pairs of bytes
    lengths = binops.rank_lengths(length_sample, 2, 40)

    lengths = sorted(lengths, key=lambda length: length[1])

    for j in range(0, 4):
        key = ""
        key_length = lengths[j][0]
        
        for i in range(0, key_length):
            string = binops.every_nth_char(key_sample, key_length, i)
            unc = freq.xor_uncipher(string)

            key += unc.char

        print "Key Length " + str(key_length) + ": " + key
        print "Result: " + binops.repeating_xor(text[0:100], key)
     
def part7():
    print "\n\n===AES Decryption==="
    with open("part7_text", "r") as f:
        text = f.read()

    text = text.replace("\n", "")

    text = trans.base64_to_binary(text)

    # initialization vector (3rd arg) is ignored for ECB
    cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB, "")

    print cipher.decrypt(text)
    
def part8():
    print "\n\n===Detecting AES-ECB==="
    f = open("part8_lines", "r")

    lineno = 1
    done = False

    while not done:
        line = f.readline().strip()

        if len(line) == 0:
            done = True
        else:
            line = trans.hex_to_binary(line)

            repeated_blocks = binops.count_repeated_blocks(line, 2)

            if repeated_blocks > 0:
                print str(lineno) + " " + str(repeated_blocks)

            lineno += 1
        
part1()
part2()
part3()
part4()
part5()
part6()
part7()
part8()
