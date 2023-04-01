"""
Screen Test
@author: Liu Feihao
"""
import os
import sys
import pygame
# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color   import *

from Map.Screen import Screen

#------------------------------------------Test------------------------------------------#
def main():
    """
    主函数, 创建 Screen 类的实例, 循环处理事件, 更新 Pygame 窗口, 直到退出 Pygame。
    """
    screen = Screen(screen_width=1500, screen_height=1000, 
                    title='Screen Test', background_color=PEARL_WHITE)
    running = True
    while running:
        for event in pygame.event.get():
            # 退出界面
            if event.type == pygame.QUIT:
                running = False

            # 处理窗口大小调整事件
            elif event.type == pygame.VIDEORESIZE:
                screen.video_resize_event(event)
            
            screen.interface.fill(screen.background_color)
            
            # Update the display
            pygame.display.update()
    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()