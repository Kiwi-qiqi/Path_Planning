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
    """

    def __init__(self, panel, button_width=80, button_height=50):
        self.button_width  = button_width
        self.button_height = button_height

        # 计算按钮的padding和y坐标
        self.button_padding = (panel.panel_width  - button_width * 3) // 4
        self.button_y       = (panel.panel_height - button_height) // 2
        self.initialize()

        self.init_button(panel)

        
#----------------------------------------Button初始化部分----------------------------------------
    def init_pygame(self):
        pygame.init()
        
    def init_color(self):
        self.button_color   = TRANSPARENT_GRAY
        self.text_color     = BLACK

    def init_bool_state(self):
        # Button 1
        self.start_search         = False
        self.restart_search       = False
        self.resume_search        = False

        self.dynamic_visualize    = False

        # Button 2
        self.pause_search         = False
        self.cancel_search        = False
        self.clear_path           = False

        # Button 3
        self.init_walls           = False
        self.clear_walls          = False

        # 起点, 终点, 障碍物是否变化
        self.state_changed        = False

        self.search_over          = False

    def init_font(self):
        self.font = pygame.font.SysFont('Helvetica', 18)

    def init_text(self):
        # 定义按钮列表和点击事件    setattr() 函数, 用来设置对象的属性值
        self.text = [
            {'label': 'Start\nSearch', 'rect': None, 'callback': lambda: setattr(self, 'start_search', True)},
            {'label': 'Pause\nSearch', 'rect': None, 'callback': lambda: setattr(self, 'pause_search', True)},
            {'label': 'Init\nWalls',   'rect': None, 'callback': lambda: setattr(self, 'init_walls', True)}]
        
    def initialize(self):
        self.init_pygame()
        self.init_color()
        self.init_bool_state()
        self.init_font()
        self.init_text()

#----------------------------------------Button文字处理与更新部分----------------------------------------

    def button_with_text(self, index):
        """
        将每个按钮上增加对应的文字
        """
        button = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
        pygame.draw.rect(button, self.button_color, button.get_rect(), border_radius=10)

        # 将文本进行换行处理
        text_lines = textwrap.wrap(self.text[index]['label'], width=5, 
                                   break_long_words=False, break_on_hyphens=False)
        # 计算文本总高度和行高
        total_height = len(text_lines) * self.font.get_height()
        line_height = total_height // len(text_lines)

        y = (button.get_height() - total_height) // 2  # 计算垂直居中的偏移量
        for line in text_lines:
            button_text = self.font.render(line, True, self.text_color)
            # 将文本渲染到按钮上, 并垂直居中显示
            button_text_rect = button_text.get_rect(center=(button.get_width() // 2, y + line_height // 2))
            button.blit(button_text, button_text_rect)
            y += line_height
        return button

    def add_text_to_buttons(self):
        """
        Adds the text to the button surfaces.
        将文本添加到按钮表面上
        """
        self.button_surfaces    = []

        for i in range(3):
            button = self.button_with_text(i)
            self.button_surfaces.append(button)
    

    def create_button(self, panel):
        for i, button in enumerate(self.button_surfaces):
            button_rect = button.get_rect()
            button_rect.x = panel.panel_rect.x + self.button_padding * (i + 1) + self.button_width * i
            button_rect.y = panel.panel_rect.y + self.button_y
            self.text[i]['rect'] = button_rect
            self.buttons_rect.append(button_rect)

        
    def init_button(self, panel):
        self.buttons_rect       = [] 
        self.buttons            = []

        self.add_text_to_buttons()
        self.create_button(panel)



#----------------------------------------Button位置更新部分----------------------------------------

    def update_button_pos(self, panel):
        # 当panel随着screen大小进行更新时,button也随之panel更新
        for i in range(len(self.buttons_rect)):
            new_button_x = panel.panel_rect.x + self.button_padding * (i + 1) + self.button_width * i
            self.buttons_rect[i].x = new_button_x
            self.buttons_rect[i].y = panel.panel_rect.y + self.button_y


    def blit_button(self, screen):
        for i in range(len(self.buttons_rect)):
            screen.interface.blit(self.button_surfaces[i], self.buttons_rect[i])


#----------------------------------------Button文字与状态更新部分----------------------------------------
    def execute_button_action(self, index):
        """
        点击button后, 根据当前button状态执行相应操作
        """
        if index == 0:
            # Button 1
            if self.start_search:
                # start_search后，文字改变，且开始搜索路径
                self.dynamic_visualize = True
                self.text[index]['label'] = 'Restart\nSearch'
                self.text[index]['callback']  = lambda: setattr(self, 'restart_search', True)
            
            if self.restart_search or self.state_changed:
                if self.restart_search:
                    self.dynamic_visualize = True
                self.text[index]['label'] = 'Start\nSearch'
                self.text[index]['callback']  = lambda: setattr(self, 'start_search', True)

            if self.resume_search:
                self.dynamic_visualize = True
                self.text[index]['label'] = 'Restart\nSearch'
                self.text[index]['callback']  = lambda: setattr(self, 'restart_search', True)

                self.text[index+1]['label'] = 'Pause\nSearch'
                self.text[index+1]['callback']  = lambda: setattr(self, 'pause_search', True)

        if index == 1:
            # Button 2
            if self.dynamic_visualize:
                if self.pause_search:
                    self.dynamic_visualize = False
                    self.pause_search = False
                    self.text[index]['label'] = 'Cancel\nSearch'
                    self.text[index]['callback']  = lambda: setattr(self, 'cancel_search', True)

                    # 点击暂停后, start_search 和 restart_search
                    # 此时button 1文字也对应修改
                    self.text[index-1]['label'] = 'Resume\nSearch'
                    self.text[index-1]['callback']  = lambda: setattr(self, 'resume_search', True)
                else:
                    pass

            if self.cancel_search:
                self.dynamic_visualize = False
                self.clear_path = True
                # 取消搜索后，所有路径与已拓展网格全部清空
                self.text[index]['label'] = 'Pause\nSearch'
                self.text[index]['callback']  = lambda: setattr(self, 'pause_search', True)

                # 此时button 1文字也对应修改
                self.text[index-1]['label'] = 'Start\nSearch'
                self.text[index-1]['callback']  = lambda: setattr(self, 'start_search', True)

            if self.search_over:
                # 如果搜索以及动态展示结束，则修改button2为Clear Path
                self.search_over = False

                self.text[index]['label'] = 'Clear\nPath'
                self.text[index]['callback']  = lambda: setattr(self, 'clear_path', True)
            
            if self.clear_path:
                # 搜索结束后，点击clear_path全部清空所有路径与已拓展网格
                self.dynamic_visualize = False
                self.clear_path = True
                self.text[index]['label'] = 'Pause\nSearch'
                self.text[index]['callback']  = lambda: setattr(self, 'pause_search', True)

                # 此时button 1文字也对应修改
                self.text[index-1]['label'] = 'Start\nSearch'
                print(self.text[index-1]['label'])
                self.text[index-1]['callback']  = lambda: setattr(self, 'start_search', True)

        if index == 2:
            # Button 3
            # 第三个按钮有两种状态
            # 初始页面为Init Walls, 此时点击将生成随机障碍物, 而后按钮变为Clear Walls
            # 当存在障碍物时, 按钮状态为Clear Walls, 此时点击将清除所有的walls, 并将按钮名称改为'Init Walls'
            if self.init_walls:
                # self.init_walls = False 这一步在执行完障碍物初始化后执行，在gridmap中
                self.text[index]['label'] = 'Clear\nWalls'
                self.text[index]['callback']  = lambda: setattr(self, 'clear_walls', True)
            
            if self.clear_walls:
                # self.clear_walls = False 这一步在执行完障碍物初始化后执行，在gridmap中
                self.text[index]['label'] = 'Init\nWalls'
                self.text[index]['callback']  = lambda: setattr(self, 'init_walls', True)


    def button_click_event(self):
        mouse_pos = pygame.mouse.get_pos()
        if all(not button['rect'].collidepoint(mouse_pos) for button in self.text):
            # 如果只点击到panel, 而非button上
            self.button_click = False

        else:
            # 如果点击到了button上,此时禁止处理button处的网格
            self.button_click = True

            for button in self.text:
                if button['rect'].collidepoint(mouse_pos):
                    button_index = self.text.index(button)
                    button['callback']()
                    
                    self.execute_button_action(button_index)
                    self.add_text_to_buttons()
                    break