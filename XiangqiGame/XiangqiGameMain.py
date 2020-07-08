import pygame
from XiangqiGame import XiangqiGame

pygame.font.init()
width = 1200  # sets width of game board
height = 1200  # sets height of game board
number_rows = 10  # number of rows
number_cols = 9  # number of columns
square_width = 1000 // 10  # width of game squares
square_height = 1000 // 10  # height of game squares
images = {}  # dictionary used to store images
max_fps = 20
font = pygame.font.Font("freesansbold.ttf", 25)
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

    # iterates through pieces list, puts piece into image list in appropriate format to be placed onto board
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("Pieces/" + piece + ".png"),
                                               (square_height, square_width))


def draw_board(screen, row, col, move_from, move_to):
    """Function that draws board. Colors pieces on board as they are selected by user. Move from = yellow, valid
    move = green invalid move to = red."""

    current_row = 0  # tracks current row, used to color selected board spaces
    current_col = 0  # tracks current column, used to color selected board spaces
    colors = [pygame.Color(213, 166, 103), pygame.Color(0, 0, 0)]  # two colors of game board, black and tan

    for x in range(number_rows):
        for y in range(number_cols):

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

            # Rows and columns are colored black and tan and current row/column is incremented
            else:
                color = colors[((x + y) % 2)]
                pygame.draw.rect(screen, color,
                                 pygame.Rect(y * square_height + 150, x * square_width + 100, square_height,
                                             square_width))
                current_row += 1
                current_col += 1


def draw_pieces(screen, board):
    """Functoin that draws pieces on game baord. Iterates through rows and columns and places piece on board if board
    place is not empty"""

    # iterates through number of rows and columns, places piece on board when piece is not empty
    for x in range(number_rows):
        for y in range(number_cols):
            piece = board[x][y]
            if piece != "":
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
    screen.blit(in_check, (845, 1133))


def draw_xiangqi_game(screen, gs, row, col, move_from, move_to):
    """Function that fills screen, draws board and pieces, shows title, active player, gamestate, and in check
    variables."""

    screen.fill(pygame.Color(101, 67, 33))  # fills background color of screen
    draw_board(screen, row, col, move_from, move_to)
    draw_pieces(screen, gs.get_board())
    show_active_player(screen, gs.get_active_player())
    show_game_state(screen, gs.get_game_state())
    show_in_check(screen, gs.get_in_check())
    show_title(screen)


def main():
    """
    Main function responsible for loading screen, board, and pieces. Also determines if user selecting piece to move and
    where to move from.
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))  # sets display with 1200x1200 dimensions
    pygame.display.set_caption("Xiangqi")  # displays Xiangqi title
    gs = XiangqiGame()  # gets XiangiGame class
    load_images()
    click_number = 0
    move_to = []  # list used to track move to location
    move_from = []  # list used to track move from location
    move_try = [100, 100]  # list used to color board based on used move selection. Green for allowed move, red for not
    running = True  # sets running to True
    first_move = False
    valid_move = False

    # while running pygame continues to run
    while running:
        screen.blit(screen, (0, 0))

        # iterates through pygame events
        for e in pygame.event.get():

            # if quit is selected, running is set to false and pygame exits
            if e.type == pygame.QUIT:
                running = False

            # checks if mouse is pressed down, if so location is set to position of mouse on screen
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()

                # if location is spot on screen but off game board, false is printed to console.
                if location[0] < 100 or location[0] > 1100 or location[1] > 1100 or location[1] < 100:
                    print(False)

                # user selected position on board. Location is converted to row/column format (ex. col = 1, row = 2).
                # this is used to move pieces with move function in XiangqiGame file.
                else:
                    col = ((location[0] - 49) // 100) - 1
                    if col == 9:
                        col = 8
                    row = (location[1] // 100) - 1

                    # Checks if first click. If so, move_from is set to be used in move function on XiangqiGame file.
                    # Move_try is set and used to update board. Click number is incremented. First move is set to true
                    # and valid move is set to false.
                    if click_number == 0:
                        move_from = [row, col]
                        click_number += 1
                        move_try = [row, col]
                        first_move = True
                        valid_move = False

                    # Checks if second click. If so move_to is set to be used to move piece. Click number is reset. Move
                    # try is updated to move_to and used to update board. Valid_move is set to result of move method
                    # in XiangqiGame. First move is set to false
                    elif click_number == 1:
                        move_to = [row, col]
                        click_number = 0
                        move_try = [row, col]
                        valid_move = gs.make_move(gs.convert_move_click(move_from), gs.convert_move_click(move_to))
                        first_move = False

        # Updates screen and board based on user selection
        draw_xiangqi_game(screen, gs, move_try[0], move_try[1], first_move,
                          valid_move)
        pygame.display.update()  # display is updated


if __name__ == '__main__':
    main()
