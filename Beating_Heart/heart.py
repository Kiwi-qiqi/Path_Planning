# Beating Heart
# default input
import random
from math import sin, cos, pi, log
from tkinter import *
 
CANVAS_WIDTH = 980  # frame_width
CANVAS_HEIGHT = 720  # frame_height
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # frame_center_x
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # center_y
IMAGE_ENLARGE = 11  # ratio
# color list
HEART_COLOR_LIST = ["#d974ff", "#be77fa", "#a478f3", "#8b78ea", "#7377e0",
                    "#4871c6", "#5c74d3", "#fa6ea9", "#dc6db1", "#ec2c2c",
                    "#e91e41", "#8b4593", "#2bd3ec", "#00be93", "#2bec62"]
 
 
def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    create a heart
    :param shrink_ratio: ratio
    :param t: parameter
    :return: x, y
    """
    # basic function, size
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
 
    # zoom
    x *= shrink_ratio
    y *= shrink_ratio
 
    # center
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
 
    return int(x), int(y)
 
 
def scatter_inside(x, y, beta=1.15):
    """
    random inner spreading
    :param x: orig x
    :param y: orig y
    :param beta: strength
    :return: new x, y
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
 
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
 
    return x - dx, y - dy
 
 
def shrink(x, y, ratio):
    """
    shrink
    :param x: orig x
    :param y: orig y
    :param ratio: ratio
    :return: new x,y
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)  # 这个参数...
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy
 
 
def curve(p):
    """
    tune beating period
    :param p: parameter
    :return: sin
    """
    # alg
    return 2 * (2 * sin(4 * p)) / (2 * pi)
 
 
class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)
 
    def build(self, number):
        # heart
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
 
        # inner heart 1
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
 
        # inner heart 2
        point_list = list(self._points)
        for _ in range(6000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))
 
    @staticmethod
    def calc_position(x, y, ratio):
        # tune ratio
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)  # alg
 
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
 
        return x - dx, y - dy
 
    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)  # curve
 
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 6000 * abs(curve(generate_frame / 10 * pi) ** 2))
 
        all_points = []
 
        # ring
        heart_halo_point = set()  # x,y of ring pts
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)  # alg
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                # new pts
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))
 
        # appearance
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
 
        # content
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
 
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
 
        self.all_points[generate_frame] = all_points
 
    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=random.choice(HEART_COLOR_LIST))
 
 
def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(70, draw, main, render_canvas, render_heart, render_frame + 1)
 
 
if __name__ == '__main__':
    root = Tk()  # Tk
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)  # draw
 
    # text2 = Label(root, text="爱你",font = ("Helvetica", 18), fg = "#c12bec" ,bg = "black") #
    # text2.place(x=460, y=350)
 
    root.mainloop()