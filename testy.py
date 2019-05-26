from config import *
from entity import *
from utils import *
from collision_handler import *

hand = Handler()

p1 = Polygon(0, [(0,0),(0,4),(4,4),(0,4)])
p2 = Polygon(0, [(2,3.5),(5,6),(2,9),(-1,9)])

print(hand.is_colliding(p1,p2))