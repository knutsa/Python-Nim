import random, math
#Player Classes
#Each has method for making move, these take care of updating the list describing the piles.
# As well as storing num of players and names
class Player:
    wins = 0
    instances = 0
    def __del__(self):
        type(self).instances -= 1
class RandomBot(Player):
    "Computer Player making moves completely at random"
    def __init__(self):
        self.name = "Dum-Bot"
        type(self).instances += 1
    def make_move(self, piles, dis=None, board=None, board_buttons=None, board_header=None, logo=None):
        """Attempts to make a move chosen at random.
        Returns True if there exists a valid move and False otherwise."""
        l = [i for i in range(len(piles)) if piles[i]]
        if not l:
            return False
        ind = random.choice(l)
        piles[ind] = random.randint(0,piles[ind]-1)
        if board:
            board.piles[ind].number = piles[ind]
            board.piles[ind].update_marker_list()
        return True
class SmartBot(Player):
    "Computer Player always making a winning move in case it's possible"
    pass