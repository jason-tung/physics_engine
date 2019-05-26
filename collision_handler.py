from collections import deque, defaultdict
from heapq import *
from config import collide_epsilon



def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return True
    return False

class Handler:

    def __init__(self):
        # enqueue all movements and lasting forces here
        # for each object compute all forces acting on it
        # get a net force
        self.heap = []
        self.objects = []

        self.tick = 0





    @staticmethod
    def compute(obj1, obj2):
        # return the forces acted on object one by object two
        # first check for possible collision

        pass

    def run(self):

        apply = defaultdict(dict)

        for i in range(len(self.objects)):
            for j in range(1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]

                apply[obj1][obj2] = self.compute(obj1, obj2)
                apply[obj2][obj1] = self.compute(obj2, obj1)

    @staticmethod
    def is_colliding(self, obj):
        pts1 = self.points()
        pts2 = obj.points()
        for i1 in range(len(pts1)):
            l1 = [pts1[i1],pts1[i1+1]]
            for i2 in range(len(pts2)):
                l2 = [pts2[i2], pts2[i2 + 1]]
                if line_intersection(l1,l2):
                    return True
        return False