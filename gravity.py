from World import Force
from entity import Polygon
from utils import distance
from constants import G
from math import sin, cos


def gravity(obj1: Polygon, obj2: Polygon):
    """

    :param obj1:
    :param obj2:
    :return: (force on first object, force on second object)
    """

    def gen_frc():
        x1, y1 = obj1.x, obj1.y
        x2, y2 = obj2.x, obj2.y

        x = x2 - x1
        y = y2 - y1
        r = distance((x1, y1), (x2, y2))

        magnitude = G * obj1.m * obj2.m / (r**2)

        fx = x / r * magnitude
        fy = y / r * magnitude

        return (fx, fy)

    return Force(obj1, gen_frc, float('inf'))