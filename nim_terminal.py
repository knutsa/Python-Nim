import random
from bots import Player, SmartBot, RandomBot, generate_board
#Constants
START_LIST = (1,3,5,7)

#Player Classes
#Each has method for making move, these take care of updating the list describing the piles.
# As well as storing num of players and names
class User(Player):
    "User Player. Makes moves based on instructions from the user."
    def __init__(self, another_user=False):
        type(self).instances += 1
        pre = "Spelare"+str(self.instances)+" " if another_user else ""
        self.name = input(pre+"Vad vill du bli kallad?\n")
    def make_move(self, piles):
        if not [i for i in piles if i]:
            return False
        ind = get_inp(inp_range(1,len(piles)+1)+((lambda i: piles[int(i)-1],"Du får inte välja en tom hög. Försök igen"),),
            "Från vilken hög vill du plocka?",
            conv = int) - 1
        amount = get_inp(inp_range(1,piles[ind]+1),
        "Hur många marker vill du ta bort?", conv=int)
        piles[ind] -= amount
        return True

#Input -- Output - terminal
#Functions for controlling indata and outdata via keyboard
def get_inp(conds, txt1, end="\n", conv=lambda x:x):
        """Keeps asking the user for input untill given a value that fulfills all conds.
         Takes an ordered iterable object of pairs with conditions and corresponding error messages that are complemented with end.
         Each condition function has to be capable of taking arbitrary string inputs that has passed all previous conditions."""
        ask_str = txt1
        while True:
            res = input(ask_str+end)
            is_legit = True
            for cond, err in conds:
                if not cond(res):
                    is_legit = False
                    ask_str = err
                    break
            if is_legit:
                break
        return conv(res)         
def inp_range(a,b):
    """Generates a function-error-messages tuple used in get_inp to get integer inputs satisfying a<=x<b."""
    isInt = lambda x:x.isnumeric()
    inRange = lambda x:a<=int(x)<b
    return ( (isInt, "Du måste ange ett heltal. Försök igen."),\
    (inRange,"Du måste ange ett tal mellan {0} och {1}. Försök igen.".format(a,b-1)) )
def inp_opts(opts):
    """Generates a function-error-messages tuple used in get_inp to get input that matches one of the options in opts."""
    isOption = lambda x:x in opts
    return ((isOption, "Det var inte ett alternativ. Ange något av"+opts.__str__()[1:-1]),)
def print_board(piles, turn):
    """Prints the board on R-form in the terminal."""
    print("Runda nr "+str(turn))
    print("Nuvarande Bräde")
    print("="*50)
    for i in range(len(piles)):
        print(("H{0}: "+"R"*piles[i]).format(i+1))
    print("="*50)


#Main Functions
#These control the game flow
def game(players, piles):
    """Starts and controls a game given the two player objects facing each other.
    Returns the index of the winning player."""
    turn = 0
    while True:
        phasing = players[turn%2]
        if type(phasing) == User:
            print_board(piles, turn+1)
        print("Din tur "+phasing.name)
        if not phasing.make_move(piles):
            print("...nej visst du har förlorat!")
            return (turn+1)%2
        print("Ok")
        turn += 1

def main():
    """Interacts with user to start games in different game modes."""
    game_mode = 1
    while game_mode: #Keep going untill user choses 0 (next line)
        game_mode = get_inp(inp_opts(('1','2','3','4')),
            "Vill du spela mot en Enkel Dator(1), Svår Dator(2),mot en annan Människa(3) eller vill du avsluta(4)?",
            conv=int); game_mode%=4
        keep_playing = bool(game_mode) #Sets to True in All cases except when 0 was chosen, in which case program should exit
        if game_mode != 3 and game_mode:
            BotGen = RandomBot if game_mode == 1 else SmartBot
            players = (User(), BotGen())
        elif game_mode:
                players = (User(True), User(True))

        while keep_playing:  #Loop that deals with each game
            piles = generate_board()
            if game_mode!=3:
                user_ind = 0 if type(players[0])==User else 1
                bot_ind = (user_ind+1)%2
                wants_to_start = get_inp(inp_opts(('1','2')),
                    "Så här ser startläget ut. "+piles.__str__()[1:-1]+" Vill du börja? Nej(1) Ja(2)",
                    conv=int)-1
                players = players[user_ind], players[bot_ind] if wants_to_start else players[bot_ind], players[user_ind]
            winner = game(players, piles)
            players[winner].wins += 1
            if type(players[winner]) == User:
                print("Grattis "+players[winner].name)
            else:
                print("Synd. Du förlorade. Bättre lycka nästa gång "+players[(winner+1)%2].name+'!')
            keep_playing = get_inp(inp_opts(('1','2')), "Vill du spela igen? Nej(1) Ja(2)", conv=int)-1
        players = ()
    print("Tack. Hej då!")
if __name__ == "__main__":
    main()