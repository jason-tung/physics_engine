from collision_handler import Handler
from canvas import Canvas
from math import sin, cos
from entity import Polygon
from heapq import *
from config import AUTO_ZOOM
from quantity import *


class World:

    def __init__(self):

        self.objects = []
        self.canvas = Canvas()
        self.handler = Handler()
        self.handler.objects = self.objects
        self.heap = []
        self.tick = 0

    def add_heap_unit(self, quantity: Quantity):
        heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

    def tick_forces(self):

        for _, i in self.heap:
            i.apply()
            print(i.__dict__)

        while self.heap and self.heap[0][0] <= self.tick:
            print(self.heap[0][0], self.tick)
            _, quantity = heappop(self.heap)

    def tick_velocities(self):
        for i in self.objects:
            i.tick_velocities()

    def add_object(self, obj):
        self.objects.append(obj)

    def rebuild_canvas(self):
        self.canvas.build(self.objects)

    def mainloop(self):
        while True:
            self.tick_forces()
            self.tick_velocities()

            if AUTO_ZOOM: self.canvas.build(self.objects)
            for i in self.objects:
                if i.m == 1000:
                    pass
                    # print(i.ax, i.ay)

                self.handler.tick()
            self.canvas.update()
            self.tick += 1


if __name__ == '__main__':
    from quantity import Gravity
    from maths.vector import Vector2D
    w = World()
    p1 = Polygon(1000, [(0, 0), (4, 0), (4, 4), (0, 4)])
    p2 = Polygon(10**5, [(2, 3.5), (-1, 9), (2, 9), (5, 6)])
    points = []
    radius = 3
    n_sides = 300
    from math import pi
    for theta in range(0, 360, 360//n_sides):
        points.append([cos(pi/180 * theta) * radius + 10, sin(pi/180 * theta) * radius + 10])

    p2 = Polygon(10**10, points)


    #p3 = Polygon(1000000000000, [(20, 5), (21, 5), (21, 6), (20, 6)])
    t = Torque(p1, 1, 1, 10)
    g = Gravity(p1, p2)
    p1.v = Vector2D(0.15, 0)
    w.add_heap_unit(g)
    w.add_heap_unit(t)
    for i in [p1, p2]:
        w.add_object(i)
    print(p1.points)
    print(p2.points)
    print("what?")
    w.rebuild_canvas()
    w.mainloop()