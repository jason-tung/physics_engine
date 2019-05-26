from collision_handler import Handler
from canvas import Canvas
from math import sin, cos
from entity import Polygon
from utils import distance
from heapq import *


class Quantity:
    def __init__(self):
        self.n_ticks = None

    def apply(self):
        pass

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __eq__(self, other):
        return True


class Force(Quantity):

    def __init__(self, object: Polygon, fx, fy, n_ticks):
        if n_ticks == 0: raise ValueError("duration of force cannot be 0")
        super(Force, self).__init__()
        self.obj = object
        self.fx = fx
        self.fy = fy
        self.n_ticks = n_ticks
        self.ticked = False

    def apply(self):
        # newton's second law
        if not self.n_ticks:
            self.obj.ax -= self.ax
            self.obj.ay -= self.ay
            return False
        if not self.ticked:
            m = self.obj.m

            self.ax = self.fx / m
            self.ay = self.fy / m

            self.obj.ax += self.ax
            self.obj.ay +=self. ay

            self.ticked = True

        self.n_ticks -=1
        return True


class Torque(Quantity):

    def __init__(self, object: Polygon, magnitude, direction, n_ticks):
        super(Torque, self).__init__()
        # direction == 1 -> clockwise
        # direction == -1 -> counter clockwise

        self.obj = object
        self.t = magnitude * direction
        self.n_ticks = n_ticks
        self.ticked = False

    def apply(self):
        # torque = I * alpha
        if not self.n_ticks:
            self.obj.a -= self.alpha
            return False
        if not self.ticked:
            i = self.obj.i
            self.alpha = self.t / i

            self.obj.a += self.alpha
            self.ticked = True

        self.n_ticks -= 1
        return True


class World:

    def __init__(self):

        self.objects = []
        self.canvas = Canvas()
        self.handler = Handler()
        self.handler.objects = self.objects
        self.heap = []
        self.tick = 0

    def add_heap_unit(self, quantity:Quantity):
        t = self.tick
        heappush(self.heap, (t + 1, quantity))

    def tick_forces(self):
        t = self.tick
        while self.heap and self.heap[0][0] <= self.tick:
            _, quantity = heappop(self.heap)
            if quantity.apply():
                heappush(self.heap, (t + 1, quantity))

    def tick_velocities(self):
        for i in self.objects:
            i.tick_velocities()

    def add_object(self, obj):
        self.objects.append(obj)

    def add_quantity(self, quantity):
        heappush(self.heap, (self.tick + 1, quantity))

    def rebuild_canvas(self):
        self.canvas.build(self.objects)

    def mainloop(self):
        while True:
            self.tick_forces()
            self.tick_velocities()
            for i in self.objects:
                i.tick_movement_no_collisions()
            self.canvas.update()
            self.tick += 1

if __name__ == '__main__':
    w = World()
    p1 = Polygon(1000, [(0, 0), (4, 0), (4, 4), (0, 4)])
    p2 = Polygon(1000, [(2, 3.5), (-1, 9), (2, 9), (5, 6)])

    f = Force(p1, 10, 5, 10)
    t = Torque(p1, 10, 1, 10)
    f1 = Force(p1, 10, -2.5, 20)
    t1 = Torque(p1, 5, -1, 10)
    w.add_quantity(f)
    w.add_quantity(t)
    w.add_quantity(f1)
    w.add_quantity(t1)
    p1.o, p2.o = 0, 0
    for i in [p1, p2]:
        w.add_object(i)
    w.rebuild_canvas()
    w.mainloop()

