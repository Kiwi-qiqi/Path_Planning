"""
Button
@author: Liu Feihao
Function:
    Create a new button class to conduct some actions

"""
import os
import sys
import pygame
import textwrap

# map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Map'))
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color import *

class Button():
    """
    按钮类。该类包含有关按钮的信息和事件处理方法。

    Attributes:
    ----------
        button_width : int
            按钮的宽度, 默认值为 80。
        button_height : int
            按钮的高度, 默认值为 50。
        button_padding : int
            每个按钮的间隔, 默认为(panel_width - button_width * 3)// 4。
        button_y : int
            每个按钮的垂直位置, 默认为(panel_height - button_height)// 2。
        button_color : tuple(int, int, int, int)
            按钮的背景颜色。
        text_color : tuple(int, int, int)
            按钮文本的颜色。
        obstacle_processing : bool
            标记是否正在处理障碍物。如果正在处理, 则禁止按钮处理, 否则可以处理。
        font : Font
            pygame 的字体对象。
        button_surfaces : list(Surface)
            存储每个按钮的 Surface。
        buttons_rect : list(Rect)
            存储每个按钮的矩形。
        buttons_with_text : list(dict)
            按钮文本信息的列表。每个字典包含 label, rect 和 callback 字段。

    Methods:
    -------
        __init__(self, panel, grid_map, button_width=80, button_height=50)
            构造函数。初始化按钮属性和按钮的 Surface。
        
        init_pygame(self)
            初始化 pygame。
        
        init_color(self)
            初始化按钮和文本的颜色。
        
        init_bool_state(self)
            初始化 obstacle_processing 属性为 True。
        
        init_font(self)
            初始化 pygame 字体对象。
        
        add_text_to_button(self)
            将按钮文本添加到按钮 Surface 上。
        
        create_button(self, panel)
            创建每个按钮的矩形对象, 并将其添加到 buttons_rect 列表中。
        
        init_button(self, grid_map, panel)
            初始化按钮的信息。将文本添加到按钮 Surface 上, 创建按钮对象
            添加到 buttons_with_text 和 buttons_rect 列表中。
        
        initialize(self, grid_map, panel)
            初始化 Button 类的所有属性。

        button_click_event(self)
            处理按钮点击事件。
        
        update_button(self, panel)
            更新按钮的位置和矩形对象。
        
        blit_button(self, screen)
            在屏幕上绘制按钮。

    """
    def __init__(self, panel, grid_map, button_width=80, button_height=50):
        self.button_width  = button_width
        self.button_height = button_height

        # 计算按钮的padding和y坐标
        self.button_padding = (panel.panel_width  - button_width * 3) // 4
        self.button_y       = (panel.panel_height - button_height) // 2
        self.initialize(grid_map, panel)

    def init_pygame(self):
        pygame.init()
        
    def init_color(self):
        self.button_color   = TRANSPARENT_GRAY
        self.text_color     = BLACK

    def init_bool_state(self):
        self.start_search = False
        self.obstacle_processing = True # 用于处理障碍物

    def init_font(self):
        self.font = pygame.font.SysFont('Helvetica', 18)
    
    def add_text_to_button(self):
        """
        Adds the text to the button surfaces.
        将文本添加到按钮表面上
        """
        for i in range(3):
            button = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
            pygame.draw.rect(button, self.button_color, button.get_rect(), border_radius=10)
            # 将文本进行换行处理
            text_lines = textwrap.wrap(self.buttons_with_text[i]['label'], width=5, break_long_words=False, break_on_hyphens=False)
            # 计算文本总高度和行高
            total_height = len(text_lines) * self.font.get_height()
            line_height = total_height // len(text_lines)

            y = (button.get_height() - total_height) // 2  # 计算垂直居中的偏移量
            for line in text_lines:
                button_text = self.font.render(line, True, self.text_color)
                # 将文本渲染到按钮上，并垂直居中显示
                button_text_rect = button_text.get_rect(center=(button.get_width() // 2, y + line_height // 2))
                button.blit(button_text, button_text_rect)
                y += line_height
            self.button_surfaces.append(button)
    
    def create_button(self, panel):
        for i, button in enumerate(self.button_surfaces):
            button_rect = button.get_rect()
            button_rect.x = panel.panel_rect.x + self.button_padding * (i + 1) + self.button_width * i
            button_rect.y = panel.panel_rect.y + self.button_y
            self.buttons_with_text[i]['rect'] = button_rect
            self.buttons_rect.append(button_rect)


    def init_button(self, grid_map, panel):
        self.button_surfaces    = []
        self.buttons_rect       = [] 
        self.buttons            = []
        # 定义按钮列表和点击事件
        self.buttons_with_text = [
            {'label': 'Start\nSearch', 'rect': None, 'callback': lambda: self.start_search==True},
            {'label': 'Pause\nSearch', 'rect': None, 'callback': lambda: print('Button 2 clicked!')},
            {'label': 'Clear\nWalls',  'rect': None, 'callback': lambda: grid_map.obstacles.clear()}]

        self.add_text_to_button()
        self.create_button(panel)

    def initialize(self, grid_map, panel):
        self.init_pygame()
        self.init_color()
        self.init_bool_state()
        self.init_font()
        self.init_button(grid_map, panel)


    def button_click_event(self):
        mouse_pos = pygame.mouse.get_pos()
        self.obstacle_processing = True

        if all(not button['rect'].collidepoint(mouse_pos) for button in self.buttons_with_text):
            # 如果只点击到panel, 而非button上
            self.button_click = False

        else:
            # 如果点击到了button上,此时禁止处理button处的网格
            self.button_click = True
            self.obstacle_processing = False
            for button in self.buttons_with_text:
                if button['rect'].collidepoint(mouse_pos):
                    button['callback']()
                    break

    def update_button(self, panel):
        # 当panel随着screen大小进行更新时,button也随之更新
        for i in range(len(self.buttons_rect)):
            new_button_x = panel.panel_rect.x + self.button_padding * (i + 1) + self.button_width * i
            self.buttons_rect[i].x = new_button_x
            self.buttons_rect[i].y = panel.panel_rect.y + self.button_y

    def blit_button(self, screen):
        for i in range(len(self.buttons_rect)):
            screen.interface.blit(self.button_surfaces[i], self.buttons_rect[i])