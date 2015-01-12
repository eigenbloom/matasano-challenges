import binops as ops
import padding as pad
from Crypto.Cipher import AES

idcount = 0

def field( key, value ):
	return key + " " + value

def profile_for( email ):
	email.replace( "=", "" )
	email.replace( "&", "" )

	profile = []

	profile.append( ("email", email) )
	profile.append( ("id", idcount) )
	profile.append( ("role", "user") )

	return send_profile( encode( profile ) )

def encode( kv ):
	output = ""

	for pair in kv:
		if ( output != "" ):
			output += "&"
		
		output += str( pair[0] ) + "=" + str( pair[1] )

	return output

key = ops.random_string( 16 )
cipher = AES.new( key, AES.MODE_ECB, "" )

def send_profile( string ):
	output = pad.PCKS7_pad( string, 16 )

	return cipher.encrypt( output )

def receive_profile( string ):
	output = cipher.decrypt( string )
	output = pad.PCKS7_unpad( output, 16 )

	return output