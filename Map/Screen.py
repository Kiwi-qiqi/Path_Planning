import pygame
from Color import *

class Screen():
    def __init__(self, screen_width=1000, screen_height=800, title="Path Finding"):
        self.screen_width   = screen_width
        self.screen_height  = screen_height
        self.title = title
        
        self.init_screen()

    def init_screen(self):
        pygame.init()   # 初始化Pygame
        pygame.display.set_caption(self.title)  #设置pygame窗口名称
        # 创建一个可调节的Pygame窗口
        self.interface = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.background_color = MIDNIGHT_BLACK
        self.interface.fill(self.background_color)


    def video_resize_event(self, event):
        self.screen_width   = event.w
        self.screen_height  = event.h
        self.interface = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.interface.fill(self.background_color)

#------------------------------------------Test------------------------------------------#
def main():
    screen = Screen(screen_width=1500, screen_height=1000, title='Trajectory Optimization')
    running = True
    while running:
        for event in pygame.event.get():
            # 退出界面
            if event.type == pygame.QUIT:
                running = False

            # 处理窗口大小调整事件
            elif event.type == pygame.VIDEORESIZE:
                screen.video_resize_event(event)
            
            # Update the display
            pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()