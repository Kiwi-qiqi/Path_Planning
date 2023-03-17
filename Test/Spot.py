import pygame
from queue import PriorityQueue

# 初始化Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# 定义地图尺寸和格子尺寸
WIDTH = 800
HEIGHT = 600
ROWS = 50
COLS = 50
GRID_SIZE = WIDTH // COLS

# 创建窗口
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# 定义单个格子的类
class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * GRID_SIZE
        self.y = col * GRID_SIZE
        self.color = WHITE
        self.neighbors = []
        self.previous = None

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():  # 下面一个点不是障碍
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # 上面一个点不是障碍
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_barrier():  # 右边一个点不是障碍
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # 左边一个点不是障碍
            self.neighbors.append(grid[self.row][self.col - 1])