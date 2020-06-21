# Author: 
# Date: 
# Description:


import pygame
from XiangqiGame import XiangqiGame

pygame.font.init()
WIDTH = 1200
HEIGHT = 1200
DIMENSION_HEIGHT = 10
DIMENSION_WIDTH = 9
SQ_SIZE_Height = 1000 // 10
SQ_SIZE_Width = 1000 // 10
MAX_FPS = 15
IMAGES = {}
font = pygame.font.Font("freesansbold.ttf", 30)
title_font = pygame.font.Font("freesansbold.ttf", 95)
print(pygame.font.get_fonts())

icon = pygame.image.load("Pieces/xiangqi.png")
pygame.display.set_icon(icon)

def loadImages():
    pieces = ["black_advisor", "black_cannon", "black_chariot", "black_elephant", "black_general", "black_horse",
              "red_advisor", "red_chariot", "red_elephant", "red_general", "red_horse", "red_soldier", "red_cannon",
              "black_soldier"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Pieces/" + piece + ".png"), (SQ_SIZE_Width, SQ_SIZE_Height))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Xiangqi")
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("#654321"))
    gs = XiangqiGame()
    loadImages()
    move_to = []
    move_from = []
    move_try = [100, 100]
    click_num = 0
    running = True
    first_move = False
    valid_move = False
    while running:
        # background image
        screen.blit(screen, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if location[0] < 100 or location[0] > 1100 or location[1] > 1100 or location[1] < 100:
                    print(False)
                else:
                    col = ((location[0]-49)//100) - 1
                    if col == 9:
                        col = 8
                    row = (location[1]//100) - 1
                    if click_num == 0:
                        move_from = [row, col]
                        click_num += 1
                        move_try = [row, col]
                        first_move = True
                        valid_move = False
                    elif click_num == 1:
                        move_to = [row, col]
                        click_num = 0
                        move_try = [row, col]
                        valid_move = gs.make_move(gs.convert_move_click(move_from), gs.convert_move_click(move_to))
                        print(valid_move)
                        first_move = False
        drawXiangqiGame(screen, gs, move_try[0], move_try[1], first_move, valid_move)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawXiangqiGame(screen, gs, row, col, move_from, move_to):
    screen.fill(pygame.Color("#654321"))
    drawboard(screen, row, col, move_from, move_to)
    drawpieces(screen, gs._board)
    show_active_player(screen, gs.get_active_player())
    show_game_state(screen, gs.get_game_state())
    show_in_check(screen, gs.get_in_check())
    show_title(screen)

def drawboard(screen, row, col, move_from, move_to):
    count_row = 0
    count_col = 0
    colors = [pygame.Color("#d5a667"), pygame.Color(0, 0, 0)]
    for x in range(DIMENSION_HEIGHT):
        for y in range(DIMENSION_WIDTH):
            if move_to and x == row and y == col:
                pygame.draw.rect(screen, pygame.Color(23, 235, 0),
                                 pygame.Rect(y * SQ_SIZE_Width + 150, x * SQ_SIZE_Height + 100, SQ_SIZE_Width,
                                             SQ_SIZE_Height))
            elif not move_to and not move_from and x == row and y == col:
                pygame.draw.rect(screen, pygame.Color(255, 10, 10),
                                 pygame.Rect(y * SQ_SIZE_Width + 150, x * SQ_SIZE_Height + 100, SQ_SIZE_Width,
                                             SQ_SIZE_Height))
            elif move_from and not move_to and x == row and y == col:
                pygame.draw.rect(screen, pygame.Color(255, 255, 0),
                                 pygame.Rect(y * SQ_SIZE_Width + 150, x * SQ_SIZE_Height + 100, SQ_SIZE_Width,
                                             SQ_SIZE_Height))
            else:
                color = colors[((x + y) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(y*SQ_SIZE_Width+150, x*SQ_SIZE_Height+100, SQ_SIZE_Width, SQ_SIZE_Height))
                count_row += 1
                count_col += 1


def drawpieces(screen, board):
    for x in range(DIMENSION_HEIGHT):
        for y in range(DIMENSION_WIDTH):
            piece = board[x][y]
            if piece != "":
                screen.blit(IMAGES[piece], pygame.Rect(y*SQ_SIZE_Width+150, x*SQ_SIZE_Height+100, SQ_SIZE_Width, SQ_SIZE_Height))

def show_active_player(screen, player):
    active_player = font.render("Active Player: " + str(player), True, (255, 255, 255))
    screen.blit(active_player, (10, 1133))

def show_game_state(screen, game_state):
    active_player = font.render("Game State: " + str(game_state), True, (255, 255, 255))
    screen.blit(active_player, (440, 1133))

def show_in_check(screen, in_check):
    in_check = font.render("In Check: " + str(in_check), True, (255, 255, 255))
    screen.blit(in_check, (850, 1133))

def show_title(screen):
    active_player = title_font.render("Xiangqi", True, (255, 255, 255))
    screen.blit(active_player, (420, 0))

if __name__ == '__main__':
    main()
