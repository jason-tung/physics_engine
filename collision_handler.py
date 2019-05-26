from collections import deque, defaultdict
from heapq import *
from config import collide_epsilon
from utils import segment_intersection, distance


class Handler:

    def __init__(self):
        # enqueue all lasting forces here
        # for each object compute all forces acting on it
        # get a net force
        self.objects = []


    @staticmethod
    def compute(obj1, obj2):
        # return the forces acted on object one by object two
        # first check for possible collision

        pass

    def iterate_forces(self):

        apply = defaultdict(dict)

        for i in range(len(self.objects)):
            for j in range(1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]

                apply[obj1][obj2] = self.compute(obj1, obj2)
                apply[obj2][obj1] = self.compute(obj2, obj1)
        return apply

    @staticmethod
    def is_colliding(obj1, obj2):
        com1 = obj1.x,obj1.y
        com2 = obj2.x, obj2.y
        if distance(com1, com2) > obj1.radius + obj2.radius:
            return False
<<<<<<< HEAD
        pts1 = obj1.points
        pts2 = obj2.points
        # print("pts1",pts1)
        # print("x,y", com1)

        intersections = []

        for i1 in range(len(pts1)):
            l1 = [pts1[i1 - 1], pts1[i1]]
            # print("l1", l1)
            for i2 in range(len(pts2)):
                l2 = [pts2[i2 - 1], pts2[i2]]
                inters = segment_intersection((l1[0], l1[1]), (l2[0], l2[1]))
                if inters:
                    intersections.append(inters)
        return intersections
=======
        pts1 = self.points
        pts2 = obj.points
        # print("pts1", pts1)
        # print("pts1 (_points)", self._points)
        # print("x,y", com1)
        ary = []
        for i1 in range(len(pts1)):
            l1 = [pts1[i1],pts1[(i1+1)%len(pts1)]]
            # print("l1",l1)
            for i2 in range(len(pts2)):
                l2 = [pts2[i2], pts2[(i2+1)%len(pts2)]]
                # if l1 == [[4,0],[4,4]]:
                #     print("---")
                #     print("l1", l1)
                #     print("l2", l2)
                if utils.intersect(l1[0], l1[1], l2[0], l2[1]):
                    ary.append(utils.line_intersection((l1[0], l1[1]), (l2[0], l2[1])))
        return ary if len(ary) > 0 else False
>>>>>>> 7be688d775b52e0bb36bca2b4cd2e6ce79ffdb39
