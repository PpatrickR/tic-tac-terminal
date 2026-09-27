import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
running = True
dt = 0
gridpos = None # store selection
activeX = []
activeO = []
turn = 0
pos_map = [(10,10), (260,10), (510,10), (10,260), (260,260), (510,260), (10,510), (260,510), (510,510)]


FONT_LARGEST = pygame.font.SysFont("Candara", 100, bold=True)
FONT_LARGE = pygame.font.SysFont("Candara", 70, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Candara", 50, bold=True)
FONT_SMALL = pygame.font.SysFont("Candara", 30, bold=True)

CELL_SIZE = 250
grid_cells = [
    ((col * CELL_SIZE, row * CELL_SIZE),
     (col * CELL_SIZE + CELL_SIZE, row * CELL_SIZE + CELL_SIZE))
    for row in range(3) for col in range(3)
]

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

def inside(p, box):
    (x1, y1), (x2, y2) = box
    return x1 <= p[0] <= x2 and y1 <= p[1] <= y2

def check_win(activeX,activeO):
    x_pos=[pos_map.index(k) for k in activeX]
    o_pos=[pos_map.index(k) for k in activeO]
    possible_wins= [
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ]
    for h in possible_wins:
        if all(i in o_pos for i in h):
            return 'O'
        elif all(i in x_pos for i in h):
            return 'X'
    return None

def check_draw(activeX,activeO):
    x_pos=[pos_map.index(k) for k in activeX]
    o_pos=[pos_map.index(k) for k in activeO]
    draw_pos=x_pos+o_pos
    if len(draw_pos)==9:
        return 9
    else:
        return None

def x_screen():
    buttons = [
        Button("Return to Main Menu",(200, 350, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for btn in buttons:
                if btn.is_clicked(event):
                    return "menu"
        screen.fill((0,0,255))
        screen.blit(FONT_LARGEST.render("X Won!", True, (0,0,0)), (240, 50))
        screen.blit(FONT_MEDIUM.render("Would you like to play again?", True, (0,0,0)), (80, 200))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def o_screen():
    buttons = [
        Button("Return to Main Menu",    (200, 350, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for btn in buttons:
                if btn.is_clicked(event):
                    return "menu"
        screen.fill((0,0,255))
        screen.blit(FONT_LARGEST.render("O Won!", True, (0,0,0)), (240, 50))
        screen.blit(FONT_MEDIUM.render("Would you like to play again?", True, (0,0,0)), (80, 200))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def draw_screen():
    buttons = [
        Button("Return to Main Menu",    (200, 350, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for btn in buttons:
                if btn.is_clicked(event):
                    return "menu"
        screen.fill((0,0,255))
        screen.blit(FONT_LARGE.render("Draw", True, (0,0,0)), (300, 100))
        screen.blit(FONT_MEDIUM.render("Would you like to play again?", True, (0,0,0)), (80, 200))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def menu_screen():
    buttons = [
        Button("Player vs Player",    (200, 350, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
        Button("Player vs CPU (Easy)",(200, 450, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
        Button("Player vs CPU (Hard)",(200, 550, 350, 70), FONT_SMALL, (0,0,0), (192,192,192)),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for i, btn in enumerate(buttons):
                if btn.is_clicked(event):
                    if i == 0:
                        return "play"
                    elif i == 1:
                        return  "play_ai_easy"
                    elif i == 2:
                        return "play_ai_hard"
        screen.fill((0,0,255))
        screen.blit(FONT_LARGE.render("Welcome to Tic-Tac-Toe!", True, (0,0,0)), (20, 100))
        screen.blit(FONT_MEDIUM.render("Choose a player mode:", True, (0,0,0)), (130, 200))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def ai_game_screen(mode="play_ai_easy"):
    gridpos = None
    activeX = []
    activeO = []
    turn = 0
    c1 = [(0,500),(249,750)]
    b1 = [(0,250),(249,500)]
    a1 = [(0,0),(249,250)]
    c2 = [(250,500),(499,750)]
    b2 = [(250,250),(499,500)]
    a2 = [(250,0),(499,250)]
    c3 = [(500,500),(750,750)]
    b3 = [(500,250),(750,500)]
    a3 = [(500,0),(750,250)]

    def get_empty_indices(activeX, activeO):
        return [i for i in range(9) if pos_map[i] not in activeX and pos_map[i] not in activeO]

    def random_ai_move(activeX, activeO):
        empties = get_empty_indices(activeX, activeO)
        return random.choice(empties) if empties else None

    def minimax_ai_move(activeX, activeO, player):
        def minimax(x_moves, o_moves, turn):
            winner = check_win(x_moves, o_moves)
            if winner == "X":
                return 1
            elif winner == "O":
                return -1
            elif len(x_moves) + len(o_moves) == 9:
                return 0
            empties = get_empty_indices(x_moves, o_moves)
            if turn == "X":
                best = -float("inf")
                for idx in empties:
                    score = minimax(x_moves + [pos_map[idx]], o_moves, "O")
                    best = max(best, score)
                return best
            else:
                best = float("inf")
                for idx in empties:
                    score = minimax(x_moves, o_moves + [pos_map[idx]], "X")
                    best = min(best, score)
                return best

        empties = get_empty_indices(activeX, activeO)
        best_score = -float("inf") if player == "X" else float("inf")
        best_move = None
        for idx in empties:
            if player == "X":
                score = minimax(activeX + [pos_map[idx]], activeO, "O")
                if score > best_score:
                    best_score = score
                    best_move = idx
            else:
                score = minimax(activeX, activeO + [pos_map[idx]], "X")
                if score < best_score:
                    best_score = score
                    best_move = idx
        return best_move

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                p = event.pos
                if inside(p, a1): gridpos = 0
                elif inside(p, a2): gridpos = 1
                elif inside(p, a3): gridpos = 2
                elif inside(p, b1): gridpos = 3
                elif inside(p, b2): gridpos = 4
                elif inside(p, b3): gridpos = 5
                elif inside(p, c1): gridpos = 6
                elif inside(p, c2): gridpos = 7
                elif inside(p, c3): gridpos = 8

        screen.fill("black")
        pygame.draw.line (screen, "white", (0,250), (750,250), width = 10)
        pygame.draw.line (screen, "white", (0,500), (750,500), width = 10)
        pygame.draw.line (screen, "white", (250,0), (250,750), width = 10)
        pygame.draw.line (screen, "white", (500,0), (500,750), width = 10)

        for x in activeX:
            impx = pygame.image.load("xttt.png")
            impx = pygame.transform.scale(impx,(230,230))
            screen.blit(impx, x)
        for x in activeO:
            impo = pygame.image.load("ottt.png")
            impo = pygame.transform.scale(impo,(230,230))
            screen.blit(impo, x)

        if gridpos is not None:
            if pos_map[gridpos] in activeX or pos_map[gridpos] in activeO:
                gridpos = None
            elif turn % 2 == 0:
                turn += 1
                impx = pygame.image.load("xttt.png")
                impx = pygame.transform.scale(impx,(230,230))
                screen.blit(impx, pos_map[gridpos])
                activeX.append(pos_map[gridpos])
                if mode == "play_ai_easy" and check_win(activeX, activeO) is None:
                    ai_move = random_ai_move(activeX, activeO)
                    if ai_move is not None:
                        turn += 1
                        impo = pygame.image.load("ottt.png")
                        impo = pygame.transform.scale(impo,(230,230))
                        screen.blit(impo, pos_map[ai_move])
                        activeO.append(pos_map[ai_move])
                elif mode == "play_ai_hard" and check_win(activeX, activeO) is None:
                    ai_move = minimax_ai_move(activeX, activeO, "O")
                    if ai_move is not None:
                        turn += 1
                        impo = pygame.image.load("ottt.png")
                        impo = pygame.transform.scale(impo,(230,230))
                        screen.blit(impo, pos_map[ai_move])
                        activeO.append(pos_map[ai_move])
            else:
                turn += 1
                impo = pygame.image.load("ottt.png")
                impo = pygame.transform.scale(impo,(230,230))
                screen.blit(impo, pos_map[gridpos])
                activeO.append(pos_map[gridpos])
            gridpos = None

        winner = check_win(activeX, activeO)
        if winner is not None:
            if winner == 'X':
                return "won_x"
            elif winner == 'O':
                return "won_o"
        if check_draw(activeX, activeO) == 9:
            return "draw"
        pygame.display.flip()
        clock.tick(60)

def game_screen():
    gridpos = None
    activeX = []
    activeO = []
    turn = 0
    c1 = [(0,500),(249,750)]
    b1 = [(0,250),(249,500)]
    a1 = [(0,0),(249,250)]
    c2 = [(250,500),(499,750)]
    b2 = [(250,250),(499,500)]
    a2 = [(250,0),(499,250)]
    c3 = [(500,500),(750,750)]
    b3 = [(500,250),(750,500)]
    a3 = [(500,0),(750,250)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                p = event.pos
                if inside(p, a1): gridpos = 0
                elif inside(p, a2): gridpos = 1
                elif inside(p, a3): gridpos = 2
                elif inside(p, b1): gridpos = 3
                elif inside(p, b2): gridpos = 4
                elif inside(p, b3): gridpos = 5
                elif inside(p, c1): gridpos = 6
                elif inside(p, c2): gridpos = 7
                elif inside(p, c3): gridpos = 8

        screen.fill("black")
        pygame.draw.line (screen, "white", (0,250), (750,250), width = 10)
        pygame.draw.line (screen, "white", (0,500), (750,500), width = 10)
        pygame.draw.line (screen, "white", (250,0), (250,750), width = 10)
        pygame.draw.line (screen, "white", (500,0), (500,750), width = 10)

        for x in activeX:
            impx = pygame.image.load("xttt.png")
            impx = pygame.transform.scale(impx,(230,230))
            screen.blit(impx, x)
        for x in activeO:
            impo = pygame.image.load("ottt.png")
            impo = pygame.transform.scale(impo,(230,230))
            screen.blit(impo, x)

        if gridpos is not None:
            if pos_map[gridpos] in activeX or pos_map[gridpos] in activeO:
                gridpos = None
            elif turn % 2 == 0:
                turn += 1
                impx = pygame.image.load("xttt.png")
                impx = pygame.transform.scale(impx,(230,230))
                screen.blit(impx, pos_map[gridpos])
                activeX.append(pos_map[gridpos])
            else:
                turn += 1
                impo = pygame.image.load("ottt.png")
                impo = pygame.transform.scale(impo,(230,230))
                screen.blit(impo, pos_map[gridpos])
                activeO.append(pos_map[gridpos])
            gridpos = None

        winner = check_win(activeX, activeO)
        if winner is not None:
            if winner == 'X':
                return "won_x"
            elif winner == 'O':
                return "won_o"
        if check_draw(activeX, activeO) == 9:
            return "draw"
        pygame.display.flip()
        clock.tick(60)

def main():
    state = "menu"
    ai_mode = "play_ai_easy"
    while state != "quit":
        if state == "menu":
            next_mode = menu_screen()
            if next_mode in ["play_ai_easy", "play_ai_hard"]:
                ai_mode = next_mode
            state = next_mode
        elif state == "play":
            state = game_screen()
        elif state in ["play_ai_easy", "play_ai_hard"]:
            state = ai_game_screen(mode=state)
        elif state == "won_o":
            state = o_screen()
        elif state == "won_x":
            state = x_screen()
        elif state == "draw":
            state = draw_screen()
        else:
            state = menu_screen()
    pygame.quit()

if __name__ == "__main__":
    main()