# Author: 
# Date: 
# Description:


import pygame
from XiangqiGame import XiangqiGame

pygame.font.init()  # initializes font
width = 1200  # sets width of gameboard
height = 1200  # sets height of gameboard
number_rows = 10  # number of rows
number_cols = 9  # number of columns
square_width = 1000 // 10  # width of game squares
square_height = 1000 // 10  # height of game squares
images = {}  # dictionary used to store images
max_fps = 20
font = pygame.font.Font("freesansbold.ttf", 30)
title_font = pygame.font.Font("freesansbold.ttf", 95)

icon = pygame.image.load("Pieces/xiangqi.png")
pygame.display.set_icon(icon)


def load_images():
    """
    Initializes dictionary of images used to put pieces on board
    """
    pieces = ["black_advisor", "black_cannon", "black_chariot", "black_elephant", "black_general", "black_horse",
              "red_advisor", "red_chariot", "red_elephant", "red_general", "red_horse", "red_soldier", "red_cannon",
              "black_soldier"]
    for piece in pieces:  # loops through list of pieces, adds image location to image dictionary in proper format
        images[piece] = pygame.transform.scale(pygame.image.load("Pieces/" + piece + ".png"),
                                               (square_height, square_width))


def draw_board(screen, row, col, move_from, move_to):
    """Function that draws board. Colors pieces on board as they are selected by user. Move from = yellow, valid
    move = green invalid move to = red. Count_row and """
    current_row = 0  # tracks current row, used to color selected board spaces
    current_col = 0  # tracks current column, used to color selected board spaces
    colors = [pygame.Color(213, 166, 103), pygame.Color(0, 0, 0)]  # two colors of game board, black and tan

    for x in range(number_rows):  # iterates through number of rows
        for y in range(number_cols):  # iterates through number of columns

            # if valid move to, space is turned to green
            if move_to and x == row and y == col:
                pygame.draw.rect(screen, pygame.Color(25, 255, 0),
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))

            # invalid move to, space turned red
            elif not move_to and not move_from and x == row and y == col:
                pygame.draw.rect(screen, pygame.Color(255, 10, 10),
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))

            # if selecting move from, space is turned yellow
            elif move_from and not move_to and x == row and y == col:
                pygame.draw.rect(screen, pygame.Color(255, 255, 0),
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))

            # Rows and columns are colored black and tan
            else:
                color = colors[((x + y) % 2)]
                pygame.draw.rect(screen, color,
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))
                current_row += 1  # current_row is incremented
                current_col += 1  # current_col is incremented


def draw_pieces(screen, board):
    """Functoin that draws pieces on game baord. Iterates through rows and columns and places piece on board if board
    place is not empty"""
    for x in range(number_rows):  # iterates through number of rows
        for y in range(number_cols):  # itersates through number of columns
            piece = board[x][y]  # sets piece to space on board
            if piece != "":  # if board is not empty, appropriate piece is placed
                screen.blit(images[piece],
                            pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                        square_width))


def show_title(screen):
    """displays title on screen"""
    active_player = title_font.render("Xiangqi", True, (255, 255, 255))
    screen.blit(active_player, (420, 0))


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


def draw_xiangqi_game(screen, gs, row, col, move_from, move_to):
    """Function that fills screen, draws board and pieces, shows title, active player, gamestate, and in check variables."""
    screen.fill(pygame.Color(101, 67, 33))
    draw_board(screen, row, col, move_from, move_to)
    draw_pieces(screen, gs._board)
    show_active_player(screen, gs.get_active_player())
    show_game_state(screen, gs.get_game_state())
    show_in_check(screen, gs.get_in_check())
    show_title(screen)


def main():
    """
    Main function responsible for loading screen, board, and pieces. Also determines if user selecting piece to move and
    where to move from.
    """
    pygame.init()  # initializes pygame
    screen = pygame.display.set_mode((width, height))  # sets display with 1200x1200 dimensions
    pygame.display.set_caption("Xiangqi")  # displays Xiangqi title
    screen.fill(pygame.Color(101, 67, 33))  # fills background color of screen
    gs = XiangqiGame()  # gets XiangiGame class
    load_images()
    click_number = 0
    move_to = []  # list used to track move to location
    move_from = []  # list used to track move from location
    move_try = [100, 100]  # list used to color board based on used move selection. Green for allowed move, red for not
    running = True  # sets running to True
    first_move = False
    valid_move = False

    while running:  # while running is true, pygame continues to run
        screen.blit(screen, (0, 0))  # loads screen

        for e in pygame.event.get():  # while running is true, pygame continues to run

            if e.type == pygame.QUIT:  # if event quit is executed, running is turned to false
                running = False  # running set to false, and game exits

            # gets mouse click location on board, if off board prints false, else updates row and column
            elif e.type == pygame.MOUSEBUTTONDOWN:  # if user presses mouse
                location = pygame.mouse.get_pos()  # location is set to position of mouse
                # position outside of board, so false is printed to console
                if location[0] < 100 or location[0] > 1100 or location[1] > 1100 or location[1] < 100:  # user selects
                    print(False)
                # user selects piece inside board
                else:
                    col = ((location[0] - 49) // 100) - 1  # col is set to number 0-8
                    if col == 9:  # if col is 9, user has selected piece outside of board
                        col = 8  # so col == last possible columnn
                    row = (location[1] // 100) - 1  # row is set to number 0-9

                    # Piece Selection
                    if click_number == 0:  # if first click
                        move_from = [row, col]  # move from is set to current row and col
                        click_number += 1  # 1 is added to click
                        move_try = [row, col]  # move try is set to row and col
                        first_move = True  # first move is set to True used to color space
                        valid_move = False  # valid move is set to False used to color space

                    # Move selection
                    elif click_number == 1:  # second click
                        move_to = [row, col]  # move_to = row and col
                        click_number = 0  # click num is reset
                        move_try = [row, col]  # move try is set to row and col
                        # move is converted, so it can be used to try move on xiangqi
                        valid_move = gs.make_move(gs.convert_move_click(move_from), gs.convert_move_click(move_to))
                        first_move = False  # first move is set to false

        # Updates screen and board based on user selection
        draw_xiangqi_game(screen, gs, move_try[0], move_try[1], first_move,
                          valid_move)
        pygame.display.update()  # display is updated


if __name__ == '__main__':
    main()
