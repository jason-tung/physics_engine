from config import *
from entity import *
from utils import *
from collision_handler import *

hand = Handler()

p1 = Polygon(0, [(0,0),(4,0),(4,4),(0,4)])
p2 = Polygon(0, [(2,3.5),(-1,9),(2,9),(5,6)])
p1.o, p2.o = 0,0

X = [(0,0),(4,0),(4,4),(0,4)]
y = [(2,3.5),(-1,9),(2,9),(5,6)]

import matplotlib.pyplot as plt

plt.plot(*zip(*X))
plt.plot(*zip(*y))
plt.show()

# print("DFSD")
# line1 = [(0,0),(2,2)]
# line2 = [(0,2),(2,0)]
# print(utils.line_intersection(line1,line2))
# print("DFSSS")
print(hand.is_colliding(p1,p2))