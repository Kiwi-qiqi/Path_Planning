import pygame
from Color import *


class GridMap():
    """
    GridMap类用于生成一个屏幕, 将屏幕分割为一个一个的网格单元, 支持在网格单元上绘制起点、终点和障碍物, 也支持对网格进行拖动操作。

    Attributes:
        cell_size:          每个网格单元格的大小（以像素为单位）
        screen_width:       屏幕的宽度
        screen_height:      屏幕的高度
        grid_width:         网格的宽度
        grid_height:        网格的高度
        screen:             Pygame窗口对象
        background_color:   背景色
        grid_color:         网格颜色
        start_point:        起点单元格坐标
        end_point:          终点单元格坐标
        start_color:        起点单元格颜色
        end_color:          终点单元格颜色
        dragging_start:     是否正在拖动起点单元格
        dragging_end:       是否正在拖动终点单元格
        drawing_obstacle:   是否正在绘制障碍物
        delete_obstacle:    是否正在删除障碍物
        obstacles:          存储障碍物单元格的set
        obstalce_color:     障碍物单元格的颜色
        boundary:           存储网格边框单元格的set
        valid_range:        有效范围, 鼠标只能在这个范围内选取网格单元

    """
    def __init__(self, cell_size=25, screen_width=1000, screen_height=800):
        """
        创建GridMap对象, 并初始化各个属性

        Args:
            cell_size:      每个网格单元格的大小（以像素为单位）, 默认为25
            screen_width:   屏幕的宽度, 默认为1000
            screen_height:  屏幕的高度, 默认为800
        """
        self.cell_size      = cell_size
        self.screen_width   = screen_width
        self.screen_height  = screen_height

        # 计算网格的尺寸
        self.grid_width  = self.screen_width  // self.cell_size
        self.grid_height = self.screen_height // self.cell_size
        self.initialize()

    def init_screen(self):
        # 初始化Pygame
        pygame.init()

        # 创建Pygame窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)

    def init_color(self):
        # 设置地图中用到的颜色
        self.background_color   = MIDNIGHT_BLACK
        self.grid_color         = COAL_BLACK
        self.boundary_color     = GRAPHITE
        self.free_space_color   = PEACH_PUFF

        self.start_color        = VIRIDIAN_GREEN
        self.end_color          = FIREBRICK_RED
        self.obstalce_color     = JET_BLACK

    def init_start_end_point(self):
        # Initialize the start and end cells
        # 初始化起点和终点单元格
        self.start_point = (5, 5)
        self.end_point   = (self.grid_width - 6, self.grid_height - 6)

    def init_bool_state(self):
        # Initialize variables for dragging the start and end cells
        # 初始化拖动起点和终点单元格的变量
        self.dragging_start = False
        self.dragging_end   = False

        # 初始化鼠标滑动选中单元格作为障碍物
        self.drawing_obstacle = False

        # 初始化鼠标滑动选中单元格实现障碍物的删除
        self.delete_obstacle = False

    def init_boundary(self):
        # 初始化列表记录地图的边框单元格数据
        self.boundary = set()
 
    def init_obstacles(self):
        # 初始化障碍物单元格数据
        self.obstacles = set()

    def set_vaild_range(self):
        # 设置有效范围
        self.valid_range = {'width' :(1, self.grid_width  - 2), 
                            'height':(1, self.grid_height - 2)}
        
    def initialize(self):
        self.init_screen()
        self.init_color()
        self.init_start_end_point()
        self.init_bool_state()
        self.init_boundary()
        self.init_obstacles()
        self.set_vaild_range()


    def update_boundary(self):
        # 窗口大小变化后, 对网格地图边界进行更新
        self.boundary.clear()
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if (i == 0 or i == self.grid_width  - 1 or 
                    j == 0 or j == self.grid_height - 1):
                    self.boundary.add((i, j))

    def set_rect(self, point):
        # 根据单元格所在点的位置绘制一个矩形
        rect = pygame.Rect(point[0]* self.cell_size, point[1] * self.cell_size, 
                           self.cell_size - 1, self.cell_size - 1)
        return rect
    
    def draw_grid(self):
        # Draw the grid
        # 绘制网格
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                # 绘制边框
                if (i == 0 or i == self.grid_width  - 1 or 
                    j == 0 or j == self.grid_height - 1):
                    boundary_rect = self.set_rect((i,j))
                    pygame.draw.rect(self.screen, self.boundary_color, boundary_rect, 0)

                # 绘制起点单元格
                elif (i, j) == self.start_point:
                    start_rect = self.set_rect((i,j))
                    pygame.draw.rect(self.screen, self.start_color, start_rect, 0)

                # 绘制终点单元格
                elif (i, j) == self.end_point:
                    end_rect = self.set_rect((i,j))
                    pygame.draw.rect(self.screen, self.end_color, end_rect, 0)
                
                # 绘制障碍物单元格
                elif (i, j) in self.obstacles:
                    obstacle_rect = self.set_rect((i,j))
                    pygame.draw.rect(self.screen, self.obstalce_color, obstacle_rect, 0)

                # 绘制空白单元格
                else:
                    free_space_rect = self.set_rect((i,j))
                    pygame.draw.rect(self.screen, self.free_space_color, free_space_rect, 0)


    def verify_point(self, point):
        """
        判断起点or终点or障碍物点是否处在当前窗口的有效区域内
        如果超出区间, 则返回False
        未超出区间, 返回True
        """
        if  point[0] >= self.valid_range['width'][0] and \
            point[0] <= self.valid_range['width'][1] and \
            point[1] >= self.valid_range['height'][0] and \
            point[1] <= self.valid_range['height'][1]:
            # 如果point处于有效区域
            return True
        else:
            return False

    def obstacles_modify(self):
        """
        由于窗口界面的变化, 当窗口缩小时, 可能导致障碍物超出了当前窗口界面
        因此当窗口大小变化时, 对障碍物是否在窗口有效范围中进行判断
        将超过有效范围的障碍物单元格进行删除
        当界面恢复时, 原有障碍物的范围不会恢复
        """
        # print(valid_range['width'][1], valid_range['height'][1])
        new_obstacles = set()
        for obstacle in self.obstacles:
            if self.verify_point(obstacle):
                new_obstacles.add(obstacle)
            else:
                continue
        self.obstacles = new_obstacles

    def search_point(self, point, list1, list2):
        """
        当窗口变化导致起点or终点初始化后, 与障碍物出现重合
        此时将对起点和终点进行更新
        1)如果是起点, 则从窗口左上侧开始遍历点
        2)如果是终点, 则从窗口右下侧开始遍历点
          一列一列的进行查找可行点作为起点
        """
        if point in self.obstacles:
            for i in list1:
                find_point = False
                for j in list2:
                    if ((i, j) not in self.obstacles and 
                        (i, j) not in self.boundary):
                        point = (i, j)
                        print("update to: ", point)
                        find_point = True
                        break
                    else:
                        continue
                if find_point:
                    break
        return point

    def update_start_end_point(self):
        """
        当窗口缩放时, 按照固定更新模式会导致起点或终点更新与障碍物位置发生重合
        因此需要根据地图环境以及障碍物信息, 对起点与终点网格位置进行更新
        更新策略：
            1.窗口变化时判断起点or终点是否在界面内
            2.若不在界面内，则给出默认的初始化点
            3.如果这个点与障碍物的点重合, 则查找自由区域点进行更新
        """
        # print("re-initializing start and end point")
        if not self.verify_point(self.start_point):
            # 如果超出区域, 则重置起点
            self.start_point = (5, 5)
        if not self.verify_point(self.end_point):
            # 如果超出区域, 则重置终点
            self.end_point = (self.grid_width - 6, self.grid_height - 6)
        
        width_range  = list(range(self.valid_range['width'][0],  self.valid_range['width'][1]))
        height_range = list(range(self.valid_range['height'][0], self.valid_range['height'][1]))
        self.start_point = self.search_point(self.start_point, width_range, height_range)
        self.end_point   = self.search_point(self.end_point,   list(reversed(width_range)), 
                                                               list(reversed(height_range)))

    def video_resize_event(self, event):
        self.screen_width   = event.w
        self.screen_height  = event.h
        self.grid_width     = self.screen_width  // self.cell_size
        self.grid_height    = self.screen_height // self.cell_size
        self.set_vaild_range()
        self.update_boundary()
        self.obstacles_modify()
        self.update_start_end_point()

        # 创建Pygame窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.screen.fill(self.background_color)

    def mouse_pos_validate_verify(self, mouse_pos):
        # Check if the mouse is within the valid range
        # 检查鼠标是否在有效范围内

        # 如果不在有效范围, 则将有效范围内设为鼠标能到达的点
        # 检查横向范围
        if mouse_pos[0] // self.cell_size < self.valid_range['width'][0]:
            mouse_pos = (self.valid_range['width'][0] * self.cell_size, mouse_pos[1])
        elif mouse_pos[0] // self.cell_size > self.valid_range['width'][1]:
            mouse_pos = (self.valid_range['width'][1] * self.cell_size, mouse_pos[1])

        # 检查纵向范围
        if mouse_pos[1] // self.cell_size < self.valid_range['height'][0]:
            mouse_pos = (mouse_pos[0], self.valid_range['height'][0] * self.cell_size)
        elif mouse_pos[1] // self.cell_size > self.valid_range['height'][1]:
            mouse_pos = (mouse_pos[0], self.valid_range['height'][1] * self.cell_size)
        return mouse_pos

    def mouse_pose_is_start_or_end(self, mouse_pos, point):
        if (mouse_pos[0] >= point[0] * self.cell_size and mouse_pos[0] < (point[0] + 1) * self.cell_size and 
            mouse_pos[1] >= point[1] * self.cell_size and mouse_pos[1] < (point[1] + 1) * self.cell_size):
            return True    

    def mouse_button_down_event(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if the mouse is on the start point
        if self.mouse_pose_is_start_or_end(mouse_pos, self.start_point):
            # Start dragging the start point
            self.dragging_start = True
        
        # Check if the mouse is on the end point
        elif self.mouse_pose_is_start_or_end(mouse_pos, self.end_point):
            # Start dragging the end point
            self.dragging_end = True

        # 检查鼠标是否在自由区域
        elif (mouse_pos[0], mouse_pos[1]) not in self.boundary:
            if ((mouse_pos[0] // self.cell_size, 
                    mouse_pos[1] // self.cell_size)) not in self.obstacles:
                # 如果当前单元格不在障碍物集合中, 则将其加入集合中
                self.obstacles.add((mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size))
                self.drawing_obstacle = True

            else:
                # 如果当前单元格为障碍物, 则将其从障碍物集合删除
                self.obstacles.remove((mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size))
                self.delete_obstacle = True

    def mouse_button_up_event(self):
        self.dragging_start     = False
        self.dragging_end       = False
        self.drawing_obstacle   = False
        self.delete_obstacle    = False
    
    def mouse_motion_event(self):
        # Check if the mouse is being dragged
        mouse_pos = pygame.mouse.get_pos()
        point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
        
        if self.dragging_start:
            mouse_pos = self.mouse_pos_validate_verify(mouse_pos)
            point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
            if point != self.end_point and \
               point not in self.obstacles:
                # Update the position of the start point
                # 更新起点位置
                self.start_point = point
        
        elif self.dragging_end:
            mouse_pos = self.mouse_pos_validate_verify(mouse_pos)
            point = (mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size)
            if point != self.start_point and \
               point not in self.obstacles:
                # Update the position of the end point
                # 更新终点位置
                self.end_point = point


        elif self.drawing_obstacle:
            # 鼠标滑动选择空白区域作为障碍物
            if point not in self.boundary and \
               point not in self.obstacles and \
               point != self.start_point and\
               point != self.end_point:
                self.obstacles.add(point)


        elif self.delete_obstacle:
            # 鼠标滑动将已有障碍物取消
            if point not in self.boundary and \
               point in self.obstacles and \
               point != self.start_point and\
               point != self.end_point:
                self.obstacles.remove(point)
    

    def run(self):
        # Main game loop
        # 主游戏循环
        running = True
        while running:
            # Handle events
            # 处理事件
            for event in pygame.event.get():
                
                # 退出界面
                if event.type == pygame.QUIT:
                    running = False

                # 处理窗口大小调整事件
                elif event.type == pygame.VIDEORESIZE:
                    self.video_resize_event(event)
                
                # 处理鼠标按下事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if left mouse button was pressed
                    # 检查是否按下了左键
                    if event.button == 1:
                        self.mouse_button_down_event()

                # 处理鼠标松开事件
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_button_up_event()

                # 当鼠标移动时
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion_event()

                self.draw_grid()

                # Update the display
                pygame.display.update()

        # Quit Pygame
        pygame.quit()


#------------------------------------------Test------------------------------------------#
def main():
    grid_map_test = GridMap()
    grid_map_test.run()


if __name__ == "__main__":
    main()