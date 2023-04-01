"""
GridMap
@author: Liu Feihao
Function:
    Create a GridMap class
    Set Start and End Point
    Select the obstacle by clicking on it with mouse
"""
import os
import sys
import random
import pygame
import numpy as np

# map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Map'))
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color import *

class GridMap():
    """
    GridMap类将屏幕分割为一个一个的网格单元,
    支持在网格单元上绘制起点、终点和障碍物
    也支持对指定的网格进行拖动操作。

    Attributes:
        cell_size:          每个网格单元格的大小（以像素为单位）
        grid_width:         网格的宽度
        grid_height:        网格的高度
        grid_color:         网格颜色
        start_point:        起点单元格坐标
        end_point:          终点单元格坐标
        start_color:        起点单元格颜色
        end_color:          终点单元格颜色
        dragging_start:     是否正在拖动起点单元格
        dragging_end:       是否正在拖动终点单元格
        drawing_obstacle:   是否正在绘制障碍物
        delete_obstacle:    是否正在删除障碍物
        obstacles:          存储障碍物单元格的set
        obstalce_color:     障碍物单元格的颜色
        boundary:           存储网格边框单元格的set
        valid_range:        有效范围, 鼠标只能在这个范围内选取网格单元

    """
    def __init__(self, screen, cell_size=25):
        """
        创建GridMap对象, 并初始化各个属性

        Args:
            cell_size:      每个网格单元格的大小（以像素为单位）, 默认为25
            screen   :      屏幕, 默认为宽度*高度=1000*800
        """
        self.cell_size      = cell_size
        # 计算网格的尺寸
        self.grid_width  = screen.screen_width  // self.cell_size
        self.grid_height = screen.screen_height // self.cell_size
        self.initialize()

    def init_color(self):
        # 设置地图中用到的颜色
        self.grid_color         = COAL_BLACK
        self.boundary_color     = GRAPHITE
        self.free_space_color   = PEACH_PUFF

        self.start_color        = VIRIDIAN_GREEN
        self.end_color          = FIREBRICK_RED
        self.obstalce_color     = JET_BLACK

    def init_start_end_point(self):
        # Initialize the start and end cells
        # 初始化起点和终点单元格
        self.start_point = (5, 5)
        self.end_point   = (self.grid_width - 6, self.grid_height - 6)

    def init_bool_state(self):
        # Initialize variables for dragging the start and end cells
        # 初始化拖动起点和终点单元格的变量
        self.dragging_start     = False
        self.dragging_end       = False
        self.init_random_obs    = False
        self.clear_obstacles    = False
        self.drawing_obstacle   = False    # 初始化鼠标滑动选中单元格作为障碍物
        self.delete_obstacle    = False    # 初始化鼠标滑动选中单元格实现障碍物的删除
        self.obstacle_processing= True     # 初始化时 是可以鼠标单击实现障碍物处理


    def init_boundary(self):
        # 初始化列表记录地图的边框单元格数据
        self.boundary = set()
 
    def init_obstacles(self):
        # 初始化障碍物单元格数据
        self.obstacles = set()

    def set_vaild_range(self):
        # 设置有效范围
        self.valid_range = {'width' :(1, self.grid_width  - 2), 
                            'height':(1, self.grid_height - 2)}

    def set_obstacles(self, density=0.3):
        """
        在窗口初始化时, 创建一些随机障碍物
        随机障碍物范围为地图边界内, 不与起点终点重合
        """
        # 初始化障碍物设置会清空原有的障碍物
        self.obstacles.clear()
        min_range = (self.valid_range['width'][0],   self.valid_range['height'][0])
        max_range = (self.valid_range['width'][1]+1, self.valid_range['height'][1]+1)

        # 共有N个可行的单元格
        N = (max_range[0]-min_range[0]) * (max_range[1]-min_range[1])
        # 设置障碍物密度density
        while len(self.obstacles) < N * density:
            point = tuple(np.random.randint(low=min_range, high=max_range, size=2))
            self.obstacles.add(point)

    def initialize(self):
        self.init_color()
        self.init_start_end_point()
        self.init_bool_state()
        self.init_boundary()
        self.init_obstacles()
        self.set_vaild_range()

    def update_grid(self, screen):
        # 窗口变化后, 对网格地图进行更新
        self.grid_width  = screen.screen_width  // self.cell_size
        self.grid_height = screen.screen_height // self.cell_size

    def update_boundary(self):
        # 窗口大小变化后, 对网格地图边界进行更新
        self.boundary.clear()
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if (i == 0 or i == self.grid_width  - 1 or 
                    j == 0 or j == self.grid_height - 1):
                    self.boundary.add((i, j))

    def set_rect(self, point):
        # 根据单元格所在点的位置绘制一个矩形
        rect = pygame.Rect(point[0]* self.cell_size, point[1] * self.cell_size, 
                           self.cell_size - 1, self.cell_size - 1)
        return rect
    
    def draw_grid(self, screen):
        # Draw the grid
        # 绘制网格
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                # 绘制边框
                if (i == 0 or i == self.grid_width  - 1 or 
                    j == 0 or j == self.grid_height - 1):
                    boundary_rect = self.set_rect((i,j))
                    pygame.draw.rect(screen.interface, self.boundary_color, boundary_rect, 0)

                # 绘制起点单元格
                elif (i, j) == self.start_point:
                    start_rect = self.set_rect((i,j))
                    pygame.draw.rect(screen.interface, self.start_color, start_rect, 0)

                # 绘制终点单元格
                elif (i, j) == self.end_point:
                    end_rect = self.set_rect((i,j))
                    pygame.draw.rect(screen.interface, self.end_color, end_rect, 0)
                
                # 绘制障碍物单元格
                elif (i, j) in self.obstacles:
                    obstacle_rect = self.set_rect((i,j))
                    pygame.draw.rect(screen.interface, self.obstalce_color, obstacle_rect, 0)

                # 绘制空白单元格
                else:
                    free_space_rect = self.set_rect((i,j))
                    pygame.draw.rect(screen.interface, self.free_space_color, free_space_rect, 0)


    def verify_point(self, point):
        """
        判断起点or终点or障碍物点是否处在当前窗口的有效区域内
        如果超出区间, 则返回False
        未超出区间, 返回True
        """
        if  point[0] >= self.valid_range['width'][0] and \
            point[0] <= self.valid_range['width'][1] and \
            point[1] >= self.valid_range['height'][0] and \
            point[1] <= self.valid_range['height'][1]:
            # 如果point处于有效区域
            return True
        else:
            return False

    def update_obstacles(self):
        """
        由于窗口界面的变化, 当窗口缩小时, 可能导致障碍物超出了当前窗口界面
        因此当窗口大小变化时, 对障碍物是否在窗口有效范围中进行判断
        将超过有效范围的障碍物单元格进行删除
        当界面恢复时, 原有障碍物的范围不会恢复
        """
        # print(valid_range['width'][1], valid_range['height'][1])
        new_obstacles = set()
        for obstacle in self.obstacles:
            if self.verify_point(obstacle):
                new_obstacles.add(obstacle)
            else:
                continue
        self.obstacles = new_obstacles

    def search_point(self, point, list1, list2):
        """
        当窗口变化导致起点or终点初始化后, 与障碍物出现重合
        此时将对起点和终点进行更新
        1)如果是起点, 则从窗口左上侧开始遍历点
        2)如果是终点, 则从窗口右下侧开始遍历点
          一列一列的进行查找可行点作为起点
        """
        if point in self.obstacles:
            for i in list1:
                find_point = False
                for j in list2:
                    if ((i, j) not in self.obstacles and 
                        (i, j) not in self.boundary):
                        point = (i, j)
                        print("update to: ", point)
                        find_point = True
                        break
                    else:
                        continue
                if find_point:
                    break
        return point

    def update_start_end_point(self):
        """
        当窗口缩放时, 按照固定更新模式会导致起点或终点更新与障碍物位置发生重合
        因此需要根据地图环境以及障碍物信息, 对起点与终点网格位置进行更新
        更新策略：
            1.窗口变化时判断起点or终点是否在界面内
            2.若不在界面内，则给出默认的初始化点
            3.如果这个点与障碍物的点重合, 则查找自由区域点进行更新
        """
        # print("re-initializing start and end point")
        if not self.verify_point(self.start_point):
            # 如果超出区域, 则重置起点
            self.start_point = (5, 5)
        if not self.verify_point(self.end_point):
            # 如果超出区域, 则重置终点
            self.end_point = (self.grid_width - 6, self.grid_height - 6)
        
        width_range  = list(range(self.valid_range['width'][0],  self.valid_range['width'][1]))
        height_range = list(range(self.valid_range['height'][0], self.valid_range['height'][1]))
        
        self.start_point = self.search_point(self.start_point, width_range, height_range)
        self.end_point   = self.search_point(self.end_point,   list(reversed(width_range)), 
                                                               list(reversed(height_range)))

    def update_with_resize(self, screen):
        self.update_grid(screen)
        self.set_vaild_range()
        self.update_boundary()
        self.update_obstacles()
        self.update_start_end_point()


    def mouse_pos_validate_verify(self, mouse_pos):
        # Check if the mouse is within the valid range
        # 检查鼠标是否在有效范围内

        # 如果不在有效范围, 则将有效范围内设为鼠标能到达的点
        # 检查横向范围
        if mouse_pos[0] // self.cell_size < self.valid_range['width'][0]:
            mouse_pos = (self.valid_range['width'][0] * self.cell_size, mouse_pos[1])
        elif mouse_pos[0] // self.cell_size > self.valid_range['width'][1]:
            mouse_pos = (self.valid_range['width'][1] * self.cell_size, mouse_pos[1])

        # 检查纵向范围
        if mouse_pos[1] // self.cell_size < self.valid_range['height'][0]:
            mouse_pos = (mouse_pos[0], self.valid_range['height'][0] * self.cell_size)
        elif mouse_pos[1] // self.cell_size > self.valid_range['height'][1]:
            mouse_pos = (mouse_pos[0], self.valid_range['height'][1] * self.cell_size)
        return mouse_pos

    def mouse_pose_is_start_or_end(self, mouse_pos, point):
        if (mouse_pos[0] >= point[0] * self.cell_size and mouse_pos[0] < (point[0] + 1) * self.cell_size and 
            mouse_pos[1] >= point[1] * self.cell_size and mouse_pos[1] < (point[1] + 1) * self.cell_size):
            return True    

    def mouse_button_down_event(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
        
        # Check if the mouse is on the start point
        if self.mouse_pose_is_start_or_end(mouse_pos, self.start_point):
            # Start dragging the start point
            self.dragging_start = True
        
        # Check if the mouse is on the end point
        elif self.mouse_pose_is_start_or_end(mouse_pos, self.end_point):
            # Start dragging the end point
            self.dragging_end = True

        # 检查鼠标是否在自由区域
        elif mouse_point not in self.boundary:
            if self.obstacle_processing:
                if mouse_point not in self.obstacles:
                    # 如果当前单元格不在障碍物集合中, 则将其加入集合中
                    self.obstacles.add(mouse_point)
                    self.drawing_obstacle = True

                else:
                    # 如果当前单元格为障碍物, 则将其从障碍物集合删除
                    self.obstacles.remove(mouse_point)
                    self.delete_obstacle = True

    def mouse_button_up_event(self):
        self.dragging_start     = False
        self.dragging_end       = False
        self.drawing_obstacle   = False
        self.delete_obstacle    = False
    
    def mouse_motion_event(self):
        # Check if the mouse is being dragged
        mouse_pos = pygame.mouse.get_pos()
        point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
        
        if self.dragging_start:
            mouse_pos = self.mouse_pos_validate_verify(mouse_pos)
            point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
            if point != self.end_point and \
               point not in self.obstacles:
                # Update the position of the start point
                # 更新起点位置
                self.start_point = point
        
        elif self.dragging_end:
            mouse_pos = self.mouse_pos_validate_verify(mouse_pos)
            point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
            if point != self.start_point and \
               point not in self.obstacles:
                # Update the position of the end point
                # 更新终点位置
                self.end_point = point


        elif self.drawing_obstacle:
            # 鼠标滑动选择空白区域作为障碍物
            if point not in self.boundary and \
               point not in self.obstacles and \
               point != self.start_point and\
               point != self.end_point:
                self.obstacles.add(point)


        elif self.delete_obstacle:
            # 鼠标滑动将已有障碍物取消
            if point not in self.boundary and \
               point in self.obstacles and \
               point != self.start_point and\
               point != self.end_point:
                self.obstacles.remove(point)