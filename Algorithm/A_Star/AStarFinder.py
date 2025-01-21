import os
import sys
import math
import time
import heapq

# 将 Map 文件夹所在路径添加到 sys.path 中
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../Path_Planning/"
sys.path.append(map_path)

from Algorithm.Heuristic.Heuristic import Heuristic

class Node:
    def __init__(self, x, y, g_score=1e6, h_score=0, parent=None):
        self.x = x
        self.y = y
        self.g_score = g_score
        self.h_score = h_score
        self.parent = parent

    def __lt__(self, other):
        return (self.g_score + self.h_score) < (other.g_score + other.h_score)

class AStarFinder:
    def __init__(self, grid_map):
        # 获取起点、终点、地图边界、障碍物的位置
        self.start_point = Node(*grid_map.start_point, g_score=0, h_score=0, parent=None)
        self.end_point   = Node(*grid_map.end_point)
        self.boundary    = grid_map.boundary
        self.obstacles   = grid_map.obstacles

        # open_list and closed_set
        self.open_list = []
        self.closed_set = set()

        # 初始化输出路径
        self.origin_path = []
        self.path = []

        self.init_bool_state()
        # 运行
        self.astar_finder(grid_map)

    def init_bool_state(self):
        self.start_search = False

    def init_heapq(self):
        self.heapq = heapq
        # 初始化优先队列
        heapq.heapify(self.open_list)
        self.heapq.heappush(self.open_list, [self.start_point.g_score + self.start_point.h_score, 
                                             self.start_point])

    def verify_node(self, node):
        """
        对拓展的节点进行验证, 判断该节点是否属于自由区域
        """
        if (node.x, node.y) not in self.obstacles and\
           (node.x, node.y) not in self.boundary  and\
           (node.x, node.y) not in self.closed_set:
            # print('this node is validity')
            return True
        else:
            # print('this node is not validity')
            return False

    def add_neighbor_node(self, current_node, neighbor_node, new_g_score):
        """
        计算当前未在open_list的邻节点的g_score, h_score, parent
        并将其加入open_list
        """
        neighbor_node.g_score = new_g_score
        neighbor_node.h_score = self.calc_h_score(neighbor_node)
        neighbor_node.parent  = current_node

        self.heapq.heappush(self.open_list, [neighbor_node.g_score + neighbor_node.h_score,
                                             neighbor_node])
        heapq.heapify(self.open_list)
        

    def update_neighbor_node(self, current_node, neighbor_node, new_g_score):
        """
        更新当前邻节点的g_score, h_score, parent
        """
        if new_g_score < neighbor_node.g_score:
            neighbor_node.g_score = new_g_score
        neighbor_node.h_score = self.calc_h_score(neighbor_node)
        neighbor_node.parent  = current_node

        index = None
        for i, item in enumerate(self.open_list):
            if item[-1] == neighbor_node:
                index = i
                break

        self.open_list[index][0] = neighbor_node.g_score + neighbor_node.h_score
        self.open_list[index][1].g_score = neighbor_node.g_score
        self.open_list[index][1].h_score = neighbor_node.h_score
        self.open_list[index][1].parent  = neighbor_node.parent
        heapq.heapify(self.open_list)


    def select_diagonal(self, diagonal=True):
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
        if (point.x, point.y) == (self.end_point.x, self.end_point.y):
            print("is_end_point: ", (point.x, point.y), (self.end_point.x, self.end_point.y))
            return True
        
    def calc_h_score(self, point, selection='Manhattan'):
        """
        根据当前节点与目标节点的位置
        选用启发函数计算估计代价值
        """
        # print((point.x, point.y), (self.end_point.x, self.end_point.y))
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
    
    def get_path(self, current_node, cell_size):
        """
        反向索引得到路径
        """
        while current_node:
            self.path.append(((current_node.x+0.5) * cell_size, 
                              (current_node.y+0.5) * cell_size))
            current_node = current_node.parent
        self.path = list(reversed(self.path))

        
    def process_neighbor_node(self, current_node):
        """
        根据motions确定邻节点
        判断邻节点是否为地图边界或障碍物
        如果不是, 则加入open_list
        """
        for motion in self.motions:
            # 获取每个邻节点的索引值
            index_x, index_y = current_node.x - motion[0], current_node.y - motion[1]
            neighbor_node = Node(index_x, index_y)
            # print('neighbor_node: ', (neighbor_node.x, neighbor_node.y))

            # 判断拓展的节点是否可用
            if self.verify_node(neighbor_node):
                # 计算每个邻节点的g_score=当前节点的g_score+两节点的运动代价cost
                cost = math.hypot(motion[0], motion[1])
                neighbor_new_g_score = current_node.g_score + cost

                if neighbor_node not in [node for _, node in self.open_list]:#self.open_list:
                    self.add_neighbor_node(current_node, neighbor_node, neighbor_new_g_score)

                else:
                    index = [i for i, (f_score, node) in enumerate(self.open_list) if node == neighbor_node][0]
                    self.update_neighbor_node(current_node, neighbor_node, neighbor_new_g_score)
            else:
                continue

    def astar_finder(self, grid_map, diagonal=False):
        self.init_heapq()
        self.start_search = True

        while self.start_search:
            # 当点击开始搜索时, 程序开始
            if len(self.open_list) == 0:
                print("Unable to find a path, please check if the starting point or the end point is reachable.")
                self.start_search = False
                break
            
            s_time = time.time()
            # 获取当前队列中总代价最小的节点
            current_node = heapq.heappop(self.open_list)[1]
            heapq.heapify(self.open_list)
            e_time = time.time()
            # print('minium cost node: ', e_time - s_time, ' s')

            self.closed_set.add(current_node)
            if self.is_end_point(current_node):
                print('end_point: ', (current_node.x, current_node.y))
                self.start_search = False

            # 根据当前节点进行direction的拓展, 查找邻节点
            self.select_diagonal(diagonal)
            self.process_neighbor_node(current_node)

        self.get_path(current_node, grid_map.cell_size)



