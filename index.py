import pygame as pg
import random

# Cores do jogo
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 250)
cinza = (150, 150, 150)
ciano = (0, 255, 255)
dourado = (255, 215, 0)
turquesa = (0, 206, 209)

class TelaInicial:
    def __init__(self, window, fonte):
        self.window = window
        self.fonte = fonte
        self.running = True
        self.state = 'inicio'
        self.fonte_titulo = pg.font.Font("./Assets/AlfaSlabOne-Regular.ttf", 70)
        self.imagem_robot = pg.image.load("./Assets/robot.png")
        self.imagem_idosa = pg.image.load("./Assets/idosas.png")

    def exibir(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if 220 <= x <= 410 and 300 <= y <= 490:
                    self.state = 'game_vs_robot'
                elif 580 <= x <= 770 and 300 <= y <= 490:
                    self.state = 'game_vs_human'

        self.window.fill(ciano)
        texto = self.fonte_titulo.render('Jogo da', 1, dourado)
        texto2 = self.fonte_titulo.render('Velha#', 1, vermelho)
        self.window.blit(texto, (330, 50))
        self.window.blit(texto2, (350, 105))
        pg.draw.rect(self.window, verde, (220, 300, 190, 190))
        pg.draw.rect(self.window, verde, (580, 300, 180, 190))
        texto = self.fonte.render('VS Robo', 1, preto)
        texto2 = self.fonte.render('1 VS 1', 1, preto)
        self.window.blit(texto, (255, 495))
        self.window.blit(texto2, (630, 495))
        self.window.blit(self.imagem_robot, (220, 300))
        self.window.blit(self.imagem_idosa, (520, 290))
        pg.display.update()

class GameBase:
    def __init__(self, window, fonte):
        self.window = window
        self.fonte = fonte
        self.fonte_Logo = pg.font.Font("./Assets/AlfaSlabOne-Regular.ttf",25)
        self.count_X_wins = 0
        self.count_O_wins = 0
        self.count_Empates = 0
        self.resetGame()

    def resetGame(self):
        self.board_array = [['n', 'n', 'n'],
                            ['n', 'n', 'n'],
                            ['n', 'n', 'n']]
        self.X_or_O_turn = 'x'
        self.end_game = False
        self.winning_line = None

    def boardGrid(self):
        pg.draw.line(self.window, preto, (200, 10), (200, 570), 10)
        pg.draw.line(self.window, preto, (400, 10), (400, 570), 10)
        pg.draw.line(self.window, preto, (10, 200), (570, 200), 10)
        pg.draw.line(self.window, preto, (10, 400), (570, 400), 10)

    def clickLogic(self, pos):
        if self.end_game:
            return

        x = pos[0] // 200
        y = pos[1] // 200

        if 0 <= x < 3 and 0 <= y < 3:
            if self.board_array[y][x] == 'n':
                self.board_array[y][x] = self.X_or_O_turn
                self.checkWin()
                self.X_or_O_turn = 'o' if self.X_or_O_turn == 'x' else 'x'

    def drawSelectedCell(self):
        for y in range(3):
            for x in range(3):
                if self.board_array[y][x] == 'x':
                    self.jogador_X(x, y)
                elif self.board_array[y][x] == 'o':
                    self.jogador_O(x, y)

    def checkWin(self):
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)]
        ]

        for line in lines:
            if self.board_array[line[0][0]][line[0][1]] == self.board_array[line[1][0]][line[1][1]] == self.board_array[line[2][0]][line[2][1]] != 'n':
                self.winning_line = (line[0], line[2])
                self.end_game = True
                if self.board_array[line[0][0]][line[0][1]] == 'x':
                    self.count_X_wins += 1
                else:
                    self.count_O_wins += 1
                return

        if all(cell != 'n' for row in self.board_array for cell in row):
            self.end_game = True
            self.count_Empates += 1

    def drawWinningLine(self):
        if self.winning_line:
            start_x = self.winning_line[0][1] * 200 + 100
            start_y = self.winning_line[0][0] * 200 + 100
            end_x = self.winning_line[1][1] * 200 + 100
            end_y = self.winning_line[1][0] * 200 + 100

            if self.winning_line[0][0] == self.winning_line[1][0]:  # horizontal line
                start_x = self.winning_line[0][1] * 200 + 20
                end_x = self.winning_line[1][1] * 200 + 180
            elif self.winning_line[0][1] == self.winning_line[1][1]:  # vertical line
                start_y = self.winning_line[0][0] * 200 + 20
                end_y = self.winning_line[1][0] * 200 + 180
            elif self.winning_line == [(0, 0), (2, 2)]:  # diagonal from top-left to bottom-right
                start_x = self.winning_line[0][1] * 200 + 20
                start_y = self.winning_line[0][0] * 200 + 20
                end_x = self.winning_line[1][1] * 200 + 180
                end_y = self.winning_line[1][0] * 200 + 180
            elif self.winning_line == [(2, 0), (0, 2)]:  # diagonal from bottom-left to top-right
                start_x = self.winning_line[0][1] * 200 + 20
                start_y = self.winning_line[0][0] * 200 + 180
                end_x = self.winning_line[1][1] * 200 + 180
                end_y = self.winning_line[1][0] * 200 + 20

            pg.draw.line(self.window, verde, (start_x, start_y), (end_x, end_y), 10)

    def restartButton(self):
        pg.draw.rect(self.window, cinza, (700, 470, 200, 55))
        texto = self.fonte.render('Restart', 1, preto)
        self.window.blit(texto, (750, 480))

    def restartGame(self, pos):
        if 700 <= pos[0] <= 900 and 470 <= pos[1] <= 535:
            self.resetGame()

    def drawCounters(self):
        logo = self.fonte_Logo.render("Jogo da", 1, dourado)
        logo2 = self.fonte_Logo.render("Velha#", 1, vermelho)
        self.window.blit(logo, (880, 25))
        self.window.blit(logo2, (890, 45))
        texto_X = self.fonte.render(f'Vitórias X: {self.count_X_wins}', 1, vermelho)
        texto_O = self.fonte.render(f'Vitórias O: {self.count_O_wins}', 1, azul)
        texto_empate = self.fonte.render(f'Empates: {self.count_Empates}', 1, preto)
        self.window.blit(texto_X, (620, 350))
        self.window.blit(texto_O, (820, 350))
        self.window.blit(texto_empate, (720, 400))

    def drawResult(self):
        texto_X = self.fonte.render(f'Vitória!', 2, vermelho)
        texto_O = self.fonte.render(f'Vitória!', 2, azul)
        if self.end_game:
            if self.winning_line:
                if self.board_array[self.winning_line[0][0]][self.winning_line[0][1]] == 'x':
                    self.window.blit(texto_X, (740, 200))
                else:
                    self.window.blit(texto_O, (740, 200))
            else:
                texto_empate = self.fonte.render('Empate!', 1, preto)
                self.window.blit(texto_empate, (740, 200))

    def jogador_X(self, x, y):
        pg.draw.line(self.window, vermelho, ((x * 200) + 30, (y * 200) + 30), ((x * 200) + 170, (y * 200) + 170), 10)
        pg.draw.line(self.window, vermelho, ((x * 200) + 30, (y * 200) + 170), ((x * 200) + 170, (y * 200) + 30), 10)

    def jogador_O(self, x, y):
        pg.draw.circle(self.window, azul, ((x * 200) + 100, (y * 200) + 100), 75, 10)

class GameVsHuman(GameBase):
    def __init__(self, window, fonte):
        super().__init__(window, fonte)

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    self.clickLogic(pos)
                    self.restartGame(pos)

            self.window.fill(turquesa)
            self.boardGrid()
            self.drawSelectedCell()
            self.drawWinningLine()
            self.drawCounters()
            self.drawResult()
            self.restartButton()
            pg.display.update()

class GameVSRobot(GameBase):
    def __init__(self, window, fonte):
        super().__init__(window, fonte)
        self.count_player_wins = 0
        self.count_robot_wins = 0
        self.count_draws = 0

    def robotMove(self):
        if self.end_game:
            return

        empty_cells = [(y, x) for y in range(3) for x in range(3) if self.board_array[y][x] == 'n']
        if empty_cells:
            move = random.choice(empty_cells)
            self.board_array[move[0]][move[1]] = self.X_or_O_turn
            self.checkWin()
            self.X_or_O_turn = 'o' if self.X_or_O_turn == 'x' else 'x'

    def checkWin(self):
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)]
        ]

        for line in lines:
            if self.board_array[line[0][0]][line[0][1]] == self.board_array[line[1][0]][line[1][1]] == \
                    self.board_array[line[2][0]][line[2][1]] != 'n':
                self.winning_line = (line[0], line[2])
                self.end_game = True
                winner = self.board_array[line[0][0]][line[0][1]]
                if winner == 'x':
                    self.count_player_wins += 1
                elif winner == 'o':
                    self.count_robot_wins += 1
                return

        if all(cell != 'n' for row in self.board_array for cell in row):
            self.end_game = True
            self.count_draws += 1

    def drawCountersBot(self):
        logo = self.fonte_Logo.render("Jogo da", 1, dourado)
        logo2 = self.fonte_Logo.render("Velha#", 1, vermelho)
        self.window.blit(logo, (880, 25))
        self.window.blit(logo2, (890, 45))

        text_player = self.fonte.render(f'Jogador: {self.count_player_wins}', 1, vermelho)
        text_robot = self.fonte.render(f'Robô: {self.count_robot_wins}', 1, azul)
        text_draws = self.fonte.render(f'Empates: {self.count_draws}', 1, preto)
        self.window.blit(text_player, (620, 350))
        self.window.blit(text_robot, (820, 350))
        self.window.blit(text_draws, (720, 400))

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    self.clickLogic(pos)
                    self.restartGame(pos)
                    if not self.end_game:
                        self.robotMove()

            self.window.fill(turquesa)
            self.boardGrid()
            self.drawSelectedCell()
            self.drawWinningLine()
            self.drawCountersBot()
            self.drawResult()
            self.restartButton()
            pg.display.update()


class JogoDaVelha:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((1000, 600))
        pg.display.set_caption('Jogo da Velha')
        self.fonte = pg.font.Font("./Assets/Ubuntu-Medium.ttf", 30)

    def run(self):
        tela_inicial = TelaInicial(self.window, self.fonte)
        game_vs_human = GameVsHuman(self.window, self.fonte)
        game_vs_robot = GameVSRobot(self.window, self.fonte)

        while tela_inicial.running:
            if tela_inicial.state == 'inicio':
                tela_inicial.exibir()
            elif tela_inicial.state == 'game_vs_human':
                game_vs_human.run()
                tela_inicial.state = 'inicio'
            elif tela_inicial.state == 'game_vs_robot':
                game_vs_robot.run()
                tela_inicial.state = 'inicio'

if __name__ == "__main__":
    JogoDaVelha().run()