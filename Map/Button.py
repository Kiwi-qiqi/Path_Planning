import pygame
import textwrap

from Color import *
from Screen import Screen
from GridMap import GridMap
from Panel import Panel

class Button():
    def __init__(self, panel, grid_map, button_width=80, button_height=50):
        self.button_width = button_width
        self.button_height = button_height

        self.button_padding = (panel.panel_width  - button_width * 3) // 4
        self.button_y       = (panel.panel_height - button_height) // 2

        self.initialize(grid_map, panel)

    def init_pygame(self):
        pygame.init()
        
    def init_color(self):
        self.button_color   = TRANSPARENT_GRAY
        self.text_color     = BLACK

    def init_bool_state(self):
        self.obstacle_processing = True # 用于处理障碍物

    def init_font(self):
        self.font = pygame.font.SysFont('Helvetica', 18)
    
    def add_text_to_button(self):
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
            # panel.blit(button, button_rect)

    def init_button(self, grid_map, panel):
        self.button_surfaces    = []
        self.buttons_rect       = [] 
        self.buttons            = []
        # 定义按钮列表和点击事件
        self.buttons_with_text = [
            {'label': 'Start\nSearch', 'rect': None, 'callback': lambda: print('Button 1 clicked!')},
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
        if all(not button['rect'].collidepoint(mouse_pos) for button in self.buttons_with_text):
            self.button_click = False
        else:
            self.button_click = True
            self.obstacle_processing = False
            for button in self.buttons_with_text:
                if button['rect'].collidepoint(mouse_pos):
                    button['callback']()
                    break

    def update_button(self, panel):
        if panel.dragging_panel:
            for i in range(len(self.buttons_rect)):
                new_button_x = panel.panel_rect.x + self.button_padding * (i + 1) + self.button_width * i
                self.buttons_rect[i].x = new_button_x
                self.buttons_rect[i].y = panel.panel_rect.y + self.button_y

    def blit_button(self, screen):
        for i in range(len(self.buttons_rect)):
            screen.interface.blit(self.button_surfaces[i], self.buttons_rect[i])



#------------------------------------------Test------------------------------------------#
def main():
    screen = Screen(title="Path Finding")
    grid_map = GridMap(screen, cell_size=30)
    panel = Panel(screen)
    button = Button(panel, grid_map)

    running = True
    while running:
        screen.interface.fill(screen.background_color)
        for event in pygame.event.get():
            
            # 退出界面
            if event.type == pygame.QUIT:
                running = False

            # 处理窗口大小调整事件
            elif event.type == pygame.VIDEORESIZE:
                screen.video_resize_event(event)
                grid_map.update_with_resize(screen)
                panel.update_panel_pose(screen)
            
            # 处理鼠标按下事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if left mouse button was pressed
                # 检查是否按下了左键
                if event.button == 1:
                    panel.mouse_button_down_event(grid_map)
                    if panel.dragging_panel:
                        continue
                    else:
                        grid_map.mouse_button_down_event()
                    

            # 处理鼠标松开事件
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    grid_map.mouse_button_up_event()
                    panel.mouse_button_up_event()

            # 当鼠标移动时
            elif event.type == pygame.MOUSEMOTION:
                grid_map.mouse_motion_event()
                panel.mouse_motion_event(screen)
                button.update_button(panel)


            grid_map.draw_grid(screen)
            panel.blit_panel(screen)
            button.blit_button(screen)

            # Update the display
            pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()