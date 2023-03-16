"""
Map
@author: Liu Feihao
Function:
    Build a grid map for path planning

"""

#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../proto/")

import numpy as np
import matplotlib.pyplot as plt

import map_pb2

class Map():
    def __init__(self, length, width, resolution):
        """
        Initialize input paramaters
        Include: length, width and resolution of map
        Example: if length is 8, width is 6, the resolution is 0.1
                 then there are 8/0.1= 80 cells in the length direction 
                 and 6/0.1=60 cells in the width direction
        """
        self.length = length
        self.width = width
        self.resolution = resolution
    
    def get_param(self):
        """
        Return the parameters of this map

        """
        return self.length, self.width, self.resolution
    
    def make_map(self):
        """
        Set the map according to the length and width of the map,
        The feasible area is 0
        The infeasible area is 1
        """
        self.map_frame = []
        for length_ in range(self.length):
            if length_ == 0 or length_ == self.length - 1:
                length_ == 1
            else:
                length_ = 0
            
            for width_ in range(self.width):
                if width_ == 0 or width_ == self.width - 1:
                    width_ == 1
                else:
                    width_ = 0
                    
                    point = (length_, width_)
                    self.map_frame.append(point)


    def show_map(self):
        x_list, y_list = [], []
        for point in self.map_frame:
            p_x = point[0]
            p_y = point[1]

            x_list.append(p_x)
            y_list.append(p_y)

        plt.plot(x_list, y_list, 'sk')
        plt.show()
        

def MapTest():
    length = 50
    width = 30
    resolution = 1

    map = Map(length, width, resolution)
    map.make_map()
    map.show_map()


if __name__ == '__main__':
    MapTest()

