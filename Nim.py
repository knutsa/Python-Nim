import pygame, random, os
#Constants
START_LIST = (1,3,5,7)
#
#Pygame Constants
WIDTH, HEIGHT = 500, 500 #For the pygame display
#colors
WHITE, BLACK, RED, BLUE, GREEN, YELLOW = (255,255,255), (0,0,0), (255,0,0), (0,0,255), (0,255,0), (255,255,0)
ORANGE, TURC, PINK, PURPLE = (255,125,0), (0,255,255), (255,125,125), (255,0,255)
COLORS = (WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE, TURC, PINK, PURPLE)
BACKGROUND = (0,125,0)
#Style source
SOURCE = "GUI_style"
MENU_SRC = os.path.join(SOURCE, "menu_buttons.txt")
YN_SRC = os.path.join(SOURCE, "yes_no.txt")
NAME_INPUT_SRC = os.path.join(SOURCE, "name_input.txt")
#Logo
LOGO_HEIGHT = (1*HEIGHT)//10
LOGO_COLOR = (0,0,0)
LOGO_TEXT_COLOR =  (255,255,255)
LOGO_FONT_SIZE = 40

#Player Classes
#Each has method for making move, these take care of updating the list describing the piles.
# As well as storing num of players and names
class Player:
    instances = 0
    def __del__(self):
        type(self).instances -= 1
class RandomBot(Player):
    "Computer Player making moves completely at random"
    def __init__(self):
        self.name = "Dum-Bot"
        type(self).instances += 1
    def make_move(self, piles):
        """Attempts to make a move chosen at random.
        Returns True if there exists a valid move and False otherwise."""
        l = [i for i in range(len(piles)) if piles[i]]
        if not l:
            return False
        ind = random.choice(l)
        piles[ind] = random.randint(0,piles[ind]-1)
        return True
class SmartBot(Player):
    "Computer Player always making a winning move in case it's possible"
    pass
class User(Player):
    "User Player. Makes moves based on instructions from the user."
    def __init__(self, another_user=False, talking_through_GUI=False, dis=None):
        type(self).instances += 1
        pre = "Spelare"+str(self.instances)+" " if another_user else ""
        self.talking_through_GUI = talking_through_GUI
        #Get your name:
        if not self.talking_through_GUI:
            self.name = input(pre+"Vad vill du bli kallad?\n")
        else:
            text_input_boxes = create_buttons(NAME_INPUT_SRC)
            text_input_boxes[0].update(pre+"Vad vill du bli kallad?")
            text_input_boxes[1].update("Spelare"+str(self.instances))
            self.name = get_text_input_via_gui(dis, text_input_boxes[0], text_input_boxes[1])
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

#Classes and Functions for the GUI
class GuiOption:
    """Describes the size and text of a button."""
    def __init__(self, pos, dim, color, txt, font_size=30, txt_color=BLACK):
        "Inits its Rect obj. and a surface obj. describing the text."
        (x,y), (w,h) = pos, dim
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.center = (x,y)
        self.color = color
        self.text = txt
        self.text_color = txt_color
        self.font_size = font_size
        self.preferred_width = w
        self.update(txt)
    def update_txtIMgPos(self):
        "Assures that its text-image is centered"
        marginx = (self.rect.w-self.txtImg.get_width())//2
        marginy = (self.rect.h-self.txtImg.get_height())//2
        self.txtImgPos = (self.rect.left+marginx,self.rect.top+marginy)
    def covers(self, pos):
        "Checks if a point is inside itself."
        return self.rect.collidepoint(pos)
    def draw(self, dis):
        "Draws itself. But doesn't update pygame display!"
        pygame.draw.rect(dis, self.color, self.rect)
        dis.blit(self.txtImg, self.txtImgPos)
    def update(self, text, position=0):
        """Updates its text value as well as the position, and value of its textImg attribute.
        By default it erases the old text. position 1 means append text. Otherwise (-1) append text at beginning."""
        if not position:
            self.text = text
        else:
            self.text = self.text+text if position==1 else text+self.text
        self.txtImg = pygame.font.SysFont(None,self.font_size,False).render(self.text, True, self.text_color)
        old_center = self.rect.center
        self.rect.w = max(self.preferred_width, self.txtImg.get_width()+20)
        self.rect.center = old_center
        self.update_txtIMgPos()
    def move(self, pos):
        "Moves itself. Setting the new center coordinates to pos."
        self.rect.center = pos
        self.update_txtIMgPos()
    def clear(self, dis):
        "Erases itself from screen."
        pygame.draw.rect(dis, BACKGROUND, self.rect)

def draw_pile(pos, n, color):
    "Draws a pile."
    pass
def draw_board(piles, dis):
    "Draws the board with current status during a game."
    pass
def draw_menu(dis, buttons, logo=None, header=None):
    "Draws the start menu."
    dis.fill(BACKGROUND)
    if logo: logo.draw(dis)
    if header: header.draw(dis)
    for button in buttons:
        button.draw(dis)
    pygame.display.update()
def create_buttons(src, start=0, end=0):
    """Reads all non-# lines in src and returns a tuple of GuiOptions."""
    res = []
    counter = 0
    with open(src) as file:
        for line in file:
            if line[0]=='#': continue
            counter += 1
            if end and counter-1>=end: continue
            if counter-1<start: continue

            args = line.split()[:8]
            for i in (0,1,2,3,6): args[i]=int(args[i]) if args[i]!='.' else '.' #convert pos, dim, font-s to int
            for i in (4,7): args[i] = tuple(int(args[i][c:c+2],16) for c in (0,2,4)) if args[i]!='.' else '.' #convert string to color tuple
            args[5] = " ".join(args[5].split('_'))

            pos, dim = args[:2], args[2:4]
            pos[0] *= WIDTH; dim[0] *= WIDTH
            pos[1] *= HEIGHT; dim[1] *= HEIGHT
            pos[0] //= 100; pos[1] //= 100; dim[0] //= 100; dim[1] //= 100
            
            ind = args.index('.') if '.' in args else len(args)
            res_args = [pos,dim]+args[4:ind]
            res.append(GuiOption(*res_args))
    return tuple(res)
def get_choice(dis, buttons):
    """Makes user chose a button. Returns index of that button in buttons"""
    clock = pygame.time.Clock()
    light = (80,80,80)
    is_inside = None
    while True:
        #Change to lighter color when mouse hovers over button
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(buttons)):
            button = buttons[i]
            if not is_inside==i and button.covers(mouse_pos):
                new_col = [0,0,0]
                last_old = button.color[:]
                for r in range(3): new_col[r] = min(255,button.color[r]+light[r])
                button.color = tuple(new_col)
                is_inside = i
                button.draw(dis)
                pygame.display.update()
            if is_inside==i and not button.covers(mouse_pos):
                button.color = last_old[:]
                is_inside = -1
                button.draw(dis)
                pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for i in range(len(buttons)):
                    if buttons[i].covers(pos):
                        return i
        clock.tick(30)
def get_text_input_via_gui(dis, header, input_box):
    "Takes text input via GUI. Does no input controls."
    clock = pygame.time.Clock()
    header.draw(dis)
    input_box.draw(dis)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_box.text
                if event.key == pygame.K_BACKSPACE:
                    input_box.clear(dis)
                    input_box.update(input_box.text[:-1])
                    input_box.draw(dis)
                    pygame.display.update()
                else:
                    input_box.update(event.unicode, 1)
                    input_box.draw(dis)
                    pygame.display.update()
        clock.tick(30)
            
#Controlling Functions
#These control the program flow
def get_data(dis, buttons, terminal_txt, talking_through_GUI):
    """Waits untill user choses button / number in 0...len(buttons).
    Channel determines if it's through terminal(0) or GUI (1). Only used in menu."""
    if talking_through_GUI:
        return get_choice(dis, buttons)
    return get_inp(inp_opts(tuple(str(i+1) for i in range(len(buttons))) ), terminal_txt, conv=lambda x:int(x)-1)

def game(players, piles, dis):
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
    #initiate Pygame and dis
    pygame.init()
    dis = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
    #Create GuiOptions
    #Buttontuples
    menu_buttons = create_buttons(MENU_SRC)
    yes_no_buttons = create_buttons(YN_SRC,0,2)
    #Logo
    logo = GuiOption((WIDTH//2, LOGO_HEIGHT//2), (WIDTH, LOGO_HEIGHT), LOGO_COLOR, "NIM!", LOGO_FONT_SIZE, LOGO_TEXT_COLOR)
    #Settings Variables
    game_mode = 1
    talking_through_GUI = 1
    while game_mode: #Keep going untill user choses 0 (next line)
        draw_menu(dis, menu_buttons, logo)
        game_mode = get_data(dis, menu_buttons,
            "Vill du spela mot en Enkel Dator(1), Svår Dator(2),mot en annan Människa(3) eller vill du avsluta(4)?",
            talking_through_GUI)+1; game_mode%=4
        if not game_mode:
            break
        if game_mode != 3:
            draw_menu(dis, yes_no_buttons, logo)
            wants_to_start = get_data(dis, yes_no_buttons,
            "Så här ser startläget ut. "+START_LIST.__str__()[1:-1]+" Vill du börja? Ja(1) Nej(2)",
            talking_through_GUI)
            draw_menu(dis, (), logo) #Clear buttons
            BotGen = RandomBot if game_mode == 1 else SmartBot
            user = User(False, talking_through_GUI, dis)
            players = (user, BotGen()) if wants_to_start else (BotGen(), user)
        else:
            draw_menu(dis, (), logo) #Clear buttons
            players = (User(True, talking_through_GUI, dis), User(True, talking_through_GUI, dis))
        keep_playing = True

        while keep_playing:  #Loop that deals with each game
            piles = list(START_LIST)
            winner = game(players, piles, dis)
            if type(players[winner]) == User:
                print("Grattis "+players[winner].name)
            else:
                print("Synd. Du förlorade. Bättre lycka nästa gång "+players[(winner+1)%2].name+'!')
            keep_playing = get_inp(inp_opts(('1','2')), "Vill du spela igen? Ja(1) Nej(2)", conv=lambda x:int(x)%2)
        players = ()
    print("Tack. Hej då!")
if __name__ == "__main__":
    main()
    

    

