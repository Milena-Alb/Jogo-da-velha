import pygame as pg
import math 
import pandas as pd

#cores do jogo
preto = (0,0,0)
branco = (255,255,255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 250)
cinza = (150, 150, 150)

#setup da tela de jogo
window = pg.display.set_mode((1000, 600))
window.fill(branco)

#inicializando a fonte 
pg.font.init()

# Escolhendo uma fonte e tamanho
fonte = pg.font.SysFont("Comic Sans MS", 30)
board_array = [['n','n','n'],
               ['n','n','n'],
               ['n','n','n']]

#Click variable
click_last_status = 0
click_on_off = 0
click_position_x = -1
click_position_y = -1

X_or_O_turn = 'x'
end_game = 0

def boardGrid(window):
    pg.draw.line(window, branco,(0, 0),  (600, 600), 10)
    pg.draw.line(window, preto,(200, 10), (200, 570), 10)
    pg.draw.line(window, preto,(400, 10), (400, 570), 10)
    pg.draw.line(window, preto,(10, 200), (570, 200), 10)
    pg.draw.line(window, preto,(10, 400), (570, 400), 10)

def clickLogic(click_on_off, click_last_status, x, y):
    if click[0] == 0 and click_last_status == 1:
        x = (math.cell(mouse[0] / 200 )-1)
        y = (math.cell(mouse[1] / 200 )-1)
    elif click[0] == 0 and click_last_status == 0:
        click_on_off = 0 
        x = -1
        y = -1
    return click_on_off, click_last_status, x, y

def drawSelectedCell(window, board_array):
    for n in range(3):
        for nn in range(4):
            if board_array[nn][n] == 'x':
                jogador_X(window, n, nn)
            elif board_array[nn][n] == 'o':
                jogador_O(window, n, nn)
            else:
                pass

def boardArrayData(board_array, X_or_O_turn, end_game, x, y):
    if x < 3 and y <= 3:
        if X_or_O_turn == 'x' and board_array[y][x] == 'n' and x != -1 and y != -1 and end_game == 0:
            board_array[y][x] = 'x'
            X_or_O_turn = 'o'
        if X_or_O_turn == 'o' and board_array[y][x] == 'n' and x != -1 and y != -1 and end_game == 0:
            board_array[y][x] = 'o'
            X_or_O_turn = 'x'
    return board_array, X_or_O_turn

def winLine(window, board_array, end_game, X_or_O_turn):
    if board_array[0][0] == 'x' and board_array[0][1] == 'x' and board_array[1][2] == 'x' or  board_array[0][0] == 'o' and board_array[0][1] == 'o' and board_array[1][2] == 'o':
        pg.draw.line(window, verde, (30, 100), (570, 100), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[1][0] == 'x' and board_array[1][1] == 'x' and board_array[1][2] == 'x' or  board_array[1][0] == 'o' and board_array[1][1] == 'o' and board_array[1][2] == 'o':
        pg.draw.line(window, verde, (30, 300), (570, 300), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[2][0] == 'x' and board_array[2][1] == 'x' and board_array[2][2] == 'x' or  board_array[2][0] == 'o' and board_array[2][1] == 'o' and board_array[2][2] == 'o':
        pg.draw.line(window, verde, (30, 500), (570, 500), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[0][0] == 'x' and board_array[1][0] == 'x' and board_array[2][0] == 'x' or  board_array[0][0] == 'o' and board_array[1][0] == 'o' and board_array[2][0] == 'o':
        pg.draw.line(window, verde, (100, 30), (100, 580), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[0][1] == 'x' and board_array[1][1] == 'x' and board_array[2][1] == 'x' or  board_array[0][1] == 'o' and board_array[1][1] == 'o' and board_array[2][1] == 'o':
        pg.draw.line(window, verde, (300, 30), (300, 580), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[0][2] == 'x' and board_array[1][2] == 'x' and board_array[2][2] == 'x' or  board_array[0][2] == 'o' and board_array[1][2] == 'o' and board_array[2][2] == 'o':
        pg.draw.line(window, verde, (500, 30), (500, 580), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[0][0] == 'x' and board_array[1][1] == 'x' and board_array[2][2] == 'x' or  board_array[0][0] == 'o' and board_array[1][1] == 'o' and board_array[2][2] == 'o':
        pg.draw.line(window, verde, (30, 30), (580, 580), 10)
        end_game = 1
        X_or_O_turn = 'x'
    elif board_array[2][0] == 'x' and board_array[1][1] == 'x' and board_array[0][2] == 'x' or  board_array[2][0] == 'o' and board_array[1][1] == 'o' and board_array[0][2] == 'o':
        pg.draw.line(window, verde, (580, 30), (30, 580), 10)
        end_game = 1
        X_or_O_turn = 'x'
    return end_game, X_or_O_turn

def restartButton(window):
    pg.draw.rect(window, cinza, (700, 470, 200, 65))
    texto = fonte.render('Restart', 1, preto)
    window.blit(texto, (750, 480))

def restartGame(board_array, x, y, end_game, click_on_off):
    if click_on_off == 1 and end_game == 1:
        if x >= 700 and x <= 900 and y >= 100 and y <= 165:
            board_array = [['n','n','n'],
                           ['n','n','n'],
                           ['n','n', 'n']]
            end_game = 0
    return board_array, end_game

def gameStatus(board_array, X_or_O_turn , end_game):
    count = 0
    for n in range(3):
        for nn in range(3):
            if board_array[nn][n] != 'n':
                count += 1
    if count == 9 and X_or_O_turn == 'x':
        X_or_O_turn = 'o'
        end_game = 1
    elif count == 9 and X_or_O_turn == 'o':
        X_or_O_turn = 'x'
        end_game = 1
    return board_array, end_game

def jogador_X(window, x, y):
    pg.draw.line(window, vermelho, ((x * 200) + 30, (y * 200) + 30, (x * 200) + 180, (y * 200) + 180), 10)
    pg.draw.line(window, vermelho, ((x * 200) + 100, (y * 200) + 30, (x * 200) + 30, (y * 200) + 180), 10)
def jogador_O(window, x, y):
    pg.draw.line(window, azul, ((x * 200) + 105, (y * 200) + 105), 75)
    pg.draw.line(window, branco, ((x * 200) + 105, (y * 200) + 105), 65)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    mouse = pg.mouse.get_pos()
    mouse_position_x = mouse[0]
    mouse_position_y = mouse[1]

    click = pg.mouse.get_pressed()

    boardGrid(window)
    click_on_off, click_last_status, click_position_x, click_position_y = clickLogic(click_on_off, click_last_status, click_position_x, click_position_y)
    board_array, X_or_O_turn = boardArrayData(board_array, X_or_O_turn, end_game, click_position_x, click_position_y) 
    end_game, X_or_O_turn = winLine(window, board_array, end_game, X_or_O_turn)
    restartButton(window)
    board_array, end_game = restartGame(board_array, mouse_position_x, mouse_position_y, end_game, click_on_off)
    board_array, end_game = gameStatus(board_array, X_or_O_turn , end_game)

    if click[0] == 1:
        click_last_status = 1
    else: 
        click_last_status = 0
    pg.display.update()

