import pygame
import time

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 设置窗口大小
WINDOW_SIZE = (400, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)

# 设置窗口标题
pygame.display.set_caption("倒数10秒")

# 定义字体
font = pygame.font.SysFont(None, 24)

# 定义按钮
start_button_rect = pygame.Rect(50, 250, 100, 50)
start_button_color = WHITE
start_button_text = font.render("Start", True, BLACK)
start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
start_button_pressed = False

pause_button_rect = pygame.Rect(250, 250, 100, 50)
pause_button_color = WHITE
pause_button_text = font.render("Pause", True, BLACK)
pause_button_text_rect = pause_button_text.get_rect(center=pause_button_rect.center)
pause_button_pressed = False

# 定义倒数时长
countdown = 10
start_time = None
pause_time = None

# 游戏循环
while True:
    # 检查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                if not start_button_pressed:
                    start_button_pressed = True
                    start_time = time.time()
                    pause_time = None
                    start_button_text = font.render("Start", True, BLACK)
                    pause_button_text = font.render("Pause", True, BLACK)
            elif pause_button_rect.collidepoint(event.pos):
                if start_button_pressed:
                    pause_button_pressed = not pause_button_pressed
                    if pause_button_pressed:
                        pause_button_text = font.render("Cancel", True, BLACK)
                        start_button_text = font.render("Continue", True, BLACK)
                        pause_time = time.time()
                    else:
                        pause_button_text = font.render("Pause", True, BLACK)
                        start_button_text = font.render("Start", True, BLACK)
                        start_time += time.time() - pause_time

    # 绘制界面
    screen.fill(BLACK)
    countdown_text = font.render(str(countdown), True, WHITE)
    countdown_text_rect = countdown_text.get_rect(center=screen.get_rect().center)
    screen.blit(countdown_text, countdown_text_rect)
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    screen.blit(start_button_text, start_button_text_rect)
    pygame.draw.rect(screen, pause_button_color, pause_button_rect)
    screen.blit(pause_button_text, pause_button_text_rect)

    # 更新界面
    pygame.display.update()

    # 计算倒数时间
    if start_button_pressed and not pause_button_pressed:
        countdown = 10 - int(time.time() - start_time)
        if countdown <= 0:
            countdown = 0
            start_button_pressed = False
            start_button_text = font.render("Start", True, BLACK)
            pause_button_text = font.render("Pause", True, BLACK)
            start_time = None
            pause_time = None
    elif start_button_pressed and pause_button_pressed:
        countdown = countdown
    else:
        countdown = 10

    # 退出pygame


# 在这个代码中，我们首先使用Pygame创建了一个窗口，
# 并定义了两个按钮，一个是“Start”按钮，另一个是“Pause”按钮。
# 我们还定义了倒数时长变量，初始值为10。
# 然后，在游戏循环中，我们不断检查事件，例如鼠标点击事件，以响应用户的操作。
# 当用户点击“Start”按钮时，倒计时开始，当用户点击“Pause”按钮时，倒计时暂停，
# 当用户再次点击“Continue”按钮时，倒计时继续，
# 当用户再次点击“Cancel”按钮时，倒计时被取消，重新开始从10秒开始倒计时。

# 我们使用time模块来计算时间，使用pygame的渲染机制来绘制倒计时和按钮。
# 在绘制按钮时，我们检查按钮是否被按下，如果是，则将按钮颜色和文本更改为相应的状态。

# 最后，当倒计时为0时，我们将倒计时重置为10，
# 并将“Start”和“Pause”按钮文本更改为初始状态。

# 你可以将这个代码保存在一个.py文件中，然后运行它来体验倒计时程序。
