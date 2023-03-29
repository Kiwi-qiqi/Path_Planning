"""
Heuristic
@author: Liu Feihao
Function:
    Heuristic Test
"""
from Heuristic import *

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    point1 = Point(10, 3)
    point2 = Point(24, 18)
    

    heuristic = Heuristic(point1, point2)

    print('Manhattan distance: ', heuristic.Manhattan())
    print('Euclidean distance: ', heuristic.Euclidean())
    print('Octile distance   : ', heuristic.Octile())
    print('Chebyshev distance: ', heuristic.Chebyshev())

if __name__ == '__main__':
    main()