"""
Panel
@author: Liu Feihao
Function:
    Create a Panel class
    Set the panel as the carrier for the button.
    
"""
import os
import sys
import pygame

# map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Map'))
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color import *

class Panel():
    def __init__(self, screen, panel_width=300, panel_height=100):
        self.panel_width = panel_width
        self.panel_height = panel_height

        self.initialize(screen)

    def init_pygame(self):
        pygame.init()
        
    def init_color(self):
        self.panel_color    = TRANSPARENT_BLACK
    
    def init_bool_state(self):
        self.dragging_panel             = False

        self.gridmap_process_obstacle   = True
        self.gridmap_drawing_obstacle   = True
        self.gridmap_delete_obstacle    = True
    
    def init_panel(self, screen):
        self.panel = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)     # pygame.SRCALPHA，以便表明该surface具有alpha通道
        pygame.draw.rect(self.panel, self.panel_color, self.panel.get_rect(), border_radius=20) # (0, 0, 0, 100), 第四个为alpha, 0 ~ 255 的值，值越小越透明
        # panel_rect是以(0,0)为左上角顶点绘制矩形框
        self.panel_rect = self.panel.get_rect()

        # 将panel放在screen右侧中心位置, panel_rect.center是panel中心的坐标
        self.panel_rect.center = (screen.screen_width // 2, screen.screen_height - self.panel_height)

    def initialize(self, screen):
        self.init_pygame()
        self.init_color()
        self.init_bool_state()
        self.init_panel(screen)

    def update_panel_pose(self, screen):
        # 窗口大小变化时,更新panel的位置到窗口的中下位置
        self.panel_rect.center = (screen.screen_width // 2, screen.screen_height - self.panel_height)

    def mouse_button_down_event(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.panel_rect.collidepoint(mouse_pos):
            # 当鼠标点击到panel时, panel可拖动, 但无法处理障碍物
            self.dragging_panel            = True

            self.gridmap_process_obstacle = False
            self.gridmap_drawing_obstacle = False
            self.gridmap_delete_obstacle  = False

            # 计算鼠标点击当前位置相对panel中心位置移动了多少
            # 后续根据偏置量重新得到panel的位置
            mouse_x, mouse_y = mouse_pos
            self.offset_x = mouse_x - self.panel_rect.x
            self.offset_y = mouse_y - self.panel_rect.y

    def mouse_button_up_event(self):
        # 停止拖动panel, 障碍物可以被处理
        self.dragging_panel = False

        self.gridmap_process_obstacle = True
        self.gridmap_drawing_obstacle = True
        self.gridmap_delete_obstacle  = True

    def mouse_motion_event(self, screen):
        if self.dragging_panel:
            # 移动的距离
            mouse_x, mouse_y = pygame.mouse.get_pos() #event.pos

            panel_x = mouse_x - self.offset_x
            panel_y = mouse_y - self.offset_y
            # 限制移动范围在大窗口内
            if panel_x < 0:
                panel_x = 0
            elif panel_x + self.panel_width > screen.screen_width:
                panel_x = screen.screen_width - self.panel_width
            if panel_y < 0:
                panel_y = 0
            elif panel_y + self.panel_height > screen.screen_height:
                panel_y = screen.screen_height - self.panel_height

            # 更新小窗口和按钮的位置
            self.panel_rect.x = panel_x
            self.panel_rect.y = panel_y


    def blit_panel(self, screen):
        # pygame.draw.rect(screen.interface, self.panel_rect)
        screen.interface.blit(self.panel, self.panel_rect)
