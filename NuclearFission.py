# coding=gbk
from ctypes import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random_map
import ctypes

plt.figure(figsize=(5, 5))

map = random_map.RandomMap()
mymap = np.zeros((map.size, map.size), dtype=c_int)

ax = plt.gca()
ax.set_xlim([0, map.size])
ax.set_ylim([0, map.size])

for i in range(map.size):
    for j in range(map.size):
        if map.IsObstacle(i, j):
            rec = Rectangle((map.size - 1-j, i), width=1, height=1, color='gray')
            ax.add_patch(rec)
            mymap[i][j] = 1
        else:
            rec = Rectangle((map.size - 1-j, i), width=1, height=1, edgecolor='gray', facecolor='w')
            ax.add_patch(rec)
#print mymap
rec = Rectangle((0, 0), width=1, height=1, facecolor='b')
ax.add_patch(rec)

rec = Rectangle((map.size - 1, map.size - 1), width=1, height=1, facecolor='r')
ax.add_patch(rec)

plt.axis('equal')
plt.axis('off')
plt.tight_layout()


class Point(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]


path = np.array([(0, 0)] * map.size*4, dtype=Point)

dll = ctypes.cdll.LoadLibrary('H:/algorithm/lib/pathfide_dll.dll')

map_ctypes_ptr = cast(mymap.ctypes.data, POINTER(c_int))
# path_ctypes_ptr = cast(path.ctypes.data, POINTER(c_int))
dll.getPath.restype = POINTER(Point)
path = dll.getPath(map.size - 1, 0, 0, map.size - 1, map_ctypes_ptr)

current = 0
while path[current].x != 0 and path[current].y != 0:
    rec = Rectangle((map.size - 1-path[current].y, path[current].x), width=1, height=1, facecolor='c')
    ax.add_patch(rec)
    #print("(%s , %d)" %(path[current].x,path[current].y))
    current = current + 1

plt.show()
