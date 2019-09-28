# While loop

# Initialize variable i with value 0
i = 0

# Initialize an empty list 
count = []

# Start executing the while loop untill the value of i is less than 8
while i < 8:
	print ('The number is %d' % i)
	count.append(i) # Append the value to the empty list 
	
	i = i + 1 # Increment the value of variable i in steps of 1
	print ('The numbers in count list is:', count)

# Execute for loop using the values in count list 	
for numbers in count:
	print ('The numbers from the count list are: %d' % numbers)
	
