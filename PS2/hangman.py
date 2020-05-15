# PS 2.2 Hangman Game
# 
# Name: Peter Bekins
# Date: 4/27/20


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
	"""
	Returns a list of valid words. Words are strings of lowercase letters.
	
	Depending on the size of the word list, this function may
	take a while to finish.
	"""
	print "Loading word list from file..."
	# inFile: file
	inFile = open(WORDLIST_FILENAME, 'r')
	# line: string
	line = inFile.readline()
	# wordlist: list of strings
	wordlist = line.split()
	print "  ", len(wordlist), "words loaded."
	return wordlist

def choose_word(wordlist):
	"""
	wordlist (list): list of words (strings)
	
	Returns a word from wordlist at random
	"""
	return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program

wordlist = load_words()

# your code begins here!

def letters_left(letters_guessed):
	"""
	Returns a string of the letters that have not yet been guesses
	"""
	all_letters = string.ascii_lowercase
	letters = ''
	for l in all_letters:
		if not l in letters_guessed:
			letters += l
	return letters

def check_guess(word, g):
	good_guess = False
	for w in word:
		if w == g:
			good_guess = True
	return good_guess

def check_word(word, letters):
	"""
	Returns string representing the current guess. Remaining letters are indicated
	by _, guessed letters by the letter.
	
	word is string of hidden word
	letters is string of letters that have been guessed 
	"""
	out_word = ''
	for w in word:
		if w in letters:
			out_word += w
		else:
			out_word += '_'
	return out_word

def hangman(wordlist, guesses):
	"""
	Function to implement one round of the game. 
	wordlist is list of good words
	guesses is integer  number of guesses allowed
	1. Randomly chooses a word from the word list. 
	2. Prompts user to guess letters until full word is guessed or guesses run out
	"""
	word = choose_word(wordlist)
	letters_guessed = []
	
	print "Welcome to the game, Hangman!"
	print "I am thinking of a word that is " + str(len(word)) + " letters long."
	print "-------------"
	
	current_word = ''
	
	while not(current_word == word) and guesses > 0:
		
		print "You have " + str(guesses) + " guesses left."
		print "Available letters: " + letters_left(letters_guessed)
		guess = raw_input("Please guess a letter:")
		
		# Check if letter has already been guessed, if so skip through loop
		double_guess = False
		if guess in letters_guessed:
			double_guess = True
		else:
			letters_guessed.append(guess)
		
		# Check status of word 
		current_word = check_word(word, letters_guessed)
		
		if double_guess:
			print "You already guessed " + guess + ":" + current_word
		elif check_guess(word, guess):
			print "Good guess: " + current_word
		else:
			print "Oops, That letter is not in my word: " + current_word
			guesses -= 1

	# Evaluate whether word was guessed or guesses ran out and print appropriate message
	print "-------------"

	if current_word == word:
		print "Congratulations!"
	elif guesses == 0:
		print "Sorry, you are out of guesses"
		print "The word was " + word

hangman(wordlist, 8)
