import binops as ops
import transcoding as trans
import padding as pad
import random
import stringops as sops
from Crypto.Cipher import AES

def oracle( func ):	
	string = ""

	# Solve for ECB vs CBC by inserting a repeating message, if we find two blocks the same
	# conclude that ECB is being used
	for i in range( 0, 4 ):
		string += "yellow submarine"

	enc1 = func( string )

	for i in range( 0, len(enc1) - 32, 16 ):
		if ( enc1[i:i+16] == enc1[i+16:i+32] ):
			return True

	return False

willy_key = ops.random_string(16)

willy_string = ops.read_file( "willy_string.txt" )
willy_string = willy_string.replace( "\n", "" )
willy_string = trans.base64_to_binary( willy_string )

willy_cipher = AES.new( willy_key, AES.MODE_ECB, "" )

willy_garbage_length = 0

def willy_encrypt( string ):
	# attacker string || target string

	return willy_cipher.encrypt( pad.PCKS7_pad( string + willy_string, 16 ) )

def willy_encrypt_2( string ):
	# random garbage || attacker string || target string

	global willy_garbage_length

	willy_garbage_length = random.randint( 0, 32 )

	in_string = ops.random_string( willy_garbage_length ) + string + willy_string

#	print in_string

	return willy_cipher.encrypt( pad.PCKS7_pad( in_string, 16 ) )

def willy_breaker():
	string = ""

	print "is ECB: " + str(oracle( willy_encrypt ))

	# find key length
	key_length = 0

	length_found = False	

	for i in range(1, 8):
		string += "AAAA"

	for i in range(8, 33):
		string += "AAAA"

		encrypted = willy_encrypt( string )

		for j in range( 0, len( encrypted ) - i*2 ):
			if ( encrypted[j:j+i] == encrypted[j+i:j+i*2] ): 
				key_length = i

				length_found = True
				break			

		if ( length_found ):
			break					

	if ( not length_found ):
		print "Unknown key length"
		return

	print "Key Length " + str(key_length)

	ecb_breaker( willy_encrypt, key_length )

def ecb_breaker( enc_func, key_length):

	# figure out the length of the encrypted message
	blank = enc_func( "" )

	# meaningless bytes inserted to push bytes into the right blocks
	# (we want to have exactly one unknown byte at the end of the block we're solving) 
	offset_word = ""

	# Block part will offset the characters of the unknown message
	# such that there is a single unknown character at the end of a
	# block, and the rest is the letter A
	for i in range( 0, key_length - 1 ):
		offset_word += "A"

	# the last blocklength-1 solved bytes of the message
	msg_tail = offset_word

	# block index we're solving
	current_block = 0

	msg = ""

	# Solve each character in order
	for j in range( 0, len(blank) ):
		test = enc_func( offset_word )
		test = test[current_block*key_length:(current_block+1)*key_length]

		found = False

		for i in range( 0, 256 ):
			block = msg_tail + chr(i)
			
			encrypted = enc_func( block )

			if ( encrypted[0:key_length] == test ):
				msg += chr(i)

				msg_tail = msg_tail[1:] + chr(i)

				# If we've solved a block
				if ( len( offset_word ) == 0 ):

					# Move on to the next one
					current_block += 1

					# Reset offset_word
					for k in range( 0, key_length - 1 ):
						offset_word += "A" 
				else:
					# Reduce the length of offset_word by 1
					offset_word = offset_word[1:]

				found = True

				break

		if ( found == False and len(msg) < len(blank) ):
			print "Error: no match"
			break

	print msg

def willy_2_no_garbage( string, key_length ):
	
	# aligner is two blocks that match
	# the junk blocks are two that don't match
	#
	# the junk blocks are for preventing errors where the last garbage character 
	# or the first text character is the same as an aligner character (very rare)
	aligner = ""
	leading_junk_block = ""
	trailing_junk_block = ""

	for i in range( 0, key_length ):
		leading_junk_block += "Z"
		aligner += "BB"
		trailing_junk_block += "Y"

	aligned = False

	encrypted = ""

	while ( not aligned ):
		encrypted = willy_encrypt_2( leading_junk_block + aligner + trailing_junk_block + string )

		for i in range( 0, len( encrypted ) - key_length * 2, key_length ):
			if ( encrypted[i:i+key_length] == encrypted[i+key_length:i+key_length*2] ): 
				aligned = True

				# return only the encrypted message (no aligner or junk)
				encrypted = encrypted[i+key_length*2+key_length:]
				break

	return encrypted

def willy_breaker_2():
	string = ""

	print "is ECB: " + str(oracle( willy_encrypt_2 ))

	# find key length
	key_length = 0

	length_found = False	

	for i in range(1, 8):
		string += "AAAA"

	for i in range(8, 33):
		string += "AAAA"

		encrypted = willy_encrypt_2( string )

		for j in range( 0, len( encrypted ) - i*2 ):
			if ( encrypted[j:j+i] == encrypted[j+i:j+i*2] ): 
				key_length = i

				length_found = True
				break			

		if ( length_found ):
			break					

	if ( not length_found ):
		print "Unknown key length"
		return

	print "Key Length " + str(key_length)

	ecb_breaker( lambda string: willy_2_no_garbage( string, key_length ), key_length )

jerry_key_length = 16
jerry_key = ops.random_string( jerry_key_length )
jerry_iv = ops.random_string( jerry_key_length )
jerry_header = "comment1=cooking%20MCs;userdata="
jerry_footer = ";comment2=%20like%20a%20pound%20of%20bacon"

def jerry_encrypt( string ):
	string = string.replace( ";", "" )
	string = string.replace( "=", "" )

	string = jerry_header + string + jerry_footer

	string = pad.PCKS7_pad( string, jerry_key_length )

	return ops.cbc_encrypt( string, jerry_iv, jerry_key )

def jerry_decrypt( encrypted ):
	string = ops.cbc_decrypt( encrypted, jerry_iv, jerry_key )

	print string

	items = string.split( ";" )

	for i in items:
		if ( i == "admin=true" ):
			return True 

	return False

wendy_key_length = 16
wendy_key = ops.random_string( wendy_key_length )
wendy_string = ""

def wendy_encrypt( string ):
	iv = ops.random_string( wendy_key_length )

	string = pad.PCKS7_pad( string, wendy_key_length )
	encrypted = ops.cbc_encrypt( string, iv, wendy_key )
	return ( encrypted, iv )

def wendy_check_padding( encrypted, iv ):
	string = ops.cbc_decrypt( encrypted, iv, wendy_key )

	global wendy_string

	wendy_string = string

	return pad.PCKS7_checkpad( string, wendy_key_length )

def wendy_breaker( encrypted, iv ):
	global wendy_string

	key_length = wendy_key_length

	# current block
	blocks = len( encrypted ) // len( iv )

	print "Encrypted Length: " + str( len( encrypted ) )
	print "Blocks: " + str( blocks )

	# solve the blocks in order
	# iv is the "0th" block
	#
	# [IX] XXXXXXX
	# I [AX]XXXXXX
	# I A[BX]XXXXX
	# I AB[CX]XXXX
	# ...
	# I ABCDEF[GX]

	decrypted_string = ""

	decrypted_string += wendy_undo( key_length, iv + encrypted[0:key_length] )

	for i in range( 1, blocks ):
		decrypted_string += wendy_undo( key_length, encrypted[key_length*(i-1):key_length*(i+1)] )
		print str(i+1) + "/" + str(blocks)

	print decrypted_string


def wendy_undo( key_length, encrypted ):

	# loop over characters in block
	#
	# first make XXXXXX22
	# then make  XXXXX333
	# then make  XXXX4444
	# ...
	##
	# First we try to make the end of the string be "\x02\x02"
	#
	# So look for bit changes that make the padding BAD
	# This means ending with \x02 thru \x0F
	# \x02 is the one we want but we don't know which it is, of the bad ones

	solved = ""

	falses = ""

	# iv doesn't matter
	iv = ops.random_string( key_length )

	stooge_index = -1
	loc = key_length

	for i in range( 0, 256 ):
		test = ops.splice( encrypted, loc + stooge_index, 1, chr( i ) )

		if ( not wendy_check_padding( test, iv ) ):
			falses += chr( i )

	stooge_index = -2

	# Now, which of the ones that failed before succeed with ONE MORE
	# character changed, right before them?

	# Find the second-to-last character
	for f in falses:
		for i in range( 0, 256 ):
			test = ops.splice( encrypted, loc + stooge_index, 2, chr( i ) + f )

			if ( wendy_check_padding( test, iv ) ):

				# Make sure that the padding-success isn't dependent on the
				# third-from-last character
				#
				# Imagine the SPECIAL CASE where the string ends in -44XX
				# Both -4422 and -4444 are proper padding (and pass the above 'if')
				# and we don't know which is which (we just know they're both proper)
				#
				# Isolate the ends-in-22 case by changing the third character

				third = encrypted[ loc + stooge_index - 1]
				third = chr( ord( third ) ^ 0xFF )

				test2 = ops.splice( test, loc + stooge_index - 1, 1, third )

				if ( wendy_check_padding( test2, iv ) ):
					solved += chr( ord( f ) ^ ord( encrypted[ loc - 1] ) ^ 0x02 )
					solved += chr( i ^ ord( encrypted[ loc - 2 ] ) ^ 0x02 )

	# Find the rest of the characters
	for i in range( 2, 16 ):
		padding_val = i + 1

		test = encrypted

		for j in range( 0, i ):
			char = encrypted[ loc - 1 - j ]

			test = ops.splice( test, loc - 1 - j, 1, chr( ord( char ) ^ ord(solved[j]) ^ padding_val ) )

		stooge_index = -padding_val

		for k in range( 0, 256 ):
			test2 = ops.splice( test, loc + stooge_index, 1, chr( k ) )

			if ( wendy_check_padding( test2, iv ) ):
				solved += chr( k ^ ord( encrypted[loc + stooge_index] ) ^ padding_val )

	reverse = ""
	for s in solved:
		reverse = s + reverse
	
	return reverse