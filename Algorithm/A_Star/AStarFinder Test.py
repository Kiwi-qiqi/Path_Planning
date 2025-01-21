"""
A Star Algorithm Test
@author: Liu Feihao
"""
import os
import sys
import time
import pygame

sys.path.append(os.getcwd())

# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color   import *
from Map.Screen  import Screen
from Map.Panel   import Panel
from Map.Button  import Button
from Map.GridMap import GridMap
from Map.Path    import Path

from Algorithm.Heuristic.Heuristic import Heuristic
from AStarFinder import *

#------------------------------------------Test------------------------------------------#
# --------------------Button1--------------------
def delivery_path_to_gridmap(grid_map, astar):
    """
    A star算法规划出的path是屏幕像素坐标系
    需要转换到gridmap的单元格坐标系中
    """
    for point in astar.path:
        x = point[0] // grid_map.cell_size
        y = point[1] // grid_map.cell_size
        grid_map.expand_grid.append((x, y))
    grid_map.expand_grid.pop(0)
    grid_map.expand_grid.pop()

def button_function_test(button, grid_map, screen, path):
    global count
    if button.start_search:
        print('Start Search--Algorithm!')
        search_start = time.time()
        astar = AStarFinder(grid_map)
        search_end   = time.time()
        print('Search Time: ', search_end-search_start, ' s')
        path.test_path = astar.path
        delivery_path_to_gridmap(grid_map, astar)
        count = 0
        button.start_search = False
        
    elif button.restart_search:
        count = 0
        grid_map.expand_grid.clear()
        grid_map.expanded_grid.clear()
        astar = AStarFinder(grid_map)

        print('Restart Search--Algorithm!')
        path.test_path = astar.path
        delivery_path_to_gridmap(grid_map, astar)
        button.restart_search = False

    elif button.resume_search:
        print('Resume Search--Algorithm!')
        button.resume_search = False

# --------------------Button2--------------------
    if button.pause_search:
        # 暂停可视化的过程
        print('Pause Search!', count)
        button.dynamic_visualize = False
        button.pause_search      = False

    if button.dynamic_visualize and not button.pause_search:
        pygame.time.delay(25)
        grid_map.draw_expand_point(grid_map.expand_grid[count], screen)
        grid_map.expanded_grid = grid_map.expand_grid[:count+1]
        count += 1
        pygame.display.update()

        if count >= len(grid_map.expand_grid):
            print('Grid Expanded Finished')
            count = 0
            button.search_over = True
            if button.search_over:
                button.reinit_button(screen)
            button.dynamic_visualize = False
                
    if button.cancel_search:
        print('Cancel Search!')
        grid_map.expand_grid.clear()
        grid_map.expanded_grid.clear()
        path.test_path.clear()
        button.clear_path = True
        button.cancel_search = False
    
    elif button.clear_path:
        count = 0
        grid_map.expand_grid.clear()
        grid_map.expanded_grid.clear()
        path.test_path.clear()
        print('Path has been cleared')
        button.clear_path = False

# --------------------Button3--------------------
    if button.init_walls:
        print('Init Walls Finished!')
        button.init_walls = False
    
    if button.clear_walls:
        print('Walls Cleared!')
        button.clear_walls = False


#------------------------------------------Test------------------------------------------#
def main():
    try:
        screen      = Screen(title="A Star Finder Test")
        panel       = Panel(screen)
        button      = Button(panel)
        grid_map    = GridMap(screen, cell_size=50)
        path        = Path()

        running = True
        while running:
            for event in pygame.event.get():
                # 退出界面
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # 按下 ESC 键退出程序
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # 处理窗口大小调整事件
                elif event.type == pygame.VIDEORESIZE:
                    screen.video_resize_event(event)
                    panel.update_panel_pose(screen)
                    button.update_button_pos(panel)
                    grid_map.update_with_resize(screen)

                # 处理鼠标按下事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if left mouse button was pressed
                    # 检查是否按下了左键
                    if event.button == 1:
                        # 判断鼠标是否点击在panel上
                        panel.mouse_button_down_event()
                        # 判断是否点击在button上
                        button.button_click_event()

                        # 如果点击在button上, 则无法拖动panel
                        if button.button_click:
                            panel.dragging_panel = False
                        grid_map.mouse_button_down_event(panel, button)

                # 处理鼠标松开事件
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        panel.mouse_button_up_event()

                        grid_map.mouse_button_up_event()

                # 当鼠标移动时
                elif event.type == pygame.MOUSEMOTION:
                    panel.mouse_motion_event(screen)
                    button.update_button_pos(panel)
                    grid_map.mouse_motion_event()

                # Update the display
                pygame.display.update()

            button.get_gridmap_obstacles(grid_map)
            screen.interface.fill(screen.background_color)
            grid_map.draw_grid(screen)
            panel.blit_panel(screen)
            button.blit_button(screen)

            if not button.dynamic_visualize:
                path.plot_test_path(screen)
                pygame.display.update()

            button_function_test(button, grid_map, screen, path)

    except Exception as e:
        print('Error: ', e)

    finally:
        # Quit Pygame
        pygame.quit()

if __name__ == "__main__":
    main()