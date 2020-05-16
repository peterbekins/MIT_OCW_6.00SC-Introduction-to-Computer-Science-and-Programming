This project involves the implementation of a scrabble-like word game. The player is served a list of random letters, which 
they use to build words and receive a score. 

The program CPUplayer extends the game by adding a CPU player who always returns the highest possible score. This is
implemented by brute force. The algorithm tries every combination of letters, checking each result against the list of 
possible words, and choosing the words that score the highest.
