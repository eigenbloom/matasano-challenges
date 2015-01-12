import binops as ops

class BadPaddingError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def PCKS7_pad( string, padToMultiple ):
	extra_chars = padToMultiple - ( len( string ) % padToMultiple )
	if ( extra_chars == padToMultiple ):
		extra_chars = 0

	while ( len(string) % padToMultiple != 0 ):
		string += chr( extra_chars )

	return string

def PCKS7_checkpad( string, padToMultiple ):
	last_character = string[-1]

	pad_length = ord( last_character )

	# if the last character has an index greater than the block size 
	# the string wasn't padded
	if ( pad_length > padToMultiple ):
		return True

	last_chars = string[-pad_length:]

	last_chars = last_chars.replace( last_character, "" )

	if ( len( last_chars ) > 0 ):
		return False

	return True

def PCKS7_unpad( string, padToMultiple ):
	output = ""

	try:
		last_character = string[-1]

		pad_length = ord( last_character )

		# if the last character has an index greater than the block size 
		# the string wasn't padded
		if ( pad_length > padToMultiple ):
			output = string

		last_chars = string[-pad_length:]

		last_chars = last_chars.replace( last_character, "" )

		if ( len( last_chars ) > 0 ):
			raise BadPaddingError( string[-padToMultiple:])

		output = string[:-pad_length]
	except BadPaddingError as b:
		print "Bad padding: " + b.value[:-pad_length] + " " + ops.ord_string( b.value[-pad_length:] )

	return output