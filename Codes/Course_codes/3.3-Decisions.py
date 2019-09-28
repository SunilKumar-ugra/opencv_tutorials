# Decision making
 
print('What would you like to drink?')
print('1. coffee')
print('2. tea')

# Take input from user 
drink = input("enter your choice ")

# If the user has entered '1' enter if conditional statement 
if drink == '1':
	print( 'What kind of coffee would you like?')
	print ('1. Irish')
	print ('2. Americano')
	
	coffee = input("> ")
	
	if coffee == '1':
		print ('Irish coffee served')
	elif coffee == '2':
		print ('Americano coffee served')
	else:
		print ('Any coffee should be fine')

# If the user has entered '2' enter elif conditional statement 
elif drink == '2':
	print ('What kind of tea would you like?')
	print ('1. Green tea')
	print ('2. Black tea')
	
	tea = input("> ")
	
	if tea == '1':
		print ('Green tea served')
	elif tea == '2':
		print ('Black tea served')
	else:
		print ('Any tea should be fine')

# If the user has not entered '1' or '2' then enter else conditional statement 
else:
	print ('You have not choosen the right option')
