# Class

# To make your own objects, class keyword is used
class Scores(object): # Class names are capitalized
	pass

# Creating instance of Scores class
a = Scores()
print (type(a))

# Inside class we just have pass
# But we can define class Attributes and Methods

# 1. Attributes - Characteristics of objects
# Syntax for creating an attribute is:
# self.attribute = something

# 2. Methods - Putting functions within a class
# Special Method used right after object is created
# __init__()

class Scores(object): 
	def __init__(self,numbers):
		self.numbers = numbers
x = Scores(numbers = 85)
print x.numbers		
