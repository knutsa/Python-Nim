import random, math
#Player Classes
#Each has method for making move, these take care of updating the list describing the piles.
# As well as storing num of players and names
def get_nim_sum(l):
    "Returns the nim-sum/bitwise xor result of an iterable object."
    sum = 0
    for x in l:
        sum ^= x
    return sum

def generate_board(max_length = 10, max_pile_height = 20):
    "Generates a random starting board."
    length = random.randint(2,max_length)
    piles = [random.randint(1,max_pile_height) for i in range(length)]
    return piles

class Player:
    "Super class to the objects used in games. Counts wins and instances."
    wins = 0
    instances = 0
    def __init__(self):
        "Inits a player. Keeps of track of the number of active players."
        type(self).instances += 1
    def __del__(self):
        "Reduces number of players when one is deleted."
        type(self).instances -= 1
class RandomBot(Player):
    "Computer Player making moves completely at random"
    name = "Dum-Bot"
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
    name = "Smart-Bot"
    def make_move(self, piles, dis=None, board=None, board_buttons=None, board_header=None, logo=None):
        """Attempts to make a move. Optimal if there exists such a move.
        Returns True if there exists a valid move and False otherwise."""
        nim_sum = get_nim_sum(piles)
        def done(ind, num):
            piles[ind] = num
            if board:
                board.piles[ind].number = piles[ind]
                board.piles[ind].update_marker_list()
        #No winning move. Keep stalling.
        if not nim_sum:
            for i, height in enumerate(piles):
                if height:
                    done(i, height-1)
                    return True
            return False
        #Find winning move
        for i, height in enumerate(piles):
            opt = height^nim_sum
            if opt < height:
                done(i, opt)
                return True

