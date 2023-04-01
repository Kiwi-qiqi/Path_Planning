import pygame
import panel as pn
import sys

# 初始化 Pygame 和 Panel
pygame.init()
pn.extension()

# 设置游戏屏幕的大小和标题
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pygame with Panel')

# 创建一个 Panel 应用，并定义 Panel 的大小和位置
app = pn.Column(width=500, height=400)
app_pos = (150, 100)

# 创建一个 Checkbox，并将其与一段文本绑定在一起
checkbox = pn.widgets.Checkbox(name='选项 1', width=100)
text = pn.pane.Markdown('这里是选项 1 执行的内容')

# 定义当 Checkbox 被选中时执行的函数
def checkbox_callback(event):
    if event.new:
        # Checkbox 被选中
        checkbox.label = '✓ 选项 1'
        text.object = '这里是选项 1 执行的内容'
        # 执行选项 1 对应的功能
        print('执行选项1')
    else:
        # Checkbox 被取消选中
        checkbox.label = '○ 选项 1'
        text.object = ''
        # 取消选项 1 对应的功能
        print('不执行选项1')

# 将 Checkbox 的回调函数绑定到其 on_change 事件上
# checkbox._comm_change('value', checkbox_callback)
checkbox._comm_change['value'] = [checkbox_callback]


# 在 Panel 上添加 Checkbox 和文本
app.append(checkbox)
app.append(text)

# 定义 Panel 的位置和大小，以及 Panel 是否被拖动
panel_rect = pygame.Rect(app_pos[0], app_pos[1], app.width, app.height)
is_dragging_panel = False

# 游戏主循环
while True:
    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标是否在 Panel 上单击
            if panel_rect.collidepoint(event.pos):
                is_dragging_panel = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # 停止拖动 Panel
            is_dragging_panel = False
        elif event.type == pygame.MOUSEMOTION:
            # 如果正在拖动 Panel，移动 Panel 到新位置
            if is_dragging_panel:
                panel_rect.move_ip(event.rel)
                app_pos = (panel_rect.left, panel_rect.top)
    
    # 绘制屏幕背景和 Panel
    screen.fill((255, 255, 255))
    app.show(port=pygame.display.get_wm_info()['window'])
    pygame.display.update()
