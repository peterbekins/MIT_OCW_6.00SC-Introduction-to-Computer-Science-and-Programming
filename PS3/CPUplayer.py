# PS 3B Word Game with CPU player
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name: Peter Bekins
# Date: 4/28/20

from wordgame import *
import time
from perm import *


# Problem 1: Implement a function that allows the CPU to choose a word

def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    hand_len = calculate_handlen(hand)
    high_score = 0
    best_word = ''
    # 1. make list of every permutation of size n using get_perms(hand, n)
    for i in range(1, hand_len + 1):
        perms_list = get_perms(hand, i)
        for p in perms_list:
            # 2. Check if it is a valid word with is_valid_word(word, hand, word_list)
            if is_valid_word(p, hand, word_list):
                # 3. Check score with get_word_score(word, n)
                score = get_word_score(p, hand_len)
                if score > high_score:
                    best_word = p
                    high_score = score
    #print "Best word is ", best_word, " at ", high_score, " points"
    return best_word
#
# Problem 2: Implement a function that allows CPU to play a hand
#
def comp_play_hand(hand, word_list):
    """
    Allows the computer to play the given hand, as follows:

    * The hand is displayed.
    * The computer chooses a word using comp_choose_words(hand, word_dict).
    * After every valid word: the score for that word is displayed,
    the remaining letters in the hand are displayed, and the computer
    chooses another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    end_hand = False
    total_score = 0
    current_hand = hand.copy()
    start_hand_len = calculate_handlen(current_hand)
   
    while not(end_hand):

        # 1. Display current letters left in hand
        print "Current Hand: ",
        display_hand(current_hand)

        # 2. Computer chooses best word
        comp_word = comp_choose_word(current_hand, word_list)
        word_score = get_word_score(comp_word, start_hand_len)
        total_score += word_score
        if comp_word != '':
            print '"', comp_word, '" earned ', word_score, ' points. Total: ', total_score, ' points'            # 2. Adjust hand
            current_hand = update_hand(current_hand, comp_word)

        if calculate_handlen(current_hand) == 0 or comp_word == '':
            end_hand = True
            print ''
            print "Total score: ", total_score, " points"
    
#
# Problem 3: Implement a function to play a game with CPU player
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    hand = {}
    choice1 = ''

    while choice1 != 'e':
        
        make_choice1 = True
        make_choice2 = True

        # 1. User turn
        while make_choice1 == True:
            choice1 = raw_input('Please enter "n" to start a new hand, "r" to replay last hand, or "e" to exit: ')
            if choice1 == 'n':
                hand = deal_hand(HAND_SIZE)
                play_hand(hand, word_list)
                make_choice1 = False
            elif choice1 == 'r':
                play_hand(hand, word_list)
                make_choice1 = False
            elif choice1 == 'e':
                make_choice1 = False
            else:
                print "Invalid choice"
                make_choice1 = True

        # 2. CPU turn
        while make_choice2 == True and choice1 != 'e':
            choice2 = raw_input('Please enter "u" to start a new user hand or "c" to start a new CPU hand:')
            if choice2 == 'c':
                comp_play_hand(hand, word_list)
                make_choice2 = False
            elif choice2 == 'u':
                make_choice2 = False
            elif choice2 != 'c':
                print "Invalid choice"
                make_choice2 = True

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
