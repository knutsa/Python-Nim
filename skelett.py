import pygame
#Player Classes
class Player:
    def make_move(self, piles):
        "Makes a move based on the current game status, and updates the passed piles list."
        pass
class RandomBot(Player):
    "Computer Player making moves completely at random"
    pass
class SmartBot(Player):
    "Computer Player always making a winning move in case it's possible"
    pass
class User(Player):
    "User Player. Makes moves based on instructions from the user."
    pass

#Gui Functions and classes
class GuiOption:
    "Describes size, color and position of a GUI-button."
    def draw(self):
        "Draws itself."
        pass
class Board:
    "Describes the board"
    def draw(self):
        "Draws the board."
        pass
def draw_menu(buttons):
    "Draws the starting menu."
    pass

#Functions that control game flow
def game(players, piles):
 """Starts and controls a game given the two player objects facing each other.
    Returns the index of the winning player."""
    pass
   
def main():
    """Interacts with user to start games in different game modes."""
    pass
   

if __name__ == "__main__":
    main()
    

    

