import transcoding as trans
import binops as ops

with open("longtelegram", "r") as f:
    text = f.read()

text = ops.repeating_xor( text, "FORRESTAL" );
text = trans.binary_to_base64( text );

outfile = open( "encrypted_message", "w" )

outfile.write( text )

outfile.close() 
