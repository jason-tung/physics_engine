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

    def tick(self):
        for i in self.objects:
            i.x += i.vx
            i.y += i.vy
            i.o += i.w

    @staticmethod
    def compute(obj1, obj2):
        # return the forces acted on object one by object two
        # first check for possible collision

        inters = Handler.collisions(obj1, obj2)
        if not inters:
            return None, None
        else:
            pass


        pass

    @staticmethod
    def collisions(obj1, obj2):
        com1 = obj1.x,obj1.y
        com2 = obj2.x, obj2.y
        if distance(com1, com2) > obj1.radius + obj2.radius:
            return []
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

    def iterate_forces(self):

        apply = defaultdict(list)

        for i in range(len(self.objects)):
            for j in range(1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]

                a, b = self.compute(obj1, obj2)
                if a:
                    apply[obj1].append(a)
                    apply[obj2].append(b)

        return apply