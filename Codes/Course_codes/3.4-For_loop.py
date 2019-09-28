# For loop

# Initialize three list
numbers = [10, 20, 30, 40]
vehicles = ['cars', 'bikes', 'buses', 'trucks'] 
age = [40, 'fifty', 60, 'seventy'] 
# List can have numbers and strings 

# Execute for loop using the numbers in numbers list
for count in numbers:
	print 'This is number: %d' % count
	# %d indicates the list contains numbers 
	
# Execute for loop using the vehicle names in vehicles list
for automobiles in vehicles: 
	print 'A type of automobile: %s' % automobiles 
	# %s indicates the list contains strings 
	
# Execute for loop using numbers and strings in age list
for i in age:
	print 'My age is: % r' % i 
	# %r when we don't know what exactly is in the list  
	
# Initialize an empty element list, data will be appended to this list later 
element = []

# Execute for loop using the numbers in the range 0 to 8
for j in range(0, 8):
	print 'Adding to the list: %d' % j
	element.append(j) 
	# Appending data to the element list 

# Execute the for loop using the data appended in the element list
for k in element:
	print 'Retrieving back from the list: %d' % k
	
