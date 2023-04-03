"""
Button Test
@author: Liu Feihao
"""
import os
import sys
import time
import pygame

# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color   import *
from Map.Screen  import Screen
from Map.Panel   import Panel
from Map.Button  import Button

#------------------------------------------Test------------------------------------------#
def countdown_timer(dynamic_visualize):
    # 定义倒数时长
    countdown = 10
    start_time = time.time()
    pause_time = None

    while countdown > 0:
        if dynamic_visualize:
            countdown = 10 - int(time.time() - start_time)
            print('倒计时: ', countdown)
            if countdown <= 0:
                # 计时结束
                dynamic_visualize = False

        else:
            pause_time = time.time()
            start_time += time.time() - pause_time
            countdown = 10 - int(time.time() - start_time)
            print('倒计时: ', countdown)

def show_dynamic(dynamic_visualize):
    for i in range(100):
        if dynamic_visualize:
            pygame.time.delay(100)
            print(i)
            if i >= 9:
                dynamic_visualize = False
                break
        else:
            break


def button1_function_test(button):
    if button.start_search:
        print('Start Search--Algorithm!')
        button.start_search = False
        
    elif button.restart_search:
        print('Restart Search--Algorithm!')
        button.restart_search = False

    elif button.resume_search:
        print('Resume Search--Algorithm!')
        button.resume_search = False


def button2_function_test(button):
    if button.pause_search:
        # 暂停可视化的过程
        print('Pause Search!')
        button.dynamic_visualize = False
        button.pause_search = False

    if button.dynamic_visualize:
        show_dynamic(button.dynamic_visualize)
        
        # button.dynamic_visualize = False
        button.search_over = True

    
    if button.cancel_search:
        print('Cancel Search!')
        button.clear_path = True
        print('Path has been cleared')
        button.clear_path = False
        button.cancel_search = False
    
    elif button.clear_path:
        print('Path has been cleared')
        button.clear_path = False



def button3_function_test(button):
    if button.init_walls:
        print('Init Walls Finished!')
        button.init_walls = False
    
    if button.clear_walls:
        print('Walls Cleared!')
        button.clear_walls = False

def main():
    screen      = Screen(title="Button Test", background_color=PEARL_WHITE)
    panel       = Panel(screen)
    button      = Button(panel)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # 按下 ESC 键退出程序
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.VIDEORESIZE:
                # panel更新到屏幕中下位置,button随着panel移动
                screen.video_resize_event(event)
                panel.update_panel_pose(screen)
                button.update_button_pos(panel)
            
            # 处理鼠标按下事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if left mouse button was pressed
                # 检查是否按下了左键
                if event.button == 1:
                    # 判断鼠标是否点击在panel上
                    panel.mouse_button_down_event()
                    # 判断是否点击在button上
                    button.button_click_event()

                    # 如果点击在button上，则无法拖动panel
                    if button.button_click:
                        panel.dragging_panel = False
                    
            # 处理鼠标松开事件
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    panel.mouse_button_up_event()

            # 当鼠标移动时
            elif event.type == pygame.MOUSEMOTION:
                panel.mouse_motion_event(screen)
                button.update_button_pos(panel)

            
            screen.interface.fill(screen.background_color)
            panel.blit_panel(screen)
            button.blit_button(screen)

            # Update the display
            pygame.display.update()



        # if button.dynamic_visualize:
        #     print('button.dynamic_visualize: ', button.dynamic_visualize)
        # if button.pause_search:
        #     print('button.pause_search     : ', button.pause_search)
        button1_function_test(button)
        button2_function_test(button)
        button3_function_test(button)

        
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()