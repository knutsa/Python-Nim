# Specifikation

## Inledning
Jag tänkte programmera spelet Nim i två versioner, en som interagerar med användaren i terminalen och
en grafisk version. Användaren ska presenteras med en meny där hen kan välja mellan att spela mot en
slump-bot, en optimal bot eller en kompis.

De största svårigheterna med projektet är att se till att användare och bot-spelare aldrig gör ett otillåtet
drag, att ta in data grafiskt och att göra en bot som spelar optimalt. Av dessa förväntar jag mig att den
grafiska inläsningen av drag kommer ta längst tid eftersom det kräver ganska mycket funktioner som inte är
inbyggda i språket.

## Användarscenarier
### Slump-bot
Sten är uttråkad en lördag kväll så han sätter sig och spelar Nim. Han får upp en meny av alternativ
och väljer att spela mot en enkel slump-bot. Detta är både roligt och bra för självförtroendet eftersom
det är enkelt att vinna.

### Smart-bot
Sten har tröttnat på att spela mot en slump-bot. Nästa spel väljar han istället att spela mot en
smartare bot som hela tiden väljer ett vinnande drag om ett sådant finns. Eftersom detta sker varje
gång den hamnar i ett läge där Nim-summan av högarna inte är noll så förlorar Sten de flesta matcherna.

### Annan användare
Nu har Sten tröttnat på att förlora, men han har lärt sig mycket av att spela mot den svåra motståndaren. Han väljer istället att spela nästa nästa match
mot en kompis. Två användare turas om att göra drag och till slut vinner någon.

## Kodskelett
```python
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
```
## Programflöde
Programmet börjar med att anropa `main`. Genom denna presenteras användaren med en meny där hen kan välja spelläge. Beroende på spelläge skapas två spelar objekt.
1. Slump-bot - Ett `User` objekt och ett `RandomBot` objekt skapas
2. Smart-bot - Ett `User` objekt och ett `SmartBot` objekt skapas
3. Två `User` objekt skapas

Vid alternativ ett och två får användaren dessutom välja om den vill börja. Spelar objekten sparas i en `tuple` som sedan skickas till funktionen `game`. Denna styr
spelet genom att alternerande anropa respektive spelares `make_move` som är specifik för varje spelar objekt och ser till att inga ogiltiga drag sker.
Om inga drag finns returnerar spelar objektet som försökte utföra draget `false` genom sin `make_move` och således avslutas spelrundan
med motparten som vinnare.

