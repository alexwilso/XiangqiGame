# Author: 
# Date: 
# Description:


import pygame
from XiangqiGame import XiangqiGame

WIDTH = 1200
HEIGHT = 1200
DIMENSION_HEIGHT = 10
DIMENSION_WIDTH = 9
SQ_SIZE_Height = 1000 // 10
SQ_SIZE_Width = 1000 // 10
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["black_advisor", "black_cannon", "black_chariot", "black_elephant", "black_general", "black_horse",
              "red_advisor", "red_chariot", "red_elephant", "red_general", "red_horse", "red_soldier", "red_cannon",
              "black_soldier"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Pieces/" + piece + ".png"), (SQ_SIZE_Width, SQ_SIZE_Height))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("#654321"))
    gs = XiangqiGame()
    loadImages()
    move_to = []
    move_from = []
    click_num = 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if location[0] < 100 or location[0] > 1100 or location[1] > 1100 or location[1] < 100:
                    print(False)
                else:
                    print(location)
                    col = (location[0]//150) - 1
                    row = (location[1]//100) - 1
                    print(row)
                    print(col)
                    if click_num == 0:
                        move_from = [row, col]
                        print(gs.convert_move_click(move_from))
                        click_num += 1
                    elif click_num == 1:
                        move_to = [row, col]
                        print(gs.convert_move_click(move_to))
                        click_num = 0
                        print(gs.make_move(gs.convert_move_click(move_from), gs.convert_move_click(move_to)))
        drawXiangqiGame(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawXiangqiGame(screen, gs):
    drawboard(screen)
    drawpieces(screen, gs._board)

def drawboard(screen):
    colors = [pygame.Color("#d5a667"), pygame.Color(0, 0, 0)]
    for x in range(DIMENSION_HEIGHT):
        for y in range(DIMENSION_WIDTH):
            color = colors[((x + y) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(y*SQ_SIZE_Width+150, x*SQ_SIZE_Height+100, SQ_SIZE_Width, SQ_SIZE_Height))


def drawpieces(screen, board):
    for x in range(DIMENSION_HEIGHT):
        for y in range(DIMENSION_WIDTH):
            piece = board[x][y]
            if piece != "":
                screen.blit(IMAGES[piece], pygame.Rect(y*SQ_SIZE_Width+150, x*SQ_SIZE_Height+100, SQ_SIZE_Width, SQ_SIZE_Height))

def show_active_player(screen):
    pass

if __name__ == '__main__':
    main()
