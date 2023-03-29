import os
import sys
import math
import pygame
import heapq


# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../Path_Planning/"
sys.path.append(map_path)

from Map.Screen  import Screen
from Map.GridMap import GridMap
from Map.Panel   import Panel
from Map.Button  import Button

from Algorithm.Heuristic.Heuristic import Heuristic


class AStarFinder():
    def __init__(self, gridmap):
        # 获取起点、终点、地图边界、障碍物的位置
        self.start_point = gridmap.start_point
        self.end_point   = gridmap.end_point
        self.boundary    = gridmap.boundary
        self.obstacles   = gridmap.obstacles

        # # 初始化open_set and closed_set
        # self.open_set   = dict()
        self.open_list = []
        self.closed_set = dict()

        # 初始化g值, 即路径长度
        self.g_score = 0
    
    def calc_g_score(self, cost):
        """
        从起点到各个节点的实际距离
        当节点的拓展方式不同, g值的计算不同
        采用4-directions时, 相邻节点的距离为1
        采用8-directions时, 相邻节点的距离为1 or sqrt(2)
        """
        self.g_score += cost

    def verify_node(self, node):
        """
        对拓展的节点进行验证, 判断该节点是否属于自由区域
        """
        if node not in self.obstacles and\
           node not in self.boundary:
            return True
        else:
            return False

    def expand_cost(self, motions):
        """
        根据motions确定邻节点
        判断邻节点是否为地图边界或障碍物
        如果不是, 则加入open_list
        """
        for motion in motions:
            cost = math.hypot(motion[0], motion[1])
            index_x, index_y = self.start_point[0] - motion[0], self.start_point[1] - motion[1]
            node = (index_x, index_y)
            if self.verify_node(node):
                self.open_list[(index_x, index_y)] = cost
            else:
                continue

    def get_neighbor(self, direction):
        """
        根据节点拓展方式, 将邻节点加入open_list
        """
        if direction == 4:
            # 四邻节点模式
            motions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            self.expand_cost(motions)
        
        elif direction == 8:
            # 八邻节点模式
            motions = [(1, 0), (-1, 0), (0 , 1), (0 , -1),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]
            self.expand_cost(motions)

    def is_end_point(self, point):
        """
        判断当前节点是否为目标节点
        """
        if point == self.end_point:
            return True
        
    def calc_h_score(self, point, selection='Manhattan'):
        """
        根据当前节点与目标节点的位置
        选用启发函数计算估计代价值
        """
        heuristic = Heuristic(point, self.end_point)
        if selection == 'Manhattan':
            h_score = heuristic.Manhattan()
        elif selection == 'Euclidean':
            h_score = heuristic.Euclidean()
        elif selection == 'Octile':
            h_score = heuristic.Octile()
        elif selection == 'Chebyshev':
            h_score = heuristic.Chebyshev()
        return h_score
    
    def is_diagonal(self, diagonal=True):
        """
        判断是否点击了菜单栏中的对角选项
        如果选中该选项, 则为8-directions, 反之为4-directions
        """
        if diagonal:
            direction = 8
        else:
            direction = 4
        return direction
        
    def astar_finder(self, button, diagonal=True):
        self.open_set[self.start_point] = 0
        while button.Start_Search:
            # 当点击开始搜索时, 程序开始
            if len(self.open_set) == 0:
                print("Unable to find a path, please check if the starting point or the end point is reachable.")

