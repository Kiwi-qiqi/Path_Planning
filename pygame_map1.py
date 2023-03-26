import os
import pygame

from Color import *

# Initialize Pygame
# 初始化 Pygame
pygame.init()

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

# Set the screen size
# 设置屏幕大小
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# 创建小窗口界面并设置大小
panel_width = 300
panel_height = 100
panel_color = TRANSPARENT_BLACK
panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)    # pygame.SRCALPHA，以便表明该surface具有alpha通道
pygame.draw.rect(panel, panel_color, panel.get_rect(), border_radius=20) # (0, 0, 0, 100), 第四个为alpha, 0 ~ 255 的值，值越小越透明

# panel_rect是以(0,0)为左上角顶点绘制矩形框
panel_rect = panel.get_rect()
# 将小窗口放在大窗口右侧中心位置
# panel_rect.center是panel中心的坐标
panel_rect.center = (screen_width // 2, screen_height - panel_height)

# 创建按钮并设置大小, 并横向均匀在panel上
button_width = 80
button_height = 50

button_padding = (panel_width - button_width * 3) // 4
button_y = (panel_height - button_height) // 2
button_color = TRANSPARENT_GRAY

def create_button_text():
    # 创建字体对象
    textes = ['Start \n Search', 'Pause \n Search', 'Clear \n Walls'] #'Cancel \n Search'
    text_color = BLACK
    button_textes = []
    for text in textes:
        font = pygame.font.SysFont('Helvetica', 14)
        button_text = font.render(text, True, text_color)
        button_textes.append(button_text)
    return button_textes


def create_button():
    buttons = []
    buttons_rect = []   # 新建一个空列表来存放按钮
    for i in range(3):
        button = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        buttons.append(button)

        button_rect = button.get_rect()
        pygame.draw.rect(button, button_color, button_rect, border_radius=10)

        button_rect.x = panel_rect.x + button_padding * (i + 1) + button_width * i
        button_rect.y = panel_rect.y + button_y
        buttons_rect.append(button_rect)
    return buttons, buttons_rect

buttons, buttons_rect = create_button()
button_textes = create_button_text()

for button, button_rect, button_text in zip(buttons, buttons_rect, button_textes):
    text_rect = button_text.get_rect(center=button.get_rect().center)
    button.blit(button_text, text_rect)
    screen.blit(button, button_rect)


# Set the background color to white
# 将背景色设置为午夜黑
background_color = MIDNIGHT_BLACK
screen.fill(background_color)

# Set the grid color to black
# 将网格颜色设置为黑色
grid_color = COAL_BLACK

# 设置地图边框网格的颜色为石墨灰
boundary_color = GRAPHITE

free_space_color = PEACH_PUFF

# Initialize the start and end cells
# 初始化起点和终点单元格
start_point = (5, 5)
end_point = (grid_width - 6, grid_height - 6)

start_color = VIRIDIAN_GREEN
end_color = FIREBRICK_RED

# 初始化列表记录地图的边框单元格数据
boundary = set()

# Initialize variables for dragging the start and end cells
# 初始化拖动起点和终点单元格的变量
dragging_start = False
dragging_end = False

# 初始化鼠标滑动选中单元格作为障碍物
drawing_obstacle = False

# 初始化鼠标滑动选中单元格实现障碍物的删除
delete_obstacle = False

# 拖动panel
dragging_panel = False

# 初始化障碍物单元格数据
obstacles = set()
obstalce_color = JET_BLACK

# 设置有效范围
valid_range = {'width':(1, grid_width - 2), 'height':(1, grid_height - 2)}


def update_boundary(boundary, grid_width, grid_height):
    boundary.clear()
    for i in range(grid_width):
        for j in range(grid_height):
            if i == 0 or j == 0 or i == grid_width - 1 or j == grid_height - 1:
                boundary.add((i, j))
    return boundary


def draw_grid():
    # Draw the grid
    # 绘制网格
    for i in range(grid_width):
        for j in range(grid_height):
            # 绘制地图边框网格
            rect = pygame.Rect(i * cell_size, j * cell_size, cell_size - 1, cell_size - 1)
            if i == 0 or j == 0 or i == grid_width - 1 or j == grid_height - 1:
                pygame.draw.rect(screen, boundary_color, rect, 0)

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
                pygame.draw.rect(screen, free_space_color, rect, 0)
            


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


def point_verify(point, valid_range):
    """
    判断起点or终点or障碍物点是否处在当前窗口的有效区域内
    如果超出区间, 则返回True
    未超出区间, 返回False
    """
    if point[0] < valid_range['width'][0] or \
       point[0] > valid_range['width'][1] or \
       point[1] < valid_range['height'][0] or \
       point[1] > valid_range['height'][1]:
        # 如果point不在有效区域
        return True
    else:
        return False


def obstacles_modify(obstacles, valid_range):
    """
    由于窗口界面的变化, 当窗口缩小时, 可能导致障碍物超出了当前窗口界面
    因此当窗口大小变化时, 对障碍物是否在窗口有效范围中进行判断
    将超过有效范围的障碍物单元格进行删除
    当界面恢复时, 原有障碍物的范围不会恢复
    """
    new_obstacles = set()
    for obstacle in obstacles:
        if point_verify(obstacle, valid_range):
            continue
        else:
            new_obstacles.add(obstacle)
    obstacles = new_obstacles
    return obstacles


def update_start_end_point(point, width_range, height_range):
    # 当窗口变化导致起点or终点初始化后, 与障碍物出现重合
    # 此时将对起点和终点进行更新
    # 1)如果是起点, 则从窗口左上侧开始遍历点
    # 2)如果是终点, 则从窗口右下侧开始遍历点
    #   一列一列的进行查找可行点作为起点

    if point in obstacles:
        for i in width_range:
            find_point = False
            for j in height_range:

                if (i, j) not in obstacles and \
                   (i, j) not in boundary:
                    point = (i, j)
                    print('update point: ', point)
                    find_point = True
                    break
                else:
                    continue
            if find_point:
                break
    return point


def reinitialize_start_end_point(start_point, end_point, grid_width, grid_height):
    """
    当窗口缩放时, 按照固定更新模式会导致起点或终点更新与障碍物位置发生重合
    因此需要根据地图环境以及障碍物信息, 对起点与终点网格位置进行更新
    更新策略：
        先给出默认的初始化点, 如果这个点不满足要求, 则
        如果是起点, 则从左侧开始遍历点
        如果是终点, 则从右侧开始遍历点
        一列一列的进行查找可行点作为起点
    """
    # print("re-initializing start and end point")
    if point_verify(start_point, valid_range):
        # 如果超出区域, 则重置起点
        start_point = (5, 5)
    if point_verify(end_point, valid_range):
        # 如果超出区域, 则重置终点
        end_point = (grid_width - 6, grid_height - 6)

    width_range  = list(range(valid_range['width'][0],  valid_range['width'][1]))
    height_range = list(range(valid_range['height'][0], valid_range['height'][1]))

    start_point = update_start_end_point(start_point, width_range, height_range)
    end_point   = update_start_end_point(end_point,   list(reversed(width_range)), list(reversed(height_range)))

    return start_point, end_point


# Main game loop
# 主游戏循环
running = True
while running:
    screen.fill(background_color)
    # Handle events
    # 处理事件
    for event in pygame.event.get():
        # 设置有效范围

        if event.type == pygame.QUIT:
            running = False
        
        # 处理窗口大小调整事件
        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            grid_width = screen_width // cell_size
            grid_height = screen_height // cell_size
            valid_range = {'width':(1, grid_width - 2), 'height':(1, grid_height - 2)}
            boundary = update_boundary(boundary, grid_width, grid_height)
            obstacles = obstacles_modify(obstacles, valid_range)

            # Initialize the start and end cells
            # 初始化起点和终点单元格
            start_point, end_point = reinitialize_start_end_point(start_point, end_point, grid_width, grid_height)

            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            screen.fill(background_color)

        # 处理鼠标按下事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if left mouse button was pressed
            # 检查是否按下了左键
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
                # 判断是否点击到小窗口
                if panel_rect.collidepoint(event.pos):
                    dragging_panel = True
                    drawing_obstacle = False
                    delete_obstacle  = False
                    mouse_x, mouse_y = event.pos
                    # 计算鼠标点击当前位置相对panel中心位置移动了多少
                    # 后续根据偏置量重新得到panel的位置
                    offset_x = mouse_x - panel_rect.x
                    offset_y = mouse_y - panel_rect.y
                    continue

                # Check if the mouse is on the start point
                # 检查鼠标是否在起点上
                if (mouse_pos[0] >= start_point[0] * cell_size and mouse_pos[0] < (start_point[0] + 1) * cell_size and 
                    mouse_pos[1] >= start_point[1] * cell_size and mouse_pos[1] < (start_point[1] + 1) * cell_size):
                    # Start dragging the start point
                    dragging_start = True
                
                # Check if the mouse is on the end point
                # 检查鼠标是否在终点上
                elif (mouse_pos[0] >= end_point[0] * cell_size and mouse_pos[0] < (end_point[0] + 1) * cell_size and 
                      mouse_pos[1] >= end_point[1] * cell_size and mouse_pos[1] < (end_point[1] + 1) * cell_size):
                    # Start dragging the end point
                    dragging_end = True

                # 检查鼠标是否在自由区域
                elif point not in boundary:
                    if point not in obstacles:
                        # 如果当前单元格不在障碍物集合中, 则将其加入集合中
                        obstacles.add(point)
                        drawing_obstacle = True

                    else:
                        # 如果当前单元格为障碍物, 则将其从障碍物集合删除
                        obstacles.remove(point)
                        delete_obstacle = True

                

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
                # 停止删除障碍物
                delete_obstacle = False
                # 停止拖动panel
                dragging_panel = False
            
        # 当鼠标移动时
        elif event.type == pygame.MOUSEMOTION:
            # Check if the mouse is being dragged
            # 检查是否在拖拽
            mouse_pos = pygame.mouse.get_pos()
            point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)

            if dragging_start:
                mouse_pos = validate_verify(valid_range, mouse_pos)
                point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)

                if point != end_point and \
                   point not in obstacles:
                    # Update the position of the start point
                    # 更新起点位置
                    start_point = point
            
            elif dragging_end:
                mouse_pos = validate_verify(valid_range, mouse_pos)
                point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)

                if point != start_point and \
                   point not in obstacles:
                    # Update the position of the end point
                    # 更新终点位置
                    end_point = point

            elif drawing_obstacle:
                # 鼠标滑动选择空白区域作为障碍物
                if point not in boundary and \
                   point not in obstacles and \
                   point != start_point and\
                   point != end_point:
                    obstacles.add(point)


            elif delete_obstacle:
                # 鼠标滑动将已有障碍物取消
                if point not in boundary and \
                   point in obstacles and \
                   point != start_point and\
                   point != end_point:
                    obstacles.remove(point)
            
            elif dragging_panel:
                # 移动的距离
                mouse_x, mouse_y = event.pos

                panel_x = mouse_x - offset_x
                panel_y = mouse_y - offset_y
                # 限制移动范围在大窗口内
                if panel_x < 0:
                    panel_x = 0
                elif panel_x + panel_width > screen_width:
                    panel_x = screen_width - panel_width
                if panel_y < 0:
                    panel_y = 0
                elif panel_y + panel_height > screen_height:
                    panel_y = screen_height - panel_height

                # 更新小窗口和按钮的位置
                panel_rect.x = panel_x
                panel_rect.y = panel_y

                for i in range(len(buttons_rect)):
                    new_button_x = panel_rect.x + button_padding * (i + 1) + button_width * i
                    buttons_rect[i].x = new_button_x
                    buttons_rect[i].y = panel_rect.y + button_y

                    # text = font.render(textes[i], True, text_color)
                    # # 计算文字坐标使其居中
                    # text_rect = text.get_rect(center=button_rect.center)
                    # button.blit(text, text_rect)

        draw_grid()

        screen.blit(panel, panel_rect)

        for i in range(len(buttons_rect)):
            screen.blit(button, buttons_rect[i])

        # Update the display
        pygame.display.update()

# Quit Pygame
pygame.quit()