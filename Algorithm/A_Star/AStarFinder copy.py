import os
import sys
import math
import pygame
import heapq

test_list = []

# 初始化优先队列
heapq.heapify(test_list)
heapq.heappush(test_list, [20, (5, 4)])
print(test_list)

heapq.heappush(test_list, [30, (6, 5)])
print(test_list)

heapq.heappush(test_list, [25, (4, 5)])
print(test_list)

current_node = heapq.heappop(test_list.copy())
print(current_node)
print(test_list)


node = (6,5)
index = None
for i, item in enumerate(test_list):
    if item[-1] == node:
        index = i
        break

test_list[index][0] = 18

print(test_list)
heapq.heapify(test_list)

current_node = heapq.heappop(test_list)

print(current_node)
print(test_list)

