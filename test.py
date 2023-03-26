import pygame

pygame.init()

# 设置窗口大小
win_width, win_height = 640, 480
screen = pygame.display.set_mode((win_width, win_height))

# 创建一个面板矩形框
panel_width, panel_height = 400, 200
panel_color = (192, 192, 192)
panel_rect = pygame.Rect((win_width - panel_width) // 2, (win_height - panel_height) // 2, panel_width, panel_height)

# 创建三个矩形框
button_width, button_height = 100, 50
button_padding = (panel_width - button_width * 3) // 4
button_y = (panel_height - button_height) // 2
button_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
textes = ['Button 1', 'Button 2', 'Button 3']
text_color = pygame.Color('white')
font = pygame.font.SysFont('Arial', 24)

for i in range(3):
    button = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(button, button_colors[i], button.get_rect(), border_radius=10)
    button_rect = button.get_rect()
    button_rect.x = panel_rect.x + button_padding * (i + 1) + button_width * i
    button_rect.y = panel_rect.y + button_y
    panel_surface = screen.subsurface(panel_rect)
    panel_surface.blit(button, button_rect)
    text = font.render(textes[i], True, text_color)
    button.blit(text, text.get_rect(center=button.get_rect().center))

# 刷新屏幕
pygame.display.flip()

# 事件循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
