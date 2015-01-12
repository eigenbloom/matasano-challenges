def remove_whitespace( string ):
	output = string

	chars = "\n\r \t"

	for c in chars:
		output = output.replace( c, "" )
		
	return output

def xor( char1, char2 ):
	return chr( ord( char1 ) ^ ord( char2 ) )

# given an array of strings A, return B, where B[n] is the (n+1)th character of 
# each string of A, in order 
def columns_to_rows( string_array ):
	max_length = 0;
	for string in string_array:
		if ( len( string ) > max_length ):
			max_length = len( string )

	output_array = [""] * max_length

	for string in string_array:
		for i in range( 0, len( string ) ):
			output_array[i] += string[i]

	return output_array