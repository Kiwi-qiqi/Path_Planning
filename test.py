import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸
WINDOW_SIZE = (500, 500)

# 创建大窗口
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("大窗口")

# 设定颜色
PEACH_PUFF = (255, 218, 185)
BLACK_TRANSPARENT = (0, 0, 0, 128)

# 填充大窗口背景为 Peach Puff 颜色
window.fill(PEACH_PUFF)

# 创建小窗口
small_window_width = 200
small_window_height = 100
small_window = pygame.Surface((small_window_width, small_window_height), pygame.SRCALPHA)
small_window.fill(BLACK_TRANSPARENT)

# 将小窗口附加到大窗口上
window.blit(small_window, (50, 50))

# 更新屏幕显示
pygame.display.flip()

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 退出 Pygame
pygame.quit()
