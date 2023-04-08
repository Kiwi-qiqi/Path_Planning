"""
Path
@author: Liu Feihao
Function:
    Create a path for algorithm visualization
"""
import os
import sys
import pygame

# map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Map'))
map_path = os.path.dirname(os.path.abspath(__file__)) + "/../../Path_Planning/"
sys.path.append(map_path)

from Map.Color import *

class Path():
    """
    创建Path类, 用于可视化规划算法的轨迹
    """
    def __init__(self, linewidth=4):
        self.linewidth  = linewidth
        
        self.initialize()

    def init_color(self):
        self.color = SIENNA

    def init_path(self):
        self.test_path   = []
        self.tested_path = []

    def init_bool_state(self):
        self.start_search   = False
        self.restart_search = False

    def init_pygame(self):
        pygame.init()

    def initialize(self):
        self.init_color()
        self.init_path()
        self.init_pygame()

    def plot_test_path(self, screen):
        for i in range(len(self.test_path)-1):
            start_node = self.test_path[i]
            end_node   = self.test_path[i+1]
            pygame.draw.line(screen.interface, self.color, start_node, end_node, self.linewidth)