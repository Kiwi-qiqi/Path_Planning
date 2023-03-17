import pygame
from queue import PriorityQueue
from Spot import *

# 初始化Pygame
pygame.init()


# 创建窗口
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

def get_clicked_pos(pos):
    x, y = pos
    row = y // GRID_SIZE
    col = x // GRID_SIZE
    return row, col

def draw_grid(win):
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE))
        for j in range(COLS):
            pygame.draw.line(win, GREY, (j * GRID_SIZE, 0), (j * GRID_SIZE, HEIGHT))

def draw(win, grid):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win)
    pygame.display.update()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()

def astar_search(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j)
            grid[i].append(spot)

    return grid


def main():

    # 初始化地图
    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None
    run = True

    # 开始游戏主循环
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标点击位置
                clicked_row, clicked_col = pygame.mouse.get_pos()
                clicked_row = clicked_row // (WIDTH // ROWS)
                clicked_col = (clicked_col - HEIGHT % WIDTH) // (WIDTH // ROWS)

                # 标记起点、终点和障碍物
                if not start and (clicked_row, clicked_col) != end:
                    start = Spot(clicked_row, clicked_col)
                elif not end and (clicked_row, clicked_col) != start:
                    end = Spot(clicked_row, clicked_col)
                elif (clicked_row, clicked_col) != start and (clicked_row, clicked_col) != end:
                    row, col = clicked_row, clicked_col
                    spot = grid[row][col]
                    spot.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # 运行 A* 算法
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    path = astar_search(grid, start, end, draw=draw)

                elif event.key == pygame.K_c:
                    # 清空地图
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

        # 重新绘制整个地图
        draw(win, grid)

        # 更新屏幕
        pygame.display.update()

    # 退出 Pygame
    pygame.quit()

if __name__ == '__main__':
    main()




# def main(win):
#     grid = [[Spot(row, col) for col in range(COLS)] for row in range(ROWS)]
#     start = None
#     end = None
#     run = True

#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False

#             if pygame.mouse.get_pressed()[0]:  # 左键按下
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_clicked_pos(pos)
#                 spot = grid[row][col]

#                 if not start and spot != end:
#                     start = spot
#                     start.make_start()

#                 elif not end and spot != start:
#                     end = spot
#                     end.make_end()

#                 elif not end and spot != start:  # 如果还没有设置终点
#                     end = spot
#                     end.make_end()

#                 elif not start and spot != end:  # 如果还没有设置起点
#                     start = spot
#                     start.make_start()

#                 elif spot != end and spot != start:
#                     spot.make_barrier()

                
#             if pygame.mouse.get_pressed()[2]:  # 右键按下
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_clicked_pos(pos)
#                 spot = grid[row][col]
#                 spot.reset()

#                 if spot == start:
#                     start = None

#                 elif spot == end:
#                     end = None

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and start and end:
#                     for row in grid:
#                         for spot in row:
#                             spot.update_neighbors(grid)

#                     astar_search(win, grid, start, end)

#                 if event.key == pygame.K_c:
#                     start = None
#                     end = None
#                     grid = [[Spot(row, col) for col in range(COLS)] for row in range(ROWS)]

#         draw(win, grid)

#     pygame.quit()

# if __name__ == "__main__":
#     main(win)