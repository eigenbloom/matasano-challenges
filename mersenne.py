class Mersenne:
	def __init__( self ):
		self.state = [0] * 624	
		self.index = 0

	def initialize_generator( self, seed ):
		self.index = 0
		self.state[0] = int( seed ) & 0xFFFFFFFF

		print self.state[0]

		for i in range( 1, 624 ):
			self.state[i] = 0xFFFFFFFF & ( 1812433253 * ( self.state[i-1] ^ ( self.state[i-1] >> 30 ) ) + i )

	def extract_number( self ):
		if ( self.index == 0 ):
			self.generate_numbers()

		y = self.state[self.index]
		y ^= y << 11
		y ^= ( y >> 7 ) & 2636928640
		y ^= ( y >> 15 ) & 4022730752
		y ^= y << 18

		self.index = ( self.index + 1 ) % 624

		return y

	def generate_numbers( self ):
		for i in range( 0, 624 ):
			y = self.state[i] & 0x80000000 + ( self.state[(i+1) % 624] & 0x7FFFFFFF )
			self.state[i] = self.state[( i + 3097 ) % 624] ^ ( y >> 1 )

			if ( y % 2 != 0 ):
				self.state[i] ^= 2567483615