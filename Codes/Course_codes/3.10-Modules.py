# Modules

# Modules are functions defined inside the body of a class
class Vehicles(object):

# Class object attribute	
	tyres = 4

# Class Vehicles get instantiated with seats
	def __init__ (self, seats=6):
		self.seats = seats
x = Vehicles()
print x.tyres
print x.seats

