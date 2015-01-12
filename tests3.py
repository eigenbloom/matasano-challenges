import padding as pad
import binops as ops
import stringops as sops
import transcoding as trans
import encops as enc
import account as acc
import frequency as freq
import ctr
import mersenne as mer
import time

def part17():
	text = ops.read_file( "saga_begins_lyrics.txt" )

	encrypted, iv = enc.wendy_encrypt( text )

	enc.wendy_breaker( encrypted, iv )

def part18():
	string = trans.base64_to_binary( "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==" )

	enc = ctr.encrypt( "grand jury probes twin cities terror recruiters, wrong turn traffic (in-error commuters) can't get where they're going or go where they're getting to", "YELLOW SUBMARINE")	
	plain = ctr.encrypt( enc, "YELLOW SUBMARINE" )

	print enc
	print plain

def part19():

	key_length = 16

	key = ops.random_string( key_length )

	strings = ops.read_file( "part_19_strings.txt" ).split( '\n' )

	for i in range( 0, len( strings ) ):
		strings[i] = trans.base64_to_binary( strings[i] )

	print strings
	print strings[37]

	enc_strings = []

	for s in strings:
		enc_strings.append( ctr.encrypt( s, key ) )

	char_strings = sops.columns_to_rows( enc_strings )	

	plain_strings = []
	nonce = ""

	for cs in char_strings:
		result = freq.xor_uncipher( cs )
		plain_strings.append( result.str )

		nonce += result.char

	nonce = nonce

	plain_strings = sops.columns_to_rows( plain_strings )

	print len( nonce )

	nonce = ops.splice( nonce, 32, 4, ops.xor( enc_strings[4][32:36], "head" ) )
	nonce = ops.splice( nonce, 36, 2, ops.xor( enc_strings[37][36:37], "n," ) )

	for es in enc_strings:
		print ops.xor( nonce, es )

	return 

def part20():

	key_length = 16

	key = ops.random_string( key_length )

	strings = ops.read_file( "part_20_strings.txt" ).split( '\n' )

	for i in range( 0, len( strings ) ):
		strings[i] = trans.base64_to_binary( strings[i] )

	enc_strings = []

	# encrypt each string and add it to a new array
	for s in strings:
		enc_strings.append( ctr.encrypt( s, key ) )

	# Make string of all first letters, all second letters, etc.
	# As if the old array were turned 90 degrees
	char_strings = sops.columns_to_rows( enc_strings )	

	plain_strings = []
	nonce = ""

	for cs in char_strings:
		result = freq.xor_uncipher( cs )
		plain_strings.append( result.str )

		nonce += result.char

	nonce = nonce

	plain_strings = sops.columns_to_rows( plain_strings )

	print len( nonce )

	for i in range( 0, len( strings ) ):
		ops.visual_compare( ops.xor( nonce, enc_strings[i] ), strings[i] )

	return 

#part17()
#part18()


#part19()
#part20()

Mer = mer.Mersenne()

t = time.time() * 1000

print t
Mer.initialize_generator( t )
print Mer.extract_number()
print Mer.extract_number()
print Mer.extract_number()
print Mer.extract_number()
#part21()