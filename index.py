import pygame as pg
import math

# Cores do jogo
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 250)
cinza = (150, 150, 150)

class JogoDaVelha:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.window = pg.display.set_mode((1000, 600))
        self.fonte = pg.font.SysFont("Comic Sans MS", 30)
        self.clock = pg.time.Clock()
        self.running = True
        self.state = 'inicio'
        self.reset_game()

#Reinicia o jogo
    def reset_game(self):
        self.board_array = [['n', 'n', 'n'],
                            ['n', 'n', 'n'],
                            ['n', 'n', 'n']]
        self.click_last_status = 0
        self.click_on_off = 0
        self.click_position_x = -1
        self.click_position_y = -1
        self.X_or_O_turn = 'x'
        self.end_game = 0

    def run(self):
        while self.running:
            if self.state == 'inicio':
                self.tela_inicio()
            elif self.state == 'jogo':
                self.tela_jogo()
            elif self.state == 'reiniciar':
                self.reset_game()
                self.state = 'jogo'
            self.clock.tick(60)
        pg.quit()
    
    def tela_inicio(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.state = 'jogo'

        self.window.fill(branco)
        texto = self.fonte.render('Jogo da velha', 1, preto)
        self.window.blit(texto, (390, 50))
        pg.draw.rect(self.window, verde, (390, 470, 200, 65))
        texto = self.fonte.render('Jogar', 1, preto)
        self.window.blit(texto, (390, 480))
        pg.display.update()

    def tela_jogo(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        mouse = pg.mouse.get_pos()
        mouse_position_x = mouse[0]
        mouse_position_y = mouse[1]

        click = pg.mouse.get_pressed()

        self.window.fill(branco)  # Redesenhar o fundo para apagar os desenhos anteriores
        self.boardGrid()
        self.click_on_off, self.click_last_status, self.click_position_x, self.click_position_y = self.clickLogic(self.click_on_off, self.click_last_status, self.click_position_x, self.click_position_y)
        self.board_array, self.X_or_O_turn = self.boardArrayData(self.board_array, self.X_or_O_turn, self.end_game, self.click_position_x, self.click_position_y) 
        self.end_game, self.X_or_O_turn = self.winLine(self.board_array, self.end_game, self.X_or_O_turn)
        self.drawSelectedCell()
        self.restartButton()
        if click[0] == 1 and self.end_game == 1:
            self.board_array, self.end_game = self.restartGame(self.board_array, mouse_position_x, mouse_position_y, self.end_game)
        self.board_array, self.end_game = self.gameStatus(self.board_array, self.X_or_O_turn, self.end_game)

        if click[0] == 1:
            self.click_last_status = 1
        else: 
            self.click_last_status = 0
        pg.display.update()

    def boardGrid(self):
        pg.draw.line(self.window, preto, (200, 10), (200, 570), 10)
        pg.draw.line(self.window, preto, (400, 10), (400, 570), 10)
        pg.draw.line(self.window, preto, (10, 200), (570, 200), 10)
        pg.draw.line(self.window, preto, (10, 400), (570, 400), 10)

    def clickLogic(self, click_on_off, click_last_status, x, y):
        if pg.mouse.get_pressed()[0] == 0 and click_last_status == 1:
            x = (math.ceil(pg.mouse.get_pos()[0] / 200) - 1)
            y = (math.ceil(pg.mouse.get_pos()[1] / 200) - 1)
        elif pg.mouse.get_pressed()[0] == 0 and click_last_status == 0:
            click_on_off = 0 
            x = -1
            y = -1
        return click_on_off, click_last_status, x, y

    def drawSelectedCell(self):
        for y in range(3):
            for x in range(3):
                if self.board_array[y][x] == 'x':
                    self.jogador_X(x, y)
                elif self.board_array[y][x] == 'o':
                    self.jogador_O(x, y)

    def boardArrayData(self, board_array, X_or_O_turn, end_game, x, y):
        if x < 3 and y < 3:
            if X_or_O_turn == 'x' and board_array[y][x] == 'n' and x != -1 and y != -1 and end_game == 0:
                board_array[y][x] = 'x'
                X_or_O_turn = 'o'
            elif X_or_O_turn == 'o' and board_array[y][x] == 'n' and x != -1 and y != -1 and end_game == 0:
                board_array[y][x] = 'o'
                X_or_O_turn = 'x'
        return board_array, X_or_O_turn

    def winLine(self, board_array, end_game, X_or_O_turn):
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
            
            pg.draw.line(self.window, verde, start, end, 10)
            end_game = 1

        return end_game, X_or_O_turn

    def restartButton(self):
        pg.draw.rect(self.window, cinza, (700, 470, 200, 65))
        texto = self.fonte.render('Restart', 1, preto)
        self.window.blit(texto, (750, 480))

    def restartGame(self, board_array, x, y, end_game):
        if x >= 700 and x <= 900 and y >= 470 and y <= 535:
            board_array = [['n', 'n', 'n'],
                           ['n', 'n', 'n'],
                           ['n', 'n', 'n']]
            end_game = 0
        return board_array, end_game

    def gameStatus(self, board_array, X_or_O_turn, end_game):
        count = sum(row.count('n') for row in board_array)
        if count == 0:
            end_game = 1
        return board_array, end_game

    def jogador_X(self, x, y):
        pg.draw.line(self.window, vermelho, ((x * 200) + 30, (y * 200) + 30), ((x * 200) + 170, (y * 200) + 170), 10)
        pg.draw.line(self.window, vermelho, ((x * 200) + 30, (y * 200) + 170), ((x * 200) + 170, (y * 200) + 30), 10)

    def jogador_O(self, x, y):
        pg.draw.circle(self.window, azul, ((x * 200) + 100, (y * 200) + 100), 75, 10)

if __name__ == "__main__":
    JogoDaVelha().run()
