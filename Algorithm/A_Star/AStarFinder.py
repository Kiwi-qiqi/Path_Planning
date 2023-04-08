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

class Node:
    def __init__(self, x, y, g_score=float('inf'), h_score=0, parent=None):
        self.x = x
        self.y = y
        self.g_score = g_score
        self.h_score = h_score
        self.parent = parent

class AStarFinder:
    def __init__(self, grid_map):
        # 获取起点、终点、地图边界、障碍物的位置
        self.start_point = Node(*grid_map.start_point)
        self.end_point   = Node(*grid_map.end_point)
        self.boundary    = grid_map.boundary
        self.obstacles   = grid_map.obstacles

        # open_list and closed_set
        self.open_list = []
        self.closed_set = set()

        # 初始化输出路径
        self.path = []

        # 运行
        self.astar_finder()

    def init_heapq(self):
        self.heapq = heapq
        # 初始化优先队列
        heapq.heapify(self.open_list)
        self.heapq.heappush(self.open_list, (self.start_point.g_score + self.start_point.h_score, 
                                             self.start_point.g_score,  self.start_point.h_score, self.start_point))

    
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
        if (node.x, node.y) not in self.obstacles and\
           (node.x, node.y) not in self.boundary  and\
           (node.x, node.y) not in self.closed_set:
            return True
        else:
            return False

    def update_neighbor_node(self, current_node, neighbor_node, g_score):
        """
        更新该邻节点的g_score, h_score, parent

        """
        neighbor_node.g_score = g_score

        # 根据启发函数计算每个邻节点的h_score
        neighbor_node.h_score = self.calc_h_score(neighbor_node)

        # 更新父节点
        neighbor_node.parent = current_node

        if neighbor_node not in self.open_list:
            # 将该节点加入open_list优先队列中
            self.heapq.heappush(self.open_list, (neighbor_node.g_score + neighbor_node.h_score, 
                                                 neighbor_node.g_score,  neighbor_node.h_score, neighbor_node))


    def expand_node(self, current_node):
        """
        根据motions确定邻节点
        判断邻节点是否为地图边界或障碍物
        如果不是, 则加入open_list
        """
        for motion in self.motions:
            # 获取每个邻节点的索引值
            index_x, index_y = current_node.x - motion[0], current_node.y - motion[1]
            neighbor_node = Node(index_x, index_y)

            # 判断拓展的节点是否可用
            if self.verify_node(neighbor_node):
                # 计算每个邻节点的g_score=当前节点的g_score+两节点的代价cost
                cost = math.hypot(motion[0], motion[1])
                g_score = current_node.g_score + cost

                # 如果拓展的当前节点g_score < 该节点原g_score
                if g_score < neighbor_node.g_score:
                    # 更新邻节点值
                    self.update_neighbor_node(current_node, neighbor_node, g_score)

                self.closed_set.add(current_node)                                                             
            else:
                continue


    def get_neighbor(self, diagonal=True):
        """
        根据节点拓展方式, 将邻节点加入open_list
        默认diagonal=True, 即八邻节点拓展模式
        """
        if diagonal:
            # 八邻节点模式
            self.motions = [(1, 0), (-1, 0), (0 , 1), (0 , -1),
                            (1, 1), (1, -1), (-1, 1), (-1, -1)]
        else:
            # 四邻节点模式
            self.motions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


    def is_end_point(self, point):
        """
        判断当前节点是否为目标节点
        """
        if (point.x, point.y) == self.end_point:
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
    
    def get_path(self, current_node):
        """
        反向索引得到路径
        """
        while current_node:
            self.path.append((current_node.x, current_node.y))
            current_node = current_node.parent
            self.path = list(reversed(self.path))
        
    def astar_finder(self, diagonal=True):
        self.init_heapq()

        while self.open_list:

            # 当点击开始搜索时, 程序开始
            if len(self.open_list) == 0 and len(self.path) == 0:
                print("Unable to find a path, please check if the starting point or the end point is reachable.")
                break
            
            # 获取当前队列中总代价最小的节点
            current_node = heapq.heappop(self.open_list)

            if self.is_end_point(current_node):
                # print("The starting point and ending point overlap. Please reset and search for a path again.")
                # 反推得到路径
                self.get_path(current_node)

            # 根据当前节点进行direction的拓展, 查找邻节点
            self.get_neighbor()
            self.expand_node(current_node)





