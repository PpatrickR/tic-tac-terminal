#importing the neccessary libraries
import pygame
import sys

#initilizing the pygame window
pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True
dt = 0

#setting the font for the homescreen
FONT_LARGE = pygame.font.SysFont("Candara", 70, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Candara", 50, bold=True)
FONT_SMALL = pygame.font.SysFont("Candara", 30, bold=True)

#making the buttons on the homescreen
class Button:
    def __init__(self, text, rect, font, color, bg):
        self.text_surf = font.render(text, True, color)
        self.rect = pygame.Rect(rect)
        self.bg = bg

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg, self.rect, border_radius=5)
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(event.pos)
        )

#function to see which box the user clicked
def inside(p, box):
    (x1, y1), (x2, y2) = box
    return x1 <= p[0] <= x2 and y1 <= p[1] <= y2


def check_sub_board_win(activeX, activeO):
    # activeX and activeO are now lists of local positions (0-8) within a sub-board
    possible_wins = [ 
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ]

    for h in possible_wins:
        if all(i in activeO for i in h):
            return 'O'
        elif all(i in activeX for i in h):
            return 'X'
    return None

def check_sub_board_draw(activeX, activeO):
    if len(activeX) + len(activeO) == 9:
        return True
    return False

def check_ultimate_win(won_boards_X, won_boards_O):
    possible_wins = [ 
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ]
    for h in possible_wins:
        if all(i in won_boards_O for i in h):
            return 'O'
        elif all(i in won_boards_X for i in h):
            return 'X'
    return None

#function that establises the homescreen
def menu_screen():
    buttons = [
        Button("Player vs Player", (20, 350, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
    ]

    #while loop to initilize pygame
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for i, btn in enumerate(buttons):
                if btn.is_clicked(event):
                    if i == 0:
                        return "pvp"

        screen.fill((0,0,255))
        screen.blit(FONT_LARGE.render("Ultimate Tic-Tac-Toe", True, (0,0,0)), (20, 100))
        screen.blit(FONT_MEDIUM.render("Choose a player mode:", True, (0,0,0)), (80, 200))

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

#stores which button was clicked by the user
mode = menu_screen()
if mode == "quit":
    pygame.quit()
    sys.exit()

#initilizes the variables needed for running the code
activeX = [[], [], [], [], [], [], [], [], []]
activeO = [[], [], [], [], [], [], [], [], []]
turn = 0
won_boards_O = []
won_boards_X = []
next_board = None

def get_board_and_position(mouse_pos):
    x, y = mouse_pos

    sub_board_row = y // 300
    sub_board_col = x // 300
    sub_board = sub_board_row * 3 + sub_board_col

    local_row = (y % 300) // 100
    local_col = (x % 300) // 100
    local_pos = local_row * 3 + local_col

    return sub_board, local_pos

def check_if_valid(sub_board, local_pos, activeX, activeO):
    
    
    if sub_board in won_boards_X or sub_board in won_boards_O:
        return False
    
    
    if local_pos in activeX[sub_board] or local_pos in activeO[sub_board]:
        return False
    if check_ultimate_win(won_boards_X, won_boards_O) is not None:
        return False
    
    return True

while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p = event.pos
            sub_board, local_pos = get_board_and_position(p)
            
            print(f"Click: sub_board={sub_board}, local_pos={local_pos}, next_board={next_board}")
            
            
            if next_board is not None:
                if next_board in won_boards_X or next_board in won_boards_O:
                    print(f"Resetting next_board {next_board} because it's won")
                    next_board = None
                elif len(activeX[next_board]) + len(activeO[next_board]) == 9:
                    print(f"Resetting next_board {next_board} because it's full")
                    next_board = None
            
            valid = check_if_valid(sub_board, local_pos, activeX, activeO)
            print(f"Move valid: {valid}")
            
            if valid:
                if turn % 2 == 0:
                    activeX[sub_board].append(local_pos)
                    if check_sub_board_win(activeX[sub_board], activeO[sub_board]) == 'X':
                        won_boards_X.append(sub_board)
                    
                    next_board = local_pos
                    
                    if next_board in won_boards_X or next_board in won_boards_O:
                        next_board = None
                    elif len(activeX[next_board]) + len(activeO[next_board]) == 9:
                        next_board = None
                else:
                    activeO[sub_board].append(local_pos)
                    if check_sub_board_win(activeX[sub_board], activeO[sub_board]) == 'O':
                        won_boards_O.append(sub_board)
                    
                    next_board = local_pos
                    
                    if next_board in won_boards_X or next_board in won_boards_O:
                        next_board = None
                    elif len(activeX[next_board]) + len(activeO[next_board]) == 9:
                        next_board = None
                turn += 1
            pass

    
    screen.fill("black")

    pygame.draw.line(screen, "white", (300, 0), (300, 900), width=20)
    pygame.draw.line(screen, "white", (600, 0), (600, 900), width=20)
    pygame.draw.line(screen, "white", (0, 300), (900, 300), width=20)
    pygame.draw.line(screen, "white", (0, 600), (900, 600), width=20)

    #top
    pygame.draw.line(screen, "white", (100, 0), (100, 300), width=2)
    pygame.draw.line(screen, "white", (200, 0), (200, 300), width=2)
    pygame.draw.line(screen, "white", (0, 100), (300, 100), width=2)
    pygame.draw.line(screen, "white", (0, 200), (300, 200), width=2)

    pygame.draw.line(screen, "white", (400, 0), (400, 300), width=2)
    pygame.draw.line(screen, "white", (500, 0), (500, 300), width=2)
    pygame.draw.line(screen, "white", (300, 100), (600, 100), width=2)
    pygame.draw.line(screen, "white", (300, 200), (600, 200), width=2)

    pygame.draw.line(screen, "white", (700, 0), (700, 300), width=2)
    pygame.draw.line(screen, "white", (800, 0), (800, 300), width=2)
    pygame.draw.line(screen, "white", (600, 100), (900, 100), width=2)
    pygame.draw.line(screen, "white", (600, 200), (900, 200), width=2)

    #mid
    pygame.draw.line(screen, "white", (100, 300), (100, 600), width=2)
    pygame.draw.line(screen, "white", (200, 300), (200, 600), width=2)
    pygame.draw.line(screen, "white", (0, 400), (300, 400), width=2)
    pygame.draw.line(screen, "white", (0, 500), (300, 500), width=2)

    pygame.draw.line(screen, "white", (400, 300), (400, 600), width=2)
    pygame.draw.line(screen, "white", (500, 300), (500, 600), width=2)
    pygame.draw.line(screen, "white", (300, 400), (600, 400), width=2)
    pygame.draw.line(screen, "white", (300, 500), (600, 500), width=2)

    pygame.draw.line(screen, "white", (700, 300), (700, 600), width=2)
    pygame.draw.line(screen, "white", (800, 300), (800, 600), width=2)
    pygame.draw.line(screen, "white", (600, 400), (900, 400), width=2)
    pygame.draw.line(screen, "white", (600, 500), (900, 500), width=2)

    #bottom
    pygame.draw.line(screen, "white", (100, 600), (100, 900), width=2)
    pygame.draw.line(screen, "white", (200, 600), (200, 900), width=2)
    pygame.draw.line(screen, "white", (0, 700), (300, 700), width=2)
    pygame.draw.line(screen, "white", (0, 800), (300, 800), width=2)
    
    pygame.draw.line(screen, "white", (400, 600), (400, 900), width=2)
    pygame.draw.line(screen, "white", (500, 600), (500, 900), width=2)
    pygame.draw.line(screen, "white", (300, 700), (600, 700), width=2)
    pygame.draw.line(screen, "white", (300, 800), (600, 800), width=2)

    pygame.draw.line(screen, "white", (700, 600), (700, 900), width=2)
    pygame.draw.line(screen, "white", (800, 600), (800, 900), width=2)
    pygame.draw.line(screen, "white", (600, 700), (900, 700), width=2)
    pygame.draw.line(screen, "white", (600, 800), (900, 800), width=2)
    
    
    for sub_board in range(9):
        sub_board_row = sub_board // 3
        sub_board_col = sub_board % 3
        for local_pos in activeX[sub_board]:
            local_row = local_pos // 3
            local_col = local_pos % 3

            x = sub_board_col * 300 + local_col * 100 + 10
            y = sub_board_row * 300 + local_row * 100 + 10
            impx = pygame.image.load("xttt.png")
            impx = pygame.transform.scale(impx, (80,80))
            screen.blit(impx, (x,y))
       
        
        for local_pos in activeO[sub_board]:
            local_row = local_pos // 3
            local_col = local_pos % 3

            x = sub_board_col * 300 + local_col * 100 + 10
            y = sub_board_row * 300 + local_row * 100 + 10

            impo = pygame.image.load("ottt.png")
            impo = pygame.transform.scale(impo, (80, 80))
            screen.blit(impo, (x,y))
        if sub_board in won_boards_X:
            big_x = pygame.image.load("xttt.png")
            big_x = pygame.transform.scale(big_x, (240, 240))
            x = sub_board_col * 300 + 30
            y = sub_board_row * 300 + 30
            screen.blit(big_x, (x, y))
        elif sub_board in won_boards_O:
            big_o = pygame.image.load("ottt.png")
            big_o = pygame.transform.scale(big_o, (240, 240))
            x = sub_board_col * 300 + 30
            y = sub_board_row * 300 + 30
            screen.blit(big_o, (x, y))   
    
    
    ultimate_winner = check_ultimate_win(won_boards_X, won_boards_O)
    if ultimate_winner is not None:
        font = pygame.font.SysFont(None, 72)
        msg = f"{ultimate_winner} wins!"
        text = font.render(msg, True, 'red')
        screen.blit(text, (200, 450))
        

    
    pygame.display.flip()

    
    dt = clock.tick(60) / 1000

pygame.quit()