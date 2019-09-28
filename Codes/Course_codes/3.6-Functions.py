# Functions

# Defining a function
def student_scores(English, German, Spanish, French):
	print 'My score in English is %d:' % English
	print 'My score in German  is %d:' % German
	print 'My score in Spanish is %d:' % Spanish
	print 'My score in French  is %d:' % French
	
# Scores given to function directly
print 'Scores given directly to student_scores function:'
student_scores(70, 83, 92, 73)

# Scores given to function using variables
print 'Scores given using variables:'
score_1 = 70
score_2 = 83
score_3 = 92
score_4 = 73
student_scores(score_1, score_2, score_3, score_4)

# Scores added and given to function 
print 'Scores given by adding assignment scores:'
student_scores(65 + 5, 80 + 3, 90 + 2, 70 + 3)

# Scores added to varilable values and given to function 
print 'Scores added to values in variables'
student_scores(score_1 + 5, score_2 + 5, score_3 + 5, score_4 + 5)
