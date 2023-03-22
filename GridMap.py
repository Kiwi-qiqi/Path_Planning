import pygame
from Color import *


class GridMap:
    """
    GridMap类用于生成一个屏幕, 将屏幕分割为一个一个的网格单元, 支持在网格单元上绘制起点、终点和障碍物, 也支持对网格进行拖动操作。

    Attributes:
        cell_size:          每个网格单元格的大小（以像素为单位）
        screen_width:       屏幕的宽度
        screen_height:      屏幕的高度
        grid_width:         网格的宽度
        grid_height:        网格的高度
        screen:             Pygame窗口对象
        background_color:   背景色
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
    def __init__(self, cell_size=25, screen_width=1000, screen_height=800):
        """
        创建GridMap对象, 并初始化各个属性

        Args:
            cell_size:      每个网格单元格的大小（以像素为单位）, 默认为25
            screen_width:   屏幕的宽度, 默认为1000
            screen_height:  屏幕的高度, 默认为800
        """
        self.cell_size      = cell_size
        self.screen_width   = screen_width
        self.screen_height  = screen_height

        # 计算网格的尺寸
        self.grid_width  = self.screen_width  // self.cell_size
        self.grid_height = self.screen_height // self.cell_size


    def initializeScreen(self):
        # 初始化Pygame
        pygame.init()

        # 创建Pygame窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)


    def initializeColor(self):
        # 设置地图中用到的颜色
        self.background_color   = MIDNIGHT_BLACK
        self.grid_color         = COAL_BLACK

        self.start_color        = VIRIDIAN_GREEN
        self.end_color          = FIREBRICK_RED
        self.obstalce_color     = JET_BLACK


    def initializeStartandEnd(self):
        # Initialize the start and end cells
        # 初始化起点和终点单元格
        self.start_point = (5, 5)
        self.end_point   = (self.grid_width - 6, self.grid_height - 6)


    def initializeBoolState(self):
        # Initialize variables for dragging the start and end cells
        # 初始化拖动起点和终点单元格的变量
        self.dragging_start = False
        self.dragging_end   = False

        # 初始化鼠标滑动选中单元格作为障碍物
        self.drawing_obstacle = False

        # 初始化鼠标滑动选中单元格实现障碍物的删除
        self.delete_obstacle = False

    
    def setVaildRange(self):
        # 设置有效范围
        self.valid_range = {'width' :(1, self.grid_width  - 2), 
                            'height':(1, self.grid_height - 2)}

