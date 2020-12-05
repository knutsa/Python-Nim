import pygame, random, os, math
from bots import Player, SmartBot, RandomBot, generate_board
#Constants
START_LIST =  (1,3,5,7, 9, 11, 4)
#
#Pygame Constants
WIDTH, HEIGHT = 700, 700 #For the pygame display
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
BOARD_SRC = os.path.join(SOURCE, "board_buttons.txt")
HEADER_SRC = os.path.join(SOURCE, "headers.txt")
#Logo
LOGO_HEIGHT = (1*HEIGHT)//10
LOGO_COLOR = (0,0,0)
LOGO_TEXT_COLOR =  (255,255,255)
LOGO_FONT_SIZE = 40
#Board
BOTTOM_HEIGHT = (2*HEIGHT)//10
MARKER_MAX = 25


#Player Classes
#Each has method for making move, these take care of updating the list describing the piles.
# As well as storing num of players and names
class User(Player):
    "User Player. Makes moves based on instructions from the user."
    def __init__(self, another_user=False, dis=None):
        type(self).instances += 1
        pre = "Spelare"+str(self.instances)+" " if another_user else ""
        #Get your name:
        text_input_boxes = create_buttons(NAME_INPUT_SRC)
        text_input_boxes[0].update(pre+"Vad vill du bli kallad?")
        text_input_boxes[1].update("")
        self.name = get_text_input_via_gui(dis, text_input_boxes[0], text_input_boxes[1])
    def make_move(self, piles, dis, board, board_buttons, board_header, logo):
        "Checks if move exists. Asks user for a move and then performs it."
        if not [i for i in piles if i]:
            return False
        #Handy short cuts
        def talk(mssg):
            board_header.update(mssg)
            board_header.draw(dis)
            pygame.display.update()
        reshape_options = lambda options, pile_ind : list(board_buttons) + [marker for marker in options if marker.pile_index == pile_ind]
        draw_board(dis, board, (), logo, board_header)
        #Build list of markers
        all_markers = []
        for pile in board.piles:
            for marker in pile.marker_list:
                all_markers.append(marker)
        removed = [] #List of lists containing every removed marker in each event
        options = []
        def remove(index):
            "Removes a marker indexed in options, from options, all_markers and board"            
            to_remove = options[index]
            to_remove.clear(dis)
            del options[index]
            all_markers.remove(to_remove)
            board.piles[removed_ind].marker_list.remove(to_remove)
            board.piles[removed_ind].number -= 1
            removed.append([to_remove])
        #Get the first removed marker and the chosen pile
        ind = get_choice(dis, all_markers)
        removed_ind = all_markers[ind].pile_index
        pile_removing_from = board.piles[removed_ind]
        options = reshape_options(all_markers, removed_ind)
        ind = options.index(all_markers[ind])
        remove(ind)
        draw_board(dis, board, board_buttons, logo, board_header)
        #Start looping
        ind = get_choice(dis, options)
        while ind != 0 or options[0] != board_buttons[0]:
            if options[0] == board_buttons[0]: #Button features
                if ind == 0: #Pressed 'Avsluta'
                    return True
                elif ind == 1: #Pressed 'Ångra'
                    pile_removing_from.marker_list.extend(removed[-1])
                    pile_removing_from.number += len(removed[-1])
                    all_markers.extend(removed[-1])
                    options.extend(removed[-1])
                    del removed[-1]
                    if len(removed) == 0:
                        options = all_markers[:]
                        removed_ind = None
                elif ind == 2: #Pressed 'Ange antal'
                    options[2].update("")
                    #Get the input
                    number_to_remove = get_text_input_via_gui(dis, board_header, options[2])
                    while(not number_to_remove.isnumeric() or int(number_to_remove)<=0):
                        talk("Du måste ange ett positivt heltal.")
                        number_to_remove = get_text_input_via_gui(dis, board_header, options[2])
                    talk("Din tur "+self.name)
                    number_to_remove = int(number_to_remove)
                    #Actually removing
                    pile_removing_from.number = max(0, pile_removing_from.number-number_to_remove)
                    removed_together = pile_removing_from.update_marker_list()
                    for marker in removed_together:
                        all_markers.remove(marker)
                        options.remove(marker)
                    removed.append(removed_together)
                else: #Removed a random marker
                    remove(ind)
            else: #No Markers removed before
                removed_ind = options[ind].pile_index
                pile_removing_from = board.piles[removed_ind]
                remove(ind)
                options = reshape_options(options, removed_ind)
            passing_buttons = board_buttons if options[0]==board_buttons[0] else ()
            options[2].update("Ange antal")
            draw_board(dis, board, passing_buttons, logo, board_header)
            ind = get_choice(dis, options)
        piles[removed_ind] = pile_removing_from.number
        return True


#Classes and Functions for the GUI
class GuiOption:
    """Describes the size and text of a button."""
    def __init__(self, pos, dim, color, txt, font_size=30, txt_color=BLACK):
        "Inits its Rect obj. and a surface obj. describing the text. pos of center"
        (x,y), (w,h) = pos, dim
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.center = (x,y)
        self.color = color
        if color == WHITE:
            self.hover_color = tuple([(7*c)//10 for c in self.color])
        else:
            self.hover_color = tuple(min(255, c+100) for c in self.color)
        self.text = txt
        self.text_color = txt_color
        self.font_size = font_size
        self.preferred_width = w
        self.preferred_height = h
        self.COLOR = color
        self.update(txt)
    def hover(self, dis):
        "Alternates objects color to hovered mode."
        self.color = self.hover_color
        self.draw(dis)
    def unhover(self, dis):
        "Changes color back to COLOR"
        self.color = self.COLOR
        self.draw(dis)
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
        """Updates its text value either by creating a new(default) or appending(position=1) at beginning or end(position=-1).
        Also updates position and value of its textImg attribute according to new textvalue."""
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
class Marker:
    "Contains color, radius and position."
    def __init__(self, center, size, color, pile_index):
        self.color = color
        self.COLOR = color #Constant - original color
        if color == WHITE:
            self.hover_color = tuple([(7*c)//10 for c in self.color])
        else:
            self.hover_color = tuple(min(255, c+80) for c in self.color)
        self.center = center
        self.size = size
        self.pile_index = pile_index #Index telling which pile this marker lies in
    def draw(self, dis):
        "Draws itself."
        pygame.draw.circle(dis, self.color, self.center, self.size)
    def covers(self, pos):
        x,y = pos
        x0, y0 = self.center
        return self.size*self.size > (x-x0)*(x-x0)+(y-y0)*(y-y0)
    def clear(self, dis):
        pygame.draw.circle(dis, BACKGROUND, self.center, self.size)
    def hover(self, dis):
        "Alternates objects color to hovered mode."
        self.color = self.hover_color
        self.draw(dis)
    def unhover(self, dis):
        "Changes color back to COLOR"
        self.color = self.COLOR
        self.draw(dis)

class Pile:
    "Consists of a number box and a list of markers."
    def __init__(self, X_center, y_bottom, color, width, height, number, index, font_size=20):
        "Inits pile."
        n_width = min(100, width)
        self.X_center = X_center
        self.y_bottom = y_bottom-n_width
        self.width = width
        self.height = height-n_width
        self.number = number
        self.color = color
        self.index = index
        self.number_box = GuiOption((X_center,y_bottom-(3*n_width)//4), (n_width, n_width//2), BACKGROUND, str(number), font_size, color)
        self.index_box = GuiOption((X_center, y_bottom-n_width//4), (n_width,n_width//2), BACKGROUND, "Hög nr"+str(index+1), font_size, BLACK)
        self.marker_list = [] #List containing all markers in this pile. Starts empty untill needed.
        self.create_marker_list()

    def create_marker_list(self):
        "Fills the marker_list with markers"
        def add(r, relx, rely):
            pos = (self.X_center-self.width//2+r+relx+2, self.y_bottom-r-rely)
            self.marker_list.append(Marker(pos, r, self.color, self.index))
        size = self.find_size()
        relx, rely = 0, 0
        while len(self.marker_list)<self.number:
            add(size//2, relx, rely)
            relx += size
            if relx > self.width-size:
                relx = 0
                rely += size  
    def find_size(self):
        "Finds appropriate size of markers, given self.number"
        can_fit = lambda size : ((self.width-5)//size)*((self.height-5)//size) >= self.number
        max_size = MARKER_MAX
        high, low = max_size, 1
        while high-low>1:
            max_size = (high+low)//2
            if can_fit(max_size): #option, but maybe non-optimal
                low = max_size
            else:
                high = max_size
        return low

    def update_marker_list(self):
        "Removes markers from its list after a bot-move."
        res = []
        while(len(self.marker_list)>self.number):
            removing = self.marker_list[-1]
            res.append(removing)
            del self.marker_list[-1]
        return res
    def draw(self,dis):
        for marker in self.marker_list:
            marker.draw(dis)
        self.number_box.update(str(self.number))
        self.number_box.draw(dis)
        self.index_box.draw(dis)

class Board:
    "Creates a number of piles on a row."
    def __init__(self, piles):
        "Inits a board based on the starting piles."
        n = len(piles)
        self.piles = []
        pile_height = HEIGHT-LOGO_HEIGHT-BOTTOM_HEIGHT
        pile_width = WIDTH//n
        for i in range(len(piles)):
            color = random.choice(COLORS) 
            num_markers = piles[i]
            self.piles.append(Pile(i*pile_width+pile_width//2, LOGO_HEIGHT+pile_height, color, pile_width, pile_height,
                num_markers, i, font_size=20) )         
    def draw(self, dis):
        "Draws itself. No display update!"
        for pile in self.piles:
            pile.draw(dis)
    
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
    with open(src, encoding='utf-8') as file:
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
    while True:
        #Change to lighter color when mouse hovers over button
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(buttons)):
            button = buttons[i]
            if button.covers(mouse_pos):
                button.hover(dis)
            else:
                button.unhover(dis)
        pygame.display.update()   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit("Hej")
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for i in range(len(buttons)):
                    if buttons[i].covers(pos):
                        return i
        clock.tick(30)
def get_text_input_via_gui(dis, header, input_box):
    "Takes text input via GUI. Doesn't validate any input."
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
def draw_board(dis, board, buttons, logo, header=None):
    dis.fill(BACKGROUND)
    header.draw(dis)
    logo.draw(dis)
    board.draw(dis)
    for button in buttons:
        button.draw(dis)
    pygame.display.update()
            
#Controlling Functions
#These control the program flow
def talk_(dis, mssg, header):
    header.update(mssg)
    header.draw(dis)
    pygame.display.update()

def game(players, piles, board, dis, logo):
    """Starts and controls a game given the two player objects facing each other.
    Returns the index of the winning player."""
    #Useful variables
    turn = 0
    board_buttons = create_buttons(BOARD_SRC)
    board_header = create_buttons(HEADER_SRC, 1)[0]
    #Communication
    def talk(mssg):
        talk_(dis, mssg, board_header)
    while True:
        phasing = players[turn%2]
        if type(phasing) == User:
            draw_board(dis, board, board_buttons, logo, board_header)
        talk("Din tur "+phasing.name)
        
        if not phasing.make_move(piles, dis, board, board_buttons, board_header, logo):
            for button in board_buttons:
                button.clear(dis)
            pygame.display.update()
            talk("")
            return (turn+1)%2
        talk("Ok")
        turn += 1

def main(talking_through_GUI=True):
    """Interacts with user to start games in different game modes."""
    #initiate Pygame and dis
    pygame.init()
    dis = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
    #Create GuiOptions
    #Buttontuples
    menu_buttons = create_buttons(MENU_SRC)
    yn_buttons = create_buttons(YN_SRC,0,2)
    #Logo
    logo = GuiOption((WIDTH//2, LOGO_HEIGHT//2), (WIDTH, LOGO_HEIGHT), LOGO_COLOR, "NIM!", LOGO_FONT_SIZE, LOGO_TEXT_COLOR)
    #header
    yn_header = create_buttons(HEADER_SRC, 0, 1)[0]
    game_over_header1, game_over_header2 = create_buttons(HEADER_SRC, 2)
    #Settings Variables
    game_mode = 1
    while game_mode: #Keep going untill user choses 0 (next line)
        draw_menu(dis, menu_buttons, logo)
        game_mode = get_choice(dis, menu_buttons)+1
        game_mode %= 4
        if not game_mode:
            break
        piles = generate_board()
        if game_mode != 3:
            yn_buttons = create_buttons(YN_SRC)
            board = Board(piles)
            draw_board(dis, board, yn_buttons, logo, yn_header)
            wants_to_start = get_choice(dis, yn_buttons)
            BotGen = RandomBot if game_mode == 1 else SmartBot
            user = User(False, dis)
            players = (user, BotGen()) if wants_to_start else (BotGen(), user)
            user = None
        if game_mode == 3:
            draw_menu(dis, (), logo) #Clear buttons
            players = (User(True, dis), User(True, dis))
        keep_playing = True

        while keep_playing:  #Loop that deals with each game
            if players[0].wins + players[1].wins:
                piles = generate_board()
                board = Board(piles)
                draw_board(dis, board, yn_buttons, logo, yn_header)
                wants_to_start = get_choice(dis, yn_buttons)
                user_ind = 0 if type(players[0]) == User else 1
                if (wants_to_start+1)%2 != user_ind: #Should swap order
                    players = players[1], players[0]
                draw_menu(dis, (), logo) #Clear buttons
            winner = game(players, piles, board, dis, logo)
            players[winner].wins += 1
            if type(players[winner]) == User:
                talk_(dis, "Grattis du vann "+players[winner].name, game_over_header1)
            else:
                talk_(dis, "Synd. Du förlorade. Bättre lycka nästa gång "+players[(winner+1)%2].name+'!', game_over_header1)
            talk_(dis, "Vill du spela igen?", game_over_header2)
            keep_playing = get_choice(dis, yn_buttons)
        players = ()
    print("Tack. Hej då!")
if __name__ == "__main__":
    main()
    

