"""
GridMap Test
@author: Liu Feihao
"""
import os
import sys
import pygame

# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Screen  import Screen
from Map.GridMap import GridMap

#------------------------------------------Test------------------------------------------#
def main():
    screen = Screen(title="Path Finding")
    grid_map = GridMap(screen, cell_size=50)

    running = True
    while running:
        # Handle events
        # 处理事件
        for event in pygame.event.get():
            
            # 退出界面
            if event.type == pygame.QUIT:
                running = False

            # 处理窗口大小调整事件
            elif event.type == pygame.VIDEORESIZE:
                screen.video_resize_event(event)
                grid_map.update_with_resize(screen)
            
            # 处理鼠标按下事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if left mouse button was pressed
                # 检查是否按下了左键
                if event.button == 1:
                    grid_map.mouse_button_down_event()

            # 处理鼠标松开事件
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    grid_map.mouse_button_up_event()

            # 当鼠标移动时
            elif event.type == pygame.MOUSEMOTION:
                grid_map.mouse_motion_event()

            grid_map.draw_grid(screen)

            # Update the display
            pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()