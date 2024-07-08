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

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    mouse = pg.mouse.get_pos()
    mouse_position_x = mouse[0]
    mouse_position_y = mouse[1]

    click = pg.mouse.get_pressed()

    if click[0] == 1:
        click_last_status = 1
    else: 
        click_last_status = 0
    pg.display.update()

