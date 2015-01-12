import binops as ops
from Crypto.Cipher import AES

def encrypt( string, key ):
	key_length = len( key )
	
	# Counter looks like this:
	# NNNNCCCC

	# N
	# Empty padding at beginning
	nonce = ""
	for i in range( 0, key_length / 2 ):
		nonce += '\x00'

	# C
	# Little-endian counter 
	counter = 0

	cipher = AES.new( key, AES.MODE_ECB, "" )

	encrypted = ""
	
	for i in range( 0, len( string ), key_length ):
		enc_counter = cipher.encrypt( nonce + ops.little_endian_string( counter, key_length ) )
	
		encrypted += ops.xor( string[i:i+key_length], enc_counter )

		counter += 1

	return encrypted

