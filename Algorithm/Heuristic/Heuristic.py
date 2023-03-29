"""
Heuristic
@author: Liu Feihao
Function:
    Heuristic class
"""
import math

class Heuristic():
    """
    根据当前点与目标点
    设置不同的启发函数计算
    """
    def __init__(self, current_point, end_point):
        self.current_point = current_point
        self.end_point     = end_point
        
        self.calc_difference()

    def calc_difference(self):
        self.dx = abs(self.current_point.x - self.end_point.x)
        self.dy = abs(self.current_point.y - self.end_point.y)

    def Manhattan(self):
        """
        manhattan曼哈顿距离, 两点之间只能通过水平or垂直的方向运动
        """
        return self.dx + self.dy
    
    def Euclidean(self):
        """
        Euclidean欧几里得距离, 两点之间最短的连线距离
        """
        return math.hypot(self.dx, self.dy)
    
    def Octile(self):
        """
        Octile距离就是沿着45度角走的最短距离
        """
        F = math.sqrt(2) - 1
        return (F * self.dx + self.dy) if self.dx < self.dy \
                                       else (F * self.dy + self.dx)

    def Chebyshev(self):
        """
        Chebyshev切比雪夫距离定义为两个点各坐标数值差绝对值的最大值
        """
        return max(self.dx, self.dy)

