import pygame as pg
import math 

# cores do jogo
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 250)
cinza = (150, 150, 150)

# setup da tela de jogo
pg.init()
window = pg.display.set_mode((1000, 600))
window.fill(branco)

# inicializando a fonte 
pg.font.init()

# Escolhendo uma fonte e tamanho
fonte = pg.font.SysFont("Comic Sans MS", 30)
board_array = [['n', 'n', 'n'],
               ['n', 'n', 'n'],
               ['n', 'n', 'n']]

# Variáveis de clique
click_last_status = 0
click_on_off = 0
click_position_x = -1
click_position_y = -1

X_or_O_turn = 'x'
end_game = 0

def boardGrid(window):
    pg.draw.line(window, preto, (200, 10), (200, 570), 10)
    pg.draw.line(window, preto, (400, 10), (400, 570), 10)
    pg.draw.line(window, preto, (10, 200), (570, 200), 10)
    pg.draw.line(window, preto, (10, 400), (570, 400), 10)

def clickLogic(click_on_off, click_last_status, x, y):
    if click[0] == 0 and click_last_status == 1:
        x = (math.ceil(mouse[0] / 200) - 1)
        y = (math.ceil(mouse[1] / 200) - 1)
    elif click[0] == 0 and click_last_status == 0:
        click_on_off = 0 
        x = -1
        y = -1
    return click_on_off, click_last_status, x, y

def drawSelectedCell(window, board_array):
    for y in range(3):
        for x in range(3):
            if board_array[y][x] == 'x':
                jogador_X(window, x, y)
            elif board_array[y][x] == 'o':
                jogador_O(window, x, y)

def boardArrayData(board_array, X_or_O_turn, end_game, x, y):
    if x < 3 and y < 3:
        if X_or_O_turn == 'x' and board_array[y][x] == 'n' and x != -1 and y != -1 and end_game == 0:
            board_array[y][x] = 'x'
            X_or_O_turn = 'o'
        elif X_or_O_turn == 'o' and board_array[y][x] == 'n' and x != -1 and y != -1 and end_game == 0:
            board_array[y][x] = 'o'
            X_or_O_turn = 'x'
    return board_array, X_or_O_turn

def winLine(window, board_array, end_game, X_or_O_turn):
    win_pos = []

    if board_array[0][0] == board_array[0][1] == board_array[0][2] != 'n':
        win_pos = [(0, 0), (0, 2)]
    elif board_array[1][0] == board_array[1][1] == board_array[1][2] != 'n':
        win_pos = [(1, 0), (1, 2)]
    elif board_array[2][0] == board_array[2][1] == board_array[2][2] != 'n':
        win_pos = [(2, 0), (2, 2)]
    elif board_array[0][0] == board_array[1][0] == board_array[2][0] != 'n':
        win_pos = [(0, 0), (2, 0)]
    elif board_array[0][1] == board_array[1][1] == board_array[2][1] != 'n':
        win_pos = [(0, 1), (2, 1)]
    elif board_array[0][2] == board_array[1][2] == board_array[2][2] != 'n':
        win_pos = [(0, 2), (2, 2)]
    elif board_array[0][0] == board_array[1][1] == board_array[2][2] != 'n':
        win_pos = [(0, 0), (2, 2)]
    elif board_array[2][0] == board_array[1][1] == board_array[0][2] != 'n':
        win_pos = [(2, 0), (0, 2)]

    if win_pos:
        start = (win_pos[0][1] * 200 + 20, win_pos[0][0] * 200 + 100)
        end = (win_pos[1][1] * 200 + 180, win_pos[1][0] * 200 + 100)
        if win_pos[0][0] == win_pos[1][0]:  # horizontal line
            start = (win_pos[0][1] * 200 + 20, win_pos[0][0] * 200 + 100)
            end = (win_pos[1][1] * 200 + 180, win_pos[1][0] * 200 + 100)
        elif win_pos[0][1] == win_pos[1][1]:  # vertical line
            start = (win_pos[0][1] * 200 + 100, win_pos[0][0] * 200 + 20)
            end = (win_pos[1][1] * 200 + 100, win_pos[1][0] * 200 + 180)
        elif win_pos == [(0, 0), (2, 2)]:  # diagonal from top-left to bottom-right
            start = (win_pos[0][1] * 200 + 20, win_pos[0][0] * 200 + 20)
            end = (win_pos[1][1] * 200 + 180, win_pos[1][0] * 200 + 180)
        elif win_pos == [(2, 0), (0, 2)]:  # diagonal from bottom-left to top-right
            start = (win_pos[0][1] * 200 + 20, win_pos[0][0] * 200 + 180)
            end = (win_pos[1][1] * 200 + 180, win_pos[1][0] * 200 + 20)
        
        pg.draw.line(window, verde, start, end, 10)
        end_game = 1

    return end_game, X_or_O_turn

def restartButton(window):
    pg.draw.rect(window, cinza, (700, 470, 200, 65))
    texto = fonte.render('Restart', 1, preto)
    window.blit(texto, (750, 480))

def restartGame(board_array, x, y, end_game):
    if x >= 700 and x <= 900 and y >= 470 and y <= 535:  # Corrigindo a posição do botão
        board_array = [['n', 'n', 'n'],
                       ['n', 'n', 'n'],
                       ['n', 'n', 'n']]
        end_game = 0
    return board_array, end_game

def gameStatus(board_array, X_or_O_turn, end_game):
    count = sum(row.count('n') for row in board_array)
    if count == 0:
        end_game = 1
    return board_array, end_game

def jogador_X(window, x, y):
    pg.draw.line(window, vermelho, ((x * 200) + 30, (y * 200) + 30), ((x * 200) + 170, (y * 200) + 170), 10)
    pg.draw.line(window, vermelho, ((x * 200) + 30, (y * 200) + 170), ((x * 200) + 170, (y * 200) + 30), 10)

def jogador_O(window, x, y):
    pg.draw.circle(window, azul, ((x * 200) + 100, (y * 200) + 100), 75, 10)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    mouse = pg.mouse.get_pos()
    mouse_position_x = mouse[0]
    mouse_position_y = mouse[1]

    click = pg.mouse.get_pressed()

    window.fill(branco)  # Redesenhar o fundo para apagar os desenhos anteriores
    boardGrid(window)
    click_on_off, click_last_status, click_position_x, click_position_y = clickLogic(click_on_off, click_last_status, click_position_x, click_position_y)
    board_array, X_or_O_turn = boardArrayData(board_array, X_or_O_turn, end_game, click_position_x, click_position_y) 
    end_game, X_or_O_turn = winLine(window, board_array, end_game, X_or_O_turn)
    drawSelectedCell(window, board_array)
    restartButton(window)
    if click[0] == 1 and end_game == 1:
        board_array, end_game = restartGame(board_array, mouse_position_x, mouse_position_y, end_game)
    board_array, end_game = gameStatus(board_array, X_or_O_turn, end_game)

    if click[0] == 1:
        click_last_status = 1
    else: 
        click_last_status = 0
    pg.display.update()
