# PS 4: Caesar Cipher
#
# Name: Peter Bekins
# Date: 4/29/20
#
# A Caeser cipher works by shifting the value of every letter in a message by a
# given integer key, e.g., h + 2 = J, Y + 2 = A, etc. This project involves
# creating functions to encode and decode messages using Caeser ciphers.
# The final problem was to decode a fable that was encrypted using a sequence of
# multiple shifts. To make things simpler, these shifts were only applied at initial
# word boundaries, so you could presumably:
#   1) move from left to right through the text, applying shifts (from 1 to 28)
#   2) when you decoded a sequence word + space, record the shift and start anew
#      at the next word
#   3) repeat until all words in the fable have been decoded
# In practice, however, it was possible to "decode" sequences of real words that were not
# actually part of the original fable. Consequently, the decoded message did not line
# up exactly with the original. No solution to this fable problem was included in the posted
# solutions, so I assume they realized their mistake and simplified future problem sets.

import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
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

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
   # Normalize word to lowercase and strip any non letter characters
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    #print "checking: ",word
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    #print s
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    lower = string.ascii_lowercase + ' '
    upper = string.ascii_uppercase + ' '
    code = {}

    for i in range(0, 27):
        if i < 27 - shift:
            new_upper = upper[i + shift]
            new_lower = lower[i + shift]
        elif i >= 27 - shift:
            new_upper = upper[i - 27 + shift]
            new_lower = lower[i - 27 + shift]
        code[upper[i]] = new_upper
        code[lower[i]] = new_lower
        
    #print code
    return code

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    code = build_coder(shift)
    return code

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    code = build_coder(-1 * shift)
    return code
 

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    out_text = ''
    for c in text:
        if coder.get(c) != None:
            out_text += coder[c]
        else:
            out_text += c
    #print out_text
    return out_text

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    out_text = apply_coder(text, build_encoder(shift))
    return out_text
   
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    shift = 0
    decoded = False
    while not decoded and shift <= 27:
        # 1. apply a decoder
        out_text = apply_coder(text, build_decoder(shift))
        # 2. check if it is decoded
        decoded = is_decoded(wordlist, out_text)
        # 3. If not decoded, increment shift and try again
        if not decoded:
            shift += 1
            
    return shift

def is_decoded(wordlist, text):
    """
    Checks whether all words in a text are valid, returns a boolean

    text = possibly decoded text
    wordlist = list of valid words
    """
    # Tokenize text string into words
    test_text = text.split()
    # Assume decoded is True, if any word is not valid, set to False
    decoded = True
    
    for word in test_text:
        if not is_word(wordlist, word):
            decoded = False

    return decoded
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """

    for shift in shifts:
        shift_text = apply_shift(text[shift[0]:], shift[1])
        text = text[:shift[0]] + shift_text
    return text
 
#
# Problem 4: Multi-level decryption.
#

def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """

    # 1. initialize list for shifts
    shifts = []
    # 2. pass list to recursive function where it will be mutated
    find_best_shifts_rec(wordlist, text, 0, shifts)
    # 3. return mutated list of shifts
    return shifts

def find_best_shifts_rec(wordlist, text, start, shifts):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """

    # 1. Apply a shift to the text[start:]
    # 2. Work through the shifted text until there is a space
    # 3. If there is a space, check whether text before space is decoded
    # 3a.If yes, move to next space and repeat 3
    # 3b.If no repeat 1

    # print "current shifts:", shifts

    shifted_text = apply_shifts(text, shifts)
    # print("Current solution:", shifted_text)
    
    if is_decoded(wordlist, shifted_text):
    # print("Final shifts in recursion:", shifts)
        return shifts
    else:
        #print ''
        #print "text is:", text
        shift = 0
        decoded = False
        good_string = ''
        
        while not decoded:
            new_text = apply_shift(shifted_text[start:], -1*shift)

            if not new_text[0] == ' ':
                good_string = find_good_words(wordlist, new_text)

            if len(good_string) > 0:
                print "hit: ", good_string
                shifts.append((start, -1*shift))
                new_start = start + len(good_string) + 1
                decoded = True
                find_best_shifts_rec(wordlist, text, new_start, shifts)
            else:
                shift += 1
                
            if shift == 28:
                # If shift = 28, then every shift was tried without decoding. This
                # means previous shift decoded a word but it was not part of message.
                # Set start to beginning of last decoded word and try again.
                print "No solution at:", start
                start = shifted_text[:start-1].rfind(' ') + 1
                print "Try over at:", start
                shift = 1        
  
             
def find_good_words(wordlist, text):
    """
    check to find first portion of text that is decoded
    """
    words = text.split()
    good_words = []
    for word in words:
        if is_word(wordlist, word):
            good_words.append(word)
        else:
            break
    return ' '.join(good_words)

def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    
    in_text = get_fable_string()
    shifts = find_best_shifts(wordlist, in_text)
    out_text = (apply_shifts(in_text, shifts))

    return out_text

#What is the moral of the story?
if __name__ == '__main__':
    fable = decrypt_fable()
    print(fable)

