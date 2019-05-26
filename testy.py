from config import *
from entity import *
from utils import *
from collision_handler import *

hand = Handler()

p1 = Polygon(0, [(0,0),(4,0),(4,4),(0,4)])
p2 = Polygon(0, [(2,3.5),(-1,9),(2,9),(5,6)])
p1.o,p2.o = 0,0


# print("DFSD")
# line1 = [(0,0),(2,2)]
# line2 = [(0,2),(2,0)]
print("test" , utils.line_intersection([(-1,10),(2,3.5)], [(0,0),(4,0)]))
# print("DFSSS")
print(hand.is_colliding(p1,p2))