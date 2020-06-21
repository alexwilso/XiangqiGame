# Author: 
# Date: 
# Description:


import pygame
from XiangqiGame import XiangqiGame

pygame.font.init() # initializes font
width = 1200 # sets width of gameboard
height = 1200 # sets height of gameboard
number_rows = 10  # number of rows
number_cols = 9 # number of columns
square_width = 1000 // 10 # width of game squares
square_height = 1000 // 10 # height of game squares
images = {} # dictionary used to store images
max_fps = 20
font = pygame.font.Font("freesansbold.ttf", 30)
title_font = pygame.font.Font("freesansbold.ttf", 95)


icon = pygame.image.load("Pieces/xiangqi.png")
pygame.display.set_icon(icon)

def loadImages():
    """
    Initializes dictionary of images used to put pieces on board
    """
    pieces = ["black_advisor", "black_cannon", "black_chariot", "black_elephant", "black_general", "black_horse",
              "red_advisor", "red_chariot", "red_elephant", "red_general", "red_horse", "red_soldier", "red_cannon",
              "black_soldier"]
    for piece in pieces: # loops through list of pieces, adds image location to image dictionary in proper format
        images[piece] = pygame.transform.scale(pygame.image.load("Pieces/" + piece + ".png"), (square_height, square_width))


def main():
    """
    Main function responsible for loading screen, board, and pieces. Also determines if user selecting piece to move and
    where to move from.
    """
    pygame.init() # initializes pygame
    screen = pygame.display.set_mode((width, height)) # sets display with 1200x1200 dimensions
    pygame.display.set_caption("Xiangqi") # displays Xiangqi title
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("#654321")) # fills background color of screen
    gs = XiangqiGame() # gets XiangiGame class
    loadImages()
    move_to = [] # list used to track move to loaction
    move_from = [] # list used to track move from location
    move_try = [100, 100] # list used to color board based on used move selection. Green for allowed move, red for not
    running = True # sets running to True
    first_move = False
    valid_move = False
    while running: # while running is true, game continues
        screen.blit(screen, (0, 0)) # loads screen
        for e in pygame.event.get():
            if e.type == pygame.QUIT: # if user exits game
                running = False # running set to false, and game exits
            elif e.type == pygame.MOUSEBUTTONDOWN: # if user presses mouse
                location = pygame.mouse.get_pos() # location is set to position of mouse
                if location[0] < 100 or location[0] > 1100 or location[1] > 1100 or location[1] < 100: # user selects
                    # position outside of board, so false is printed to console
                    print(False)
                else: # user selects piece inside board
                    col = ((location[0]-49)//100) - 1 # col is set to number 0-8
                    if col == 9: # if col is 9, user has selected piece outside of board
                        col = 8 # so col == last possible columnn
                    row = (location[1]//100) - 1 # row is set to number 0-9
                    if click_num == 0: # if first click
                        move_from = [row, col] # move from is set to current row and col
                        click_num += 1 # 1 is added to click
                        move_try = [row, col] # move try is set to row and col
                        first_move = True # first move is set to True used to color space
                        valid_move = False # valid move is set to False used to color space
                    elif click_num == 1: # second click
                        move_to = [row, col] # move_to = row and col
                        click_num = 0 # click num is reset
                        move_try = [row, col] # move try is set to row and col
                        # move is converted, so it can be used to try move on xiangqi
                        valid_move = gs.make_move(gs.convert_move_click(move_from), gs.convert_move_click(move_to))
                        print(valid_move) # move is printed to console
                        first_move = False # first move is set to false
        drawXiangqiGame(screen, gs, move_try[0], move_try[1], first_move, valid_move) # function is called with variables
        clock.tick(max_fps) # clock is run
        pygame.display.flip() # display is run

def drawXiangqiGame(screen, gs, row, col, move_from, move_to):
    """Function that fills screen, draws board and pieces, shows title, active player, gamestate, and in check variables."""
    screen.fill(pygame.Color("#654321"))
    drawboard(screen, row, col, move_from, move_to)
    drawpieces(screen, gs._board)
    show_active_player(screen, gs.get_active_player())
    show_game_state(screen, gs.get_game_state())
    show_in_check(screen, gs.get_in_check())
    show_title(screen)


def drawboard(screen, row, col, move_from, move_to):
    """Function that draws board. Also colors pieces on board as they are selected by user. Move from = yellow, valid
    move = green invalid move to = red"""
    count_row = 0 # count rows used to color board spaces
    count_col = 0 # count cols used to color board spaces
    colors = [pygame.Color("#d5a667"), pygame.Color(0, 0, 0)] # two colors of game board, black and tan
    for x in range(number_rows): # iterates through number of rows
        for y in range(number_cols): # iterates through number of columns
            if move_to and x == row and y == col: # if valid move to, space is turned to green
                pygame.draw.rect(screen, pygame.Color(25, 255, 0),
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))
            elif not move_to and not move_from and x == row and y == col: # invalid move to, space turned red
                pygame.draw.rect(screen, pygame.Color(255, 10, 10),
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))
            elif move_from and not move_to and x == row and y == col: # if selecting move from, space is turned yellow
                pygame.draw.rect(screen, pygame.Color(255, 255, 0),
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))
            else: # else, rows and columns are colored black and tan
                color = colors[((x + y) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(y*square_height+150, x*square_width+100, square_height, square_width))
                count_row += 1
                count_col += 1


def drawpieces(screen, board):
    """Functoin that draws pieces on game baord """
    for x in range(number_rows): # iterates through number of rows
        for y in range(number_cols): # itersates through number of columns
            piece = board[x][y] # sets piece to space on board
            if piece != "": # if board is not empty, appropriate piece is placed
                screen.blit(images[piece], pygame.Rect(y*square_height+150, x*square_width+100, square_height, square_width))

def show_active_player(screen, player):
    """displays active player on screen"""
    active_player = font.render("Active Player: " + str(player), True, (255, 255, 255))
    screen.blit(active_player, (10, 1133))

def show_game_state(screen, game_state):
    """Displays current game state on screen"""
    active_player = font.render("Game State: " + str(game_state), True, (255, 255, 255))
    screen.blit(active_player, (440, 1133))

def show_in_check(screen, in_check):
    """Displays piece in check on board"""
    in_check = font.render("In Check: " + str(in_check), True, (255, 255, 255))
    screen.blit(in_check, (850, 1133))

def show_title(screen):
    """displays title on screen"""
    active_player = title_font.render("Xiangqi", True, (255, 255, 255))
    screen.blit(active_player, (420, 0))

if __name__ == '__main__':
    main()
