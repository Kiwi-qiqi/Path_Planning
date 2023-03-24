# 导入必要的库
import random
from math import sin, cos, pi, log
from tkinter import *


# 适合爱心的颜色和名称
COLORS_FOR_HEART = {
    'pink': '#FF69B4',               # 粉红色
    'deep pink': '#FF1493',          # 深粉色
    'crimson': '#DC143C',            # 猩红色
    'magenta': '#FF00FF',            # 洋红色
    'orchid': '#DA70D6',             # 兰花紫
    'dark magenta': '#8B008B',       # 深洋红色
    'medium violet red': '#C71585',  # 中紫红色
    'pink lace': '#FFC0CB',          # 粉色
    'light salmon': '#FFA07A',       # 浅橙色
    'Hot Pink': "#FF69B4"            # 热情的粉红色
}


# 定义画布大小和颜色
CANVAS_WIDTH = 640    # 画布宽度
CANVAS_HEIGHT = 480    # 画布高度
CANVAS_CENTER_X = CANVAS_WIDTH / 2    # 画布中心点X坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2    # 画布中心点Y坐标
IMAGE_ENLARGE = 11    # 图像放大倍数
HEART_COLOR = COLORS_FOR_HEART['Hot Pink']    # 心形颜色


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    根据参数t计算该t对应的x, y坐标, 并返回。

    参数: 
        t: 自变量。
        shrink_ratio: 缩小比例, 默认值为IMAGE_ENLARGE。

    返回值: 
        x, y坐标的元组, 经过shrink_ratio的比例缩小后心形图案出现的位置。
    """
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    x *= shrink_ratio    # 缩小x坐标
    y *= shrink_ratio    # 缩小y坐标

    x += CANVAS_CENTER_X    # 调整x坐标
    y += CANVAS_CENTER_Y    # 调整y坐标

    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """
    计算散点在心形图案内部的位置。

    参数: 
        x: 自变量x。
        y: 自变量y。
        beta: 系数beta, 默认值为0.15。

    返回值: 
        元组, 包含经过计算后的xy坐标。
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def shrink(x, y, ratio):
    """
    根据参数ratio缩小心形图案。

    参数: 
        x: 自变量x。
        y: 自变量y。
        ratio: 缩小比例。

    返回值: 
        元组, 包含经过计算后的xy坐标。
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)  # 这个参数...
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """
    将实数p映射到对应的数值。用于调整绘制心形图案时的曲线。

    参数: 
        p: 实数。

    返回值: 
        p对应的数值。
    """
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:
    def __init__(self, generate_frame=20):
        # 初始化各种点的集合, 以及存放所有点的字典
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        
        # 构建心形图案, 将2000个随机角度对应的坐标添加到_points集合中
        self.build(2000)

        self.random_halo = 1000    # 随机参数

        self.generate_frame = generate_frame    # 生成帧数
        # 计算出所有帧的画布点
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # 先随机生成number个角度t, 计算其对应的坐标, 并加入set _points中
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        # 对于每一个点(x,y), 扩散出3个新点, 加入set _edge_diffusion_points中
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        point_list = list(self._points)    # 将_points转换为列表
        # 对于point_list中的每一个点, 扩散出6000个新点, 加入set _center_diffusion_points中
        for _ in range(6000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        """
        计算点(x,y)缩小后的目标位置。

        参数: 
            x: 自变量x。
            y: 自变量y。
            ratio: 缩小比例。

        返回值: 
            元组, 包含经过计算后的xy坐标。
        """
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)  # 魔法参数

        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)

        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)

        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []

        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 4 * pi)
            x, y = heart_function(t, shrink_ratio=11.5)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        for x, y in self._points:
            # 计算点(x,y)缩小后的目标位置, 将其与size一起添加到all_points中
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        for x, y in self._edge_diffusion_points:
            # 计算扩散边缘上的点(x,y)缩小后的目标位置, 将其与size一起添加到all_points中
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points:
            # 计算扩散中心的点(x,y)缩小后的目标位置, 将其与size一起添加到all_points中
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # 将本次生成的所有点保存到self.all_points中
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        """
        在指定画布上绘制指定帧数的心形图案。

        参数: 
            render_canvas: 绘图的画布。
            render_frame: 要绘制的帧数。

        返回值: 
            无。
        """
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)



def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    """
    绘制心形图案。

    参数: 
        main: GUI主窗口。
        render_canvas: 绘图的画布。
        render_heart: 要绘制的Heart对象。
        render_frame: 当前要绘制的帧数。

    返回值: 
        无。
    """
    render_canvas.delete('all')    # 清空画布
    render_heart.render(render_canvas, render_frame)    # 绘制指定帧数的心形图案
    main.after(10, draw, main, render_canvas, render_heart, render_frame + 1)    # 循环调用自己, 实现动画效果


if __name__ == '__main__':
    root = Tk()    # 创建GUI主窗口
    root.title('Beating_heart')
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)    # 在主窗口上创建一个黑色背景、宽度为CANVAS_WIDTH, 高度为CANVAS_HEIGHT的画布
    canvas.pack()    # 将画布放置在主窗口中
    heart = Heart()    # 创建一个Heart对象
    draw(root, canvas, heart)    # 开始绘制心形图案

    root.mainloop()    # 运行主窗口, 等待用户交互事件