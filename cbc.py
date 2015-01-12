import binops as ops
import padding as pad
from Crypto.Cipher import AES

key_length = 16
jerry_key = ops.random_string( key_length )
jerry_iv = ops.random_string( key_length )
jerry_header = "comment1=cooking%20MCs;userdata="
jerry_footer = ";comment2=%20like%20a%20pound%20of%20bacon"

cipher = AES.new( jerry_key, AES.MODE_CBC, "" )

def jerry_encrypt( string ):
	string.replace( ";", "" )
	string.replace( "=", "" )

	string = jerry_header + string + jerry_footer

	string = pad.PCKS7_pad( string, key_length )

	return ops.cbc_encrypt( string, jerry_iv, jerry_key )

def jerry_decrypt( encrypted ):
	string = ops.cbc_decrypt( string, jerry_iv, jerry_key )

	print string

	items = string.split( ";" )

	for i in items:
		if ( i == "admin=true" ):
			return True 

	return False