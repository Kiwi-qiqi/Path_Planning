import pygame

pygame.init()

# 设置窗口大小和标题
win_width, win_height = 600, 400
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Panel with Buttons Demo")

# 定义颜色和字体
bg_color = (255, 255, 255)
panel_color = (200, 200, 200)
button_color = (150, 150, 150)
active_button_color = (100, 100, 100)
font = pygame.font.SysFont('Helvetica', 18)

# 定义按钮列表和点击事件
buttons = [
    {'label': 'Button 1', 'rect': None, 'callback': lambda: print('Button 1 clicked!')},
    {'label': 'Button 2', 'rect': None, 'callback': lambda: print('Button 2 clicked!')},
    {'label': 'Button 3', 'rect': None, 'callback': lambda: print('Button 3 clicked!')}
]

# 定义面板位置和大小
panel_rect = pygame.Rect(50, 50, 500, 100)

# 利用文字渲染器计算按钮位置和大小
button_width = panel_rect.width // len(buttons)
button_height = panel_rect.height * 2 // 3
for i, button in enumerate(buttons):
    button_surface = font.render(button['label'], True, (0, 0, 0))
    button_rect = pygame.Rect(panel_rect.x + i * button_width, panel_rect.y + panel_rect.height // 6,
                              button_width, button_height)
    button['rect'] = button_rect

# 定义面板是否可拖动的标志
panel_dragging = False
panel_offset_x = 0
panel_offset_y = 0

# 创建面板 Surface，并在其中绘制按钮
panel_surface = pygame.Surface(panel_rect.size)
panel_surface.fill(panel_color)
for button in buttons:
    pygame.draw.rect(panel_surface, button_color, button['rect'])
    button_label = font.render(button['label'], True, (255, 255, 255))
    label_rect = button_label.get_rect(center=button['rect'].center)
    panel_surface.blit(button_label, label_rect)

# 在屏幕上绘制面板和按钮
screen.fill(bg_color)
screen.blit(panel_surface, panel_rect)

# 刷新屏幕
pygame.display.flip()

# 进入主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击在面板上
            if panel_rect.collidepoint(event.pos):
                if all(not button['rect'].collidepoint(event.pos) for button in buttons):
                    panel_dragging = True
                    # 计算面板的偏移量，使鼠标与面板中心对齐
                    panel_offset_x = event.pos[0] - panel_rect.centerx
                    panel_offset_y = event.pos[1] - panel_rect.centery
                else:
                    # 触发相应按钮的点击事件
                    for button in buttons:
                        if button['rect'].collidepoint(event.pos):
                            button['callback']()
                            break
        elif event.type == pygame.MOUSEBUTTONUP:
            panel_dragging = False
        elif event.type == pygame.MOUSEMOTION and panel_dragging:
            # 移动面板位置
            panel_rect.centerx = event.pos[0] - panel_offset_x
            panel_rect.centery = event.pos[1] - panel_offset_y

    # 重新绘制面板和按钮
    panel_surface.fill(panel_color)
    for button in buttons:
        if button['rect'].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(panel_surface, active_button_color, button['rect'])
        else:
            pygame.draw.rect(panel_surface, button_color, button['rect'])
        button_label = font.render(button['label'], True, (255, 255, 255))
        label_rect = button_label.get_rect(center=button['rect'].center)
        panel_surface.blit(button_label, label_rect)
    screen.fill(bg_color)
    screen.blit(panel_surface, panel_rect)

    # 刷新屏幕
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
