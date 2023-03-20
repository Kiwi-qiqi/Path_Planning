import os
import pygame

# Define color constants
# 定义颜色常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (64, 64, 64)
BLUE = (0, 0, 255)
Spcify = (190, 190, 190)
Obstacle = (50, 50, 50)

# Set the size of each grid cell in pixels
# 设置每个网格单元格的大小（以像素为单位）
cell_size = 25

# Set the dimensions of the screen
# 设置屏幕的尺寸
screen_width = 1000
screen_height = 800

# Set the dimensions of the grid
# 设置网格的尺寸
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size

# Initialize Pygame
# 初始化 Pygame
pygame.init()

# Set the screen size
# 设置屏幕大小
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Set the background color to white
# 将背景色设置为白色
background_color = WHITE

# Set the grid color to black
# 将网格颜色设置为黑色
grid_color = BLACK

# Initialize the start and end cells
# 初始化起点和终点单元格
start_point = (5, 5)
end_point = (grid_width - 6, grid_height - 6)

start_color = GREEN
end_color = RED

# 初始化列表记录地图的边框单元格数据
boundary = set()

# Initialize variables for dragging the start and end cells
# 初始化拖动起点和终点单元格的变量
dragging_start = False
dragging_end = False

# 初始化鼠标滑动选中单元格作为障碍物的变量
drawing_obstacle = False

# 初始化障碍物单元格数据
obstacles = set()
obstalce_color = (50, 50, 50)


def record_data():
    boundary.clear()
    # 记录网格地图边界, 起点, 终点的数据
    for i in range(grid_width):
        for j in range(grid_height):
            if i == 0 or j == 0 or i == grid_width - 1 or j == grid_height - 1:
                boundary.add((i, j))

def draw_grid():
    # Draw the grid
    # 绘制网格
    for i in range(grid_width):
        for j in range(grid_height):
            # 绘制边框
            rect = pygame.Rect(i * cell_size, j * cell_size, cell_size - 1, cell_size - 1)
            if i == 0 or j == 0 or i == grid_width - 1 or j == grid_height - 1:
                pygame.draw.rect(screen, GRAY, rect, 0)

            # 绘制起点单元格
            elif (i, j) == start_point:
                start_rect = pygame.Rect(start_point[0] * cell_size, start_point[1] * cell_size, cell_size - 1, cell_size - 1)
                pygame.draw.rect(screen, start_color, start_rect, 0)

            # 绘制终点单元格
            elif (i, j) == end_point:
                end_rect = pygame.Rect(end_point[0] * cell_size, end_point[1] * cell_size, cell_size - 1, cell_size - 1)
                pygame.draw.rect(screen, end_color, end_rect, 0)
            
            # 绘制障碍物单元格
            elif (i, j) in obstacles:
                obstacle_rect = pygame.Rect(i * cell_size, j * cell_size, cell_size - 1, cell_size - 1)
                pygame.draw.rect(screen, obstalce_color, obstacle_rect, 0)

            # 绘制空白单元格
            else:
                pygame.draw.rect(screen, Spcify, rect, 0)
            


# valid_range = {'width':(1, grid_width - 2), 'height':(1, grid_height - 2)}
def validate_verify(valid_range, mouse_pos):
    # Check if the mouse is within the valid range
    # 检查鼠标是否在有效范围内

    # 如果不在有效范围, 则将有效范围内设为鼠标能到达的点
    # 检查横向范围
    if mouse_pos[0] // cell_size < valid_range['width'][0]:
        mouse_pos = (valid_range['width'][0] * cell_size, mouse_pos[1])
    elif mouse_pos[0] // cell_size > valid_range['width'][1]:
        mouse_pos = (valid_range['width'][1] * cell_size, mouse_pos[1])

    # 检查纵向范围
    if mouse_pos[1] // cell_size < valid_range['height'][0]:
        mouse_pos = (mouse_pos[0], valid_range['height'][0] * cell_size)
    elif mouse_pos[1] // cell_size > valid_range['height'][1]:
        mouse_pos = (mouse_pos[0], valid_range['height'][1] * cell_size)
    
    return mouse_pos


# Main game loop
# 主游戏循环
running = True
while running:
    # Handle events
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 处理窗口大小调整事件
        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            grid_width = screen_width // cell_size
            grid_height = screen_height // cell_size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            screen.fill(background_color)

        # 处理鼠标按下事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if left mouse button was pressed
            # 检查是否按下了左键
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the mouse is on the start point
                # 检查鼠标是否在起点上
                if (mouse_pos[0] >= start_point[0] * cell_size and mouse_pos[0] < (start_point[0] + 1) * cell_size and 
                    mouse_pos[1] >= start_point[1] * cell_size and mouse_pos[1] < (start_point[1] + 1) * cell_size):
                    # Start dragging the start point
                    # 开始拖拽起点
                    dragging_start = True
                
                # Check if the mouse is on the end point
                # 检查鼠标是否在终点上
                elif (mouse_pos[0] >= end_point[0] * cell_size and mouse_pos[0] < (end_point[0] + 1) * cell_size and 
                      mouse_pos[1] >= end_point[1] * cell_size and mouse_pos[1] < (end_point[1] + 1) * cell_size):
                    # Start dragging the end point
                    # 开始拖拽终点
                    dragging_end = True

                # 检查鼠标是否在自由区域
                elif (mouse_pos[0], mouse_pos[1]) not in boundary:
                    drawing_obstacle = True
                    if ((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)) not in obstacles:
                        obstacles.add((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size))
                    else:
                        obstacles.remove((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size))

                
            # print(drawing_obstacle)


        # 当鼠标抬起时
        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if left mouse button was released
            # 检查是否释放了左键
            if event.button == 1:   
                # Stop dragging the start point
                # 停止拖拽起点
                dragging_start = False
                
                # Stop dragging the end point
                # 停止拖拽终点
                dragging_end = False

                # 停止选择障碍物
                drawing_obstacle = False
            

        # 当鼠标移动时
        elif event.type == pygame.MOUSEMOTION:
            # Check if the mouse is being dragged
            # 检查是否在拖拽

            # 设置有效范围
            valid_range = {'width':(1, grid_width - 2), 'height':(1, grid_height - 2)}

            if dragging_start:
                # Get the position of the mouse
                # 获取鼠标位置
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = validate_verify(valid_range, mouse_pos)
                if (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size) != end_point:
                    # Update the position of the start point
                    # 更新起点位置
                    start_point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
            
            elif dragging_end:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = validate_verify(valid_range, mouse_pos)
                if (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size) != start_point:
                    # Update the position of the end point
                    # 更新终点位置
                    end_point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)

            elif drawing_obstacle:
                # print("Select cell for obstacle ")
                mouse_pos = pygame.mouse.get_pos()
                if ((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)) not in boundary and \
                   ((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)) not in obstacles and \
                   (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size) != start_point and\
                   (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size) != end_point:
                    # print("Add the cell to obstacle")
                    obstacles.add((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size))
                    # print(obstacles)

                # elif ((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)) in obstacles:
                #     # print("Delete the cell from obstacle")
                #     obstacles.remove((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size))

            
        draw_grid()
        record_data()

        # Update the display
        pygame.display.update()

# Quit Pygame
pygame.quit()