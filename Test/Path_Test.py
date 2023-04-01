"""
Button Test
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
from Map.Panel   import Panel
from Map.Button  import Button
from Map.Path    import Path

def create_test_path(cell_size):
    path = []
    for i in range(10, 20):
        path_point = (i, 5)
        path_point = tuple((pose+0.5) * cell_size for pose in path_point)
        path.append(path_point)
    
    for j in range(6, 15):
        path_point = (19, j)
        path_point = tuple((pose+0.5) * cell_size for pose in path_point)

        path.append(path_point)
    return path

#------------------------------------------Test------------------------------------------#
def main():
    screen      = Screen(title="Path Finding")
    grid_map    = GridMap(screen, cell_size=30)
    panel       = Panel(screen)
    button      = Button(panel, grid_map)
    path        = Path(screen)

    is_path_found = False
    running = True
    while running:
        screen.interface.fill(screen.background_color)
        for event in pygame.event.get():
            
            # 退出界面
            if event.type == pygame.QUIT:
                running = False

            # 处理窗口大小调整事件
            elif event.type == pygame.VIDEORESIZE:
                # 窗口更新时,屏幕,网格随着进行比例更新
                # panel更新到屏幕中下位置,button随着panel移动
                screen.video_resize_event(event)
                grid_map.update_with_resize(screen)
                panel.update_panel_pose(screen)
                button.update_button(panel)
            
            # 处理鼠标按下事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if left mouse button was pressed
                # 检查是否按下了左键
                if event.button == 1:
                    # 判断鼠标是否点击在panel上
                    panel.mouse_button_down_event(grid_map)
                    # 判断是否点击在button上
                    button.button_click_event()

                    if button.start_search:
                        test_path = create_test_path(grid_map.cell_size)
                        is_path_found = True

                    # 点击在button上，则不能拖动panel
                    if button.button_click:
                        panel.dragging_panel = False
                    if panel.dragging_panel:
                        continue
                    else:
                        if button.obstacle_processing:
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

            if is_path_found:
                path.plot_path(test_path)

            # Update the display
            pygame.display.update()
        
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()