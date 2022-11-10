import numpy as np
from random import choice
import pygame
import sys
from math import inf, floor


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r, c] == 1:
                SCREEN.blit(player1piece_img, ((c)*SQUARESIZE +
                            30,  (r+1)*SQUARESIZE+80))
            elif board[r, c] == 2:
                SCREEN.blit(player2piece_img, ((c)*SQUARESIZE +
                            30,  (r+1)*SQUARESIZE+80))

    SCREEN.blit(board_img, (0, 150))
    pygame.display.update()


def clear():
    SCREEN.fill(WHITE)
    pygame.display.update()


def create_board(ROWS, COLUMNS):
    board = np.zeros((ROWS, COLUMNS))
    return board


def place(board, row, col, player):
    board[row, col] = player


def is_open(board, col):
    if board[0, col] == 0:
        return True
    else:
        return False


def next_open(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row, col] == 0:
            return row


def win_condition(board, player):
    # Horizontal condition
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r, c] == player and board[r, c+1] == player and board[r, c+2] == player and board[r, c+3] == player:
                return True

    # Downward diagonal
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r, c] == player and board[r-1, c+1] == player and board[r-2, c+2] == player and board[r-3, c+3] == player:
                return True

    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r, c] == player and board[r+1, c] == player and board[r+2, c] == player and board[r+3, c] == player:
                return True

    # Upward diagonal
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r, c] == player and board[r+1, c+1] == player and board[r+2, c+2] == player and board[r+3, c+3] == player:
                return True


def space_score(space, player):
    space_score = 0
    if player == AI_ID:
        opponent = HUMAN_ID
    else:
        opponent = AI_ID

    if space.count(player) == 4:
        space_score += 1000
    elif space.count(player) == 3 and space.count(0) == 1:
        space_score += 5
    elif space.count(player) == 2 and space.count(0) == 2:
        space_score += 2

    if space.count(opponent) == 3 and space.count(0) == 1:
        space_score -= 4

    return space_score


def decision_score(board, player):
    score = 0

    # Center score
    ctr_arr = [i for i in list(board[:, COLUMNS//2])]
    score += ctr_arr.count(player)*2

    # Horizontal score
    for r in range(ROWS):
        row_arr = [i for i in list(board[r, :])]
    for c in range(COLUMNS-3):
        space = row_arr[c:c+4]
        score += space_score(space, player)

    # Vertical score
    for c in range(COLUMNS):
        col_arr = [i for i in list(board[:, c])]
    for r in range(ROWS-3):
        space = col_arr[r:r+4]
        score += space_score(space, player)

    # Upward diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            space = [board[r+i, c+i] for i in range(4)]
            score += space_score(space, player)

    # Downward diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            space = [board[(r+3)-i, c+i] for i in range(4,)]
            score += space_score(space, player)

    return score


def get_terminal_nodes(board):
    return len(get_open_columns(board)) == 0 or win_condition(board, HUMAN_ID) or win_condition(board, AI_ID)


def get_depth(difficulty):
    if difficulty == 1:
        depth = choice((1, 1, 1, 2))
        return depth
    if difficulty == 2:
        depth = choice((1, 2, 2, 3, 3))
        return depth
    if difficulty == 3:
        depth = choice((5, 6))
        return depth


def minimax_ai(board, depth, alpha, beta, maxPlayer=True):
    open_cols = get_open_columns(board)
    terminal = get_terminal_nodes(board)
    if depth == 0 or terminal:
        if get_terminal_nodes(board):
            if win_condition(board, AI_ID):
                return (None, inf)
            elif win_condition(board, HUMAN_ID):
                return (None, -inf)
            else:
                return (None, 0)
        else:
            return (None, decision_score(board, AI_ID))

    if maxPlayer:
        value = -inf
        best_col = choice(open_cols)
        for col in open_cols:
            row = next_open(board, col)
            board_copy = board.copy()
            place(board_copy, row, col, AI_ID)
            running_score = minimax_ai(
                board_copy, depth-1, alpha, beta, False)[1]
            if running_score > value:
                value = running_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (best_col, value)

    else:
        value = inf
        best_col = choice(open_cols)
        for col in open_cols:
            row = next_open(board, col)
            board_copy = board.copy()
            place(board_copy, row, col, HUMAN_ID)
            running_score = minimax_ai(
                board_copy, depth-1, alpha, beta, True)[1]
            if running_score < value:
                value = running_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (best_col, value)


def get_open_columns(board):
    open_cols = []
    for col in range(COLUMNS):
        if is_open(board, col):
            open_cols.append(col)
    return open_cols


def player1_mode(difficulty):
    # 1 Player loop
    board = create_board(ROWS, COLUMNS)
    turn = 0
    game_over = False
    clear()
    draw_board(board)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]-50
                if turn == HUMAN:
                    SCREEN.blit(player1piece_img, (posx, int(SQUARESIZE/2)-50))
                    pygame.display.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = create_board(ROWS, COLUMNS)
                    clear()
                    draw_board(board)
                    pygame.display.update()
                    pygame.time.wait(500)
                    turn = HUMAN
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE))

                # Ask for Player 1 Input
                if turn == HUMAN:
                    posx = event.pos[0]
                    col = int(floor(posx/SQUARESIZE))
                    if col > 6:
                        col = 6

                    if is_open(board, col):
                        row = next_open(board, col)
                        place(board, row, col, HUMAN_ID)
                        draw_board(board)

                        if win_condition(board, HUMAN_ID):
                            label = myfont.render("You win!", 1, RED)
                            pygame.draw.rect(
                                SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                            SCREEN.blit(label, (250, 30))
                            game_over = True
                            pygame.display.update()
                            pygame.time.wait(3000)
                            pygame.draw.rect(
                                SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                            return game_over
                        elif not get_open_columns(board):
                            label = myfont.render("Draw!", 1, RED)
                            pygame.draw.rect(
                                SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                            SCREEN.blit(label, (300, 30))
                            game_over = True
                            pygame.display.update()
                            pygame.time.wait(3000)
                            pygame.draw.rect(
                                SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                            return game_over

                        turn += 1
                        turn = turn % 2

        # AI turn
        if turn == AI and not game_over:
            ai_col, minimax_score = minimax_ai(
                board, get_depth(difficulty), -inf, inf, True)

            if is_open(board, ai_col):
                # pygame.time.wait(500)
                row = next_open(board, ai_col)
                place(board, row, ai_col, AI_ID)
                draw_board(board)

                if win_condition(board, AI_ID):
                    label = myfont.render("You lose", 1, RED)
                    pygame.draw.rect(
                        SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                    SCREEN.blit(label, (250, 30))
                    game_over = True
                    pygame.display.update()
                    pygame.time.wait(3000)
                    pygame.draw.rect(
                        SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                    return game_over

                elif not get_open_columns(board):
                    label = myfont.render("Draw!", 1, RED)
                    pygame.draw.rect(
                        SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                    SCREEN.blit(label, (300, 30))
                    game_over = True
                    pygame.display.update()
                    pygame.time.wait(3000)
                    pygame.draw.rect(
                        SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                    return game_over

                turn += 1
                turn = turn % 2


def players2_mode():

    # 2 Players loop
    board = create_board(ROWS, COLUMNS)

    turn = choice((0, 1))
    game_over = False
    clear()
    draw_board(board)
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

            player = turn
            playerID = players_dict[player]

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]-50

                SCREEN.blit(player_imgs[player], (posx, int(SQUARESIZE/2)-50))
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                col = int(floor(posx/SQUARESIZE))

                if col > 6:
                    col = 6

                if is_open(board, col):
                    row = next_open(board, col)
                    place(board, row, col, playerID)
                    draw_board(board)

                    if win_condition(board, playerID):
                        label = myfont.render(
                            f"Player {playerID}  wins!", 1, RED)
                        pygame.draw.rect(
                            SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                        SCREEN.blit(label, (150, 30))
                        game_over = True
                        pygame.display.update()
                        pygame.time.wait(3000)
                        pygame.draw.rect(
                            SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                        return

                    elif not get_open_columns(board):
                        label = myfont.render("Draw!", 1, RED)
                        pygame.draw.rect(
                            SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                        SCREEN.blit(label, (3000, 30))
                        game_over = True
                        pygame.display.update()
                        pygame.time.wait(3000)
                        pygame.draw.rect(
                            SCREEN, WHITE, (0, 0, WIDTH, SQUARESIZE+50))
                        return game_over

                    turn += 1
                    turn = turn % 2


class Button():
    def __init__(self, x, y, image, scale=1):
        height = image.get_height()
        width = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action_trigger = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action_trigger = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        return action_trigger


pygame.init()
# Constants
ROWS = 6
COLUMNS = 7

SQUARESIZE = 100

WIDTH = COLUMNS * SQUARESIZE+50
HEIGHT = (ROWS+1) * SQUARESIZE+100
SIZE = (WIDTH, HEIGHT)

SCREEN = pygame.display.set_mode(SIZE)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
RADIUS = int(SQUARESIZE/2-1)

HUMAN = 0
AI = 1
PLAYER1 = 0
PLAYER2 = 1

HUMAN_ID = 1
AI_ID = 2
PLAYER1_ID = 1
PLAYER2_ID = 2

# Setup
board = create_board(ROWS, COLUMNS)
turn = 0
player_turn = 0
players_dict = {0: 1, 1: 2}
turn_count = 0

# Images
board_img = pygame.image.load('assets/connect4.png')
player1piece_img = pygame.image.load('assets/player1piece.png')
player2piece_img = pygame.image.load('assets/player2piece.png')
mode1_btn_img = pygame.image.load('assets/player1_btn.png')
mode2_btn_img = pygame.image.load('assets/player2_btn.png')
easy_btn_img = pygame.image.load('assets/easy_btn.png')
medium_btn_img = pygame.image.load('assets/medium_btn.png')
hard_btn_img = pygame.image.load('assets/hard_btn.png')
newgame_btn_img = pygame.image.load('assets/newgame_btn.png')
quit_btn_img = pygame.image.load('assets/quit_btn.png')

# Dictionaries
player_imgs = {PLAYER1: player1piece_img, PLAYER2: player2piece_img}
player_dict = {PLAYER1: PLAYER1_ID, PLAYER2: PLAYER2_ID}

# Initalize buttons

player1_mode_btn = Button(150, 0, mode1_btn_img)
player2_mode_btn = Button(450, 0, mode2_btn_img)

easy_btn = Button(60, 0, easy_btn_img)
medium_btn = Button(295, 0, medium_btn_img)
hard_btn = Button(540, 0, hard_btn_img)


# Game window
pygame.display.set_caption('Connect 4')

myfont = pygame.font.SysFont('assets\Raleway-VariableFont_wght.ttf', 90)

SCREEN.fill(WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    draw_board(board)

    mode1 = player1_mode_btn.draw()
    mode2 = player2_mode_btn.draw()

    if mode1:
        clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

            draw_board(board)

            easy = easy_btn.draw()
            medium = medium_btn.draw()
            hard = hard_btn.draw()

            if easy:
                player1_mode(1)
                break

            if medium:
                player1_mode(2)
                break

            if hard:
                player1_mode(3)
                break

    if mode2:
        players2_mode()
