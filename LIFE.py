import pygame
import random
pygame.init()
screen = pygame.display.set_mode((140, 140))
class Board:
    # создание поля
    def __init__(self, width, height):
        width += 2
        height += 2
        self.width = width#высота
        self.height = height  #ширина
        self.board = [[0] * width for _ in range(height)]
        self.boardnext = [[0] * width for _ in range(height)]
        self.left = 10 #отступ слева
        self.top = 10 #отступ сверху
        self.cell_size = 10 #размер клетки

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        self.boardnext = [[0] * self.width for _ in range(self.height)]
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                if self.board[j][i] == 0:
                    pygame.draw.rect(screen, pygame.Color('white'), (self.top + i * self.cell_size, self.left + self.cell_size* j, self.cell_size, self.cell_size), 1)
                elif self.board[j][i] == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), (self.top + i * self.cell_size, self.left + self.cell_size* j, self.cell_size, self.cell_size))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        if cell_coords != None:
            x, y = cell_coords
            for i in range(self.width):
                for j in range(self.height):
                    if i == x and j == y:
                        if self.board[j][i] == 0:
                            self.board[j][i] = 1
                        elif self.board[j][i] == 1:
                            self.board[j][i] = 0
                            
    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x > self.width * self.cell_size + self.left or y > self.height * self.cell_size + self.top:
            return(None)
        if x < self.left or y < self.top:
            return(None)
        x -= self.left
        y -= self.top
        x = (x - 1) // self.cell_size
        y = (y - 1) // self.cell_size
        return(x, y)
class Life(Board):
    def next_move(self):
        #for i in range(1,self.width - 1):
        for i in range(self.width - 2, 0, -1):
            for j in range(1, self.height - 1):
                m = 0
                #m += self.board[j][i]                   
                m += self.board[j][i + 1]
                m += self.board[j][i - 1]
                m += self.board[j - 1][i]
                m += self.board[j - 1][i + 1]
                m += self.board[j - 1][i - 1]
                m += self.board[j + 1][i]
                m += self.board[j + 1][i + 1]
                m += self.board[j + 1][i - 1]
                if m == 3 or (m == 2 and self.board[j][i] == 1):
                    self.boardnext[j][i] = 1
                else:
                    self.boardnext[j][i] = 0
        self.board = self.boardnext[:]
        self.boardnext = [[0] * self.width for _ in range(self.height)]
board = Board(10, 10)
pygame.init()
clock = pygame.time.Clock()
Go = False
running = True
fps1 = 20
while running:
    fps = 100
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN and not Go:
            if event.button == 1:
                board.get_click(event.pos)
                k = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                Go = True
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[32]:
                if Go:
                    Go = False
                else:
                    Go = True
        if event.type == pygame.MOUSEBUTTONDOWN and Go:
            if event.button == 4:
                if fps1 < 100:
                    fps1 += 1
        if event.type == pygame.MOUSEBUTTONDOWN and Go:
            if event.button == 5:
                if fps1 > 1:
                    fps1 -= 1
    if Go:
        Life.next_move(board)
        fps = fps1
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
