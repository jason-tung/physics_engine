from collections import deque, defaultdict
from heapq import *
from config import collide_epsilon


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

