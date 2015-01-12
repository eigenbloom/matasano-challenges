import padding as pad
import binops as ops
import stringops as sops
import transcoding as trans
import encops as enc
import account as acc

def part9():
        key = "Hello, my name's" 
        iv = "BlastoiseFlareon"

        string = "A long, long time ago, in a galaxy far away, Naboo was under an attack. And I thought me and Qui-Gon Jinn could talk the Federation in, to maybe cutting them a little slack"
        string = pad.PCKS7( string, 16 )

        enc = ops.cbc_encrypt( string, iv, key)
        print ops.cbc_decrypt( enc, iv, key )

def part10():
        text = ops.read_file( "part10_text.txt" )

        text = text.replace( "\n", "" )

        text = trans.base64_to_binary( text )

        iv = ""

        for i in range( 0, 16 ):
                iv += "\x00"

        print "iv is " + str( len( iv ) ) + " characters long"

        output = ops.cbc_decrypt( text, iv, "YELLOW SUBMARINE" )

        print output[0:60]

def part11():
        for i in range( 0, 20 ):
                print enc.oracle( ops.random_encrypt )

def part12():
        enc.willy_breaker()

def part13():
        key_length = 16

        padding = key_length - len( "admin" )

        # string structure

        # |---1---2---3---|---1---2---3---|---1---2---3---
        # email=helloiamanadminXXXXXXXXXXX
        # email=equal_end_block&id=0&role=

        # X's are mimicked padding characters

        admin_email = "helloiamanadmin"

        # Mimic PCKS7 padding
        while ( len( "email=" + admin_email ) % key_length != 0 ):
                admin_email += chr( padding )

        admin_string = acc.profile_for( admin_email )

        user_string = acc.profile_for( "equal_end_block" )

        admin_prof = acc.receive_profile( admin_string )
        user_prof = acc.receive_profile( user_string )

        print admin_prof + " " + str( len( admin_prof ) ) 
        print user_prof + " " + str( len( user_prof ) )
        
        stitched_string = user_string[0:32] + admin_string[16:32]

        stitched_prof = acc.receive_profile( stitched_string )

        print stitched_prof

def part14():
        enc.willy_breaker_2()

def part15():
        badpad = "hellomynameis\x04\x05\x06"
        print pad.PCKS7_unpad( badpad, 16 )

        goodpad = "menyazavut\x06\x06\x06\x06\x06\x06"
        print pad.PCKS7_unpad( goodpad, 16 )

def part16():

        #     0---4---8---c---       
        s1 = "garbledxxxxxxxxx" # 3rd block, 32 - 47
        s2 = "blahz:admin<true" # 4th block, 48 - 63
        #          |     |     
        #          5     11

        encrypted = enc.jerry_encrypt( s1 + s2 )

        # : to ;
        char = ord( encrypted[37] )
        char ^= 0x01
        encrypted = ops.splice( encrypted, 37, 1, chr( char ) )

        # < to =
        char = ord( encrypted[43] )
        char ^= 0x01
        encrypted = ops.splice( encrypted, 43, 1, chr( char ) )        

        print encrypted

        print enc.jerry_decrypt( encrypted ) 

#part12()
#part14()
#part15()

part16()