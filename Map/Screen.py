"""
Screen
@author: Liu Feihao
Function:
    Create a Screen class
    The window size can be adjusted and limited as needed.
"""
import os
import sys
import pygame
import win32api

# map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Map'))
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"   # 选哪个路径格式都可以
sys.path.append(map_path)

from Map.Color import *

class Screen:
    """
    创建一个 Pygame 窗口类。

    Attributes:
    -----------
    screen_width: int
        窗口的宽度, 默认值为 1000。
    screen_height: int
        窗口的高度, 默认值为 800。
    title: str
        窗口的标题, 默认值为 "Path Finding"。

    Methods:
    --------
    init_screen()
        初始化 Pygame, 设置窗口名称, 创建 Pygame 窗口, 填充背景颜色。
    update_screen_size()
        更新窗口大小。
    set_screen_range()
        设置屏幕最大最小范围。
    video_resize_event(event)
        处理窗口大小调整事件。
    """

    def __init__(self, screen_width=1000, screen_height=800, title="Path Finding"):
        self.screen_width   = screen_width
        self.screen_height  = screen_height
        self.title          = title
        
        self.update_screen_size()
        self.init_screen()
        self.set_screen_range()

    def init_screen(self):
        """初始化 Pygame, 设置窗口名称, 创建 Pygame 窗口, 填充背景颜色。"""
        pygame.init()
        pygame.display.set_caption(self.title)
        self.interface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.background_color = MIDNIGHT_BLACK
        self.interface.fill(self.background_color)

    def update_screen_size(self):
        """更新窗口大小。"""
        self.size = (self.screen_width, self.screen_height)

    def set_screen_range(self):
        """设置屏幕最大最小范围。"""
        # 设置最小屏幕参数
        self.min_size = (500, 400)

        # 获取显示器分辨率作为最大屏幕参数
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        self.max_size = (width, height)

    def video_resize_event(self, event):
        """
        处理窗口大小调整事件。
        如果窗口大小超出最大或最小限制, 则将其调整为最大或最小值
        更新窗口大小, 并填充背景颜色。
        """
        self.screen_width   = event.w
        self.screen_height  = event.h

        if self.screen_width < self.min_size[0] or self.screen_height < self.min_size[1]:
            self.screen_width, self.screen_height = self.min_size
        elif self.screen_width > self.max_size[0] or self.screen_height > self.max_size[1]:
            self.screen_width, self.screen_height = self.max_size
        self.update_screen_size()
        self.interface = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.interface.fill(self.background_color)
