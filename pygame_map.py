import pygame

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# 设置屏幕大小和标题
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Grid Map")

# 定义网格属性
grid_size = 50
margin = 5
num_cols = size[0] // (grid_size + margin)
num_rows = size[1] // (grid_size + margin)

# 初始化地图
grid_map = []
for row in range(num_rows):
    grid_map.append([])
    for col in range(num_cols):
        grid_map[row].append(0)

# 初始化起点和终点
start_pos = [0, 0]
end_pos = [num_rows - 1, num_cols - 1]
grid_map[start_pos[0]][start_pos[1]] = 1
grid_map[end_pos[0]][end_pos[1]] = 2

# 游戏循环
done = False

# 定义变量
dragging = False  # 是否正在拖动
start_dragging = False  # 是否开始拖动
end_dragging = False  # 是否结束拖动

# 游戏循环
while not done:
    # 检查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 获取鼠标位置
            pos = pygame.mouse.get_pos()
            # 计算所在格子的行列号
            row = (pos[1] - margin) // (grid_size + margin)
            col = (pos[0] - margin) // (grid_size + margin)
            # 如果是起点或终点，记录开始拖动
            if (row, col) == start_pos:
                start_dragging = True
            elif (row, col) == end_pos:
                end_dragging = True
            # 否则开始拖动或选择
            else:
                dragging = True
                if grid_map[row][col] == 0:
                    grid_map[row][col] = 3
                elif grid_map[row][col] == 3:
                    grid_map[row][col] = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            # 结束拖动或选择
            dragging = False
            start_dragging = False
            end_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # 如果正在拖动起点或终点，则更新其位置
            if start_dragging:
                pos = pygame.mouse.get_pos()
                row = (pos[1] - margin) // (grid_size + margin)
                col = (pos[0] - margin) // (grid_size + margin)
                if 0 <= row < num_rows and 0 <= col < num_cols:
                    if (row, col) != end:
                        start = (row, col)
            elif end_dragging:
                pos = pygame.mouse.get_pos()
                row = (pos[1] - margin) // (grid_size + margin)
                col = (pos[0] - margin) // (grid_size + margin)
                if 0 <= row < num_rows and 0 <= col < num_cols:
                    if (row, col) != start:
                        end = (row, col)
            # 如果正在选择障碍物，则更新其状态
            elif dragging:
                pos = pygame.mouse.get_pos()
                row = (pos[1] - margin) // (grid_size + margin)
                col = (pos[0] - margin) // (grid_size + margin)
                if 0 <= row < num_rows and 0 <= col < num_cols:
                    if grid_map[row][col] == 0:
                        grid_map[row][col] = 3
                    elif grid_map[row][col] == 3:
                        grid_map[row][col] = 0
    # 绘制地图
    screen.fill(WHITE)
    
    # 绘制网格
    for row in range(num_rows):
        for col in range(num_cols):
            color = BLACK
            if grid_map[row][col] == 1:
                color = GREEN
            elif grid_map[row][col] == 2:
                color = RED
            elif grid_map[row][col] == 3:
                color = GREY
            pygame.draw.rect(screen, color, [(margin + grid_size) * col + margin,
                                             (margin + grid_size) * row + margin,
                                             grid_size, grid_size])
# while not done:

#     # 事件循环
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             # 获取鼠标点击的位置
#             pos = pygame.mouse.get_pos()
#             row = pos[1] // (grid_size + margin)
#             col = pos[0] // (grid_size + margin)
#             # 判断是否点击了起点或终点
#             if (row, col) == tuple(start_pos) or (row, col) == tuple(end_pos):
#                 # 如果是起点或终点，则拖动它们
#                 while True:
#                     event = pygame.event.wait()
#                     if event.type == pygame.MOUSEBUTTONUP:
#                         break
#                     elif event.type == pygame.MOUSEMOTION:
#                         pos = pygame.mouse.get_pos()
#                         new_row = pos[1] // (grid_size + margin)
#                         new_col = pos[0] // (grid_size + margin)
#                         if (new_row, new_col) != tuple(start_pos) and (new_row, new_col) != tuple(end_pos):
#                             if (new_row != row or new_col != col) and 0 <= new_row < num_rows and 0 <= new_col < num_cols:
#                                 # 移动起点或终点，并更新地图
#                                 if (row, col) == tuple(start_pos):
#                                     start_pos = [new_row, new_col]
#                                     grid_map[row][col] = 0
#                                     grid_map[new_row][new_col] = 1
#                                 else:
#                                     end_pos = [new_row, new_col]
#                                     grid_map[row][col] = 0
#                                     grid_map[new_row][new_col] = 2
#                                 row, col = new_row, new_col
#             else:
#                 # 如果不是起点或终点，则将其设为障碍物或非障
#                 # 将选中的格子设为障碍或非障碍
#                 if grid_map[row][col] == 0:
#                     grid_map[row][col] = 3
#                 elif grid_map[row][col] == 3:
#                     grid_map[row][col] = 0

#     # 填充背景色
#     screen.fill(WHITE)

#     # 绘制网格
#     for row in range(num_rows):
#         for col in range(num_cols):
#             color = BLACK
#             if grid_map[row][col] == 1:
#                 color = GREEN
#             elif grid_map[row][col] == 2:
#                 color = RED
#             elif grid_map[row][col] == 3:
#                 color = GREY
#             pygame.draw.rect(screen, color, [(margin + grid_size) * col + margin,
#                                              (margin + grid_size) * row + margin,
#                                              grid_size, grid_size])

    # 更新屏幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()

