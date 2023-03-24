import pygame

# 初始化pygame
pygame.init()

# 创建窗口并设置大小
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 创建小窗口并设置大小
box_width = 300
box_height = 100
box = pygame.Surface((box_width, box_height))
box.fill((255, 255, 255))
box_rect = box.get_rect()

# 将小窗口放在大窗口中心位置
box_rect.center = (screen_width // 2, screen_height // 2)

# 设置拖拽标志
dragging = False

# 创建按钮并设置大小
button_width = 80
button_height = 30
button_padding = (box_width - button_width * 3) // 4
button_y = (box_height - button_height) // 2
button1_rect = pygame.Rect(button_padding, button_y, button_width, button_height)
button2_rect = pygame.Rect(button_padding * 2 + button_width, button_y, button_width, button_height)
button3_rect = pygame.Rect(button_padding * 3 + button_width * 2, button_y, button_width, button_height)

buttons = [button1_rect, button2_rect, button3_rect]

# 游戏循环
while True:
    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 退出游戏
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 判断是否点击到小窗口
            if box_rect.collidepoint(event.pos):
                dragging = True
                mouse_x, mouse_y = event.pos
                offset_x = mouse_x - box_rect.x
                offset_y = mouse_y - box_rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            # 放开鼠标停止拖拽
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            # 拖拽移动小窗口
            if dragging:
                # 移动的距离
                mouse_x, mouse_y = event.pos
                box_x = mouse_x - offset_x
                box_y = mouse_y - offset_y
                # 限制移动范围在大窗口内
                if box_x < 0:
                    box_x = 0
                elif box_x + box_width > screen_width:
                    box_x = screen_width - box_width
                if box_y < 0:
                    box_y = 0
                elif box_y + box_height > screen_height:
                    box_y = screen_height - box_height

                # 更新小窗口和按钮的位置
                box_rect.x = box_x
                box_rect.y = box_y

                for i in range(len(buttons)):
                    button = buttons[i]
                    new_button_x = box_x + button_padding * (i + 1) + button_width * i
                    # 限制按钮在小窗口内
                    if new_button_x < 0:
                        new_button_x = 0
                    button.x = new_button_x
                    button.y = box_y + button_y

                # for i in range(len(buttons)):
                #     button = buttons[i]
                #     new_button_x = box_x + button_padding * (i + 1) + button_width * i
                #     button.x = new_button_x
                #     button.y = box_y + button_y

                # 绘制按钮
            pygame.draw.rect(box, (120, 120, 120), button1_rect)
            pygame.draw.rect(box, (120, 120, 120), button2_rect)
            pygame.draw.rect(box, (120, 120, 120), button3_rect)

    # 填充背景颜色
    screen.fill((200, 200, 200))

    # 将小窗口绘制到大窗口
    screen.blit(box, box_rect)



    # 更新屏幕显示
    pygame.display.flip()
