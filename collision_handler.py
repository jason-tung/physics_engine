from collections import deque, defaultdict
from heapq import *
from config import collide_epsilon
import utils


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
        com1 = self.x,self.y
        com2 = obj.x, obj.y
        if utils.distance(com1, com2) > self.radius + obj.radius:
            return False
        pts1 = self.points
        pts2 = obj.points
        print("pts1", pts1)
        # print("pts1 (_points)", self._points)
        print("x,y", com1)
        for i1 in range(len(pts1)):
            l1 = [pts1[i1],pts1[i1+1]]
            print("l1",l1)
            for i2 in range(len(pts2)):
                l2 = [pts2[i2], pts2[i2 + 1]]
                print("l2", l2)
                inters = utils.line_intersection((l1[0],l1[1]),(l2[0],l2[1]))
                print("inters",inters)
                if inters:
                    return inters
        return False
