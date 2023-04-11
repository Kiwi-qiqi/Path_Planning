"""
Path Test
@author: Liu Feihao
"""
import os
import sys
import random
import pygame

# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color   import *
from Map.Screen  import Screen
from Map.Panel   import Panel
from Map.Button  import Button
from Map.GridMap import GridMap
from Map.Path    import Path


#------------------------------------------Test------------------------------------------#
# --------------------Expand_Grip_Test--------------------
def random_expand_grip(grid_map):
    """
    根据当前网格地图大小, 生成一组随机单元格, 模拟算法拓展过程
    从起点开始, 向周围4个或者8个方向随即拓展, 如果拓展到了终点, 则结束
    """
    grid_map.expand_grid.append(grid_map.start_point)

    motions = [(1, 0), (-1, 0), (0 , 1), (0 , -1),
               (1, 1), (1, -1), (-1, 1), (-1, -1)]
    # motions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    index = None
    generate_expand_grid = True
    while generate_expand_grid:
        # print("Generating")
        parent_node = grid_map.expand_grid[-1]
        if index is not None:
            parent_node = grid_map.expand_grid[index-1]
                
        motion_has_explored = set()

        while True:
            i = random.randint(0, 7)
            if motions[i] not in motion_has_explored:
                # 如果这种拓展方式未使用过，则继续
                motion_has_explored.add(motions[i])

                son_node_x = parent_node[0] + motions[i][0]
                son_node_y = parent_node[1] + motions[i][1]
                son_node = (son_node_x, son_node_y)
            else:
                continue

            if len(motion_has_explored) == len(motions):
                # 如果八种拓展方式都找不到合适的解，则换个父节点
                # print('change parent node')
                index = grid_map.expand_grid.index(parent_node)
                break
            
            if son_node not in grid_map.obstacles and \
               son_node not in grid_map.boundary  and \
               grid_map.verify_point(son_node)    and \
               son_node not in grid_map.expand_grid:
                # 由于当前拓展方式随机，会陷入边角区域无法进行下一步拓展
                # 且设置了节点不能重复
                if son_node == grid_map.end_point:
                    # print('Find End Point')
                    # grid_map.expand_grid.append(son_node)
                    generate_expand_grid = False
                    grid_map.expand_grid.pop(0)
                    break

                else:
                    grid_map.expand_grid.append(son_node)
                    if len(grid_map.expand_grid) > 60:
                        generate_expand_grid = False
                        grid_map.expand_grid.pop(0)
                    break
            
            else:
                continue


def create_test_path(cell_size, path):
    for i in range(10, 20):
        path_point = (i, 5)
        path_point = tuple((pose+0.5) * cell_size for pose in path_point)
        path.test_path.append(path_point)
    
    for j in range(6, 15):
        path_point = (19, j)
        path_point = tuple((pose+0.5) * cell_size for pose in path_point)
        path.test_path.append(path_point)

# --------------------Button1--------------------
def button_function_test(button, grid_map, screen, path):
    global count
    if button.start_search:
        print('Start Search--Algorithm!')
        create_test_path(grid_map.cell_size, path)
        random_expand_grip(grid_map)
        
        count = 0
        button.start_search = False
        
    elif button.restart_search:
        count = 0
        grid_map.expand_grid.clear()
        grid_map.expanded_grid.clear()
        print('Restart Search--Algorithm!')
        random_expand_grip(grid_map)    # 扩展的网格
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
    screen      = Screen(title="GridMap Test")
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

        if len(path.test_path) != 0:
            print('Plot Path? ', path.test_path )
        if not button.dynamic_visualize:
            path.plot_test_path(screen)
            pygame.display.update()

        button_function_test(button, grid_map, screen, path)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()