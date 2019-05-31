from backend.collision_handler import Handler
from frontend.canvas import Canvas
from math import sin, cos
from heapq import *
from config import AUTO_ZOOM
from backend.quantity import *


class World:

    def __init__(self):

        self.objects = []
        self.canvas = Canvas()
        self.handler = Handler()
        self.handler.objects = self.objects
        self.heap = []
        self.tick = 0

    def add_heap_unit(self, quantity: [Torque, Force]):
        # print(quantity, type(quantity))
        print(self.heap)
        if isinstance(quantity, Torque):
            if quantity.t == 0:
                return
        else:
            if quantity.frc_func().magnitude() == 0:
                return

        if False and quantity.applier:
            this = (quantity.obj, quantity.applier, quantity.__class__)

            for _, qnt in self.heap:
                print(self.heap)
                print((qnt.obj, qnt.applier, quantity.__class__), quantity)
                print(this, quantity)
                if this == (qnt.obj, qnt.applier, quantity.__class__):
                    print('broken', self.heap)
                    break
            else:
                heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

        else:
            heappush(self.heap, (self.tick + quantity.n_ticks, quantity))

        print('FINAL', self.heap)

    def tick_forces(self):

        for _, i in self.heap:
            i.apply()
            #print(i.__dict__)

        while self.heap and self.heap[0][0] <= self.tick:
            #print(self.heap[0][0], self.tick)
            _, quantity = heappop(self.heap)
            quantity.apply()

    def add_object(self, obj):
        self.objects.append(obj)

    def rebuild_canvas(self):
        self.canvas.build(self.objects)

    def mainloop(self):
        while True:
            print('\n', self.tick, '\n')

            self.tick_forces()

            print(self.heap)

            if AUTO_ZOOM:
                self.canvas.build(self.objects)
            for i in self.objects:
                print(i.__dict__)

            for frc in self.handler.tick():
                self.add_heap_unit(frc)
            self.canvas.update()
            self.tick += 1


if __name__ == '__main__':
    from backend.quantity import Gravity
    from maths.vector import Vector2D
    w = World()
    p1 = Polygon(1000, [(0, 0), (4, 0), (4, 4), (0, 4)])
    p2 = Polygon(10**5, [(2, 3.5), (-1, 9), (2, 9), (5, 6)])
    p3 = Polygon(1, [(50, 50), (51, 50), (50, 51)])
    points = []
    radius = 3
    n_sides = 50
    from math import pi
    for theta in range(0, 360, 360//n_sides):
        points.append([cos(pi/180 * theta) * radius + 10, sin(pi/180 * theta) * radius + 10])

    p2 = Polygon(10**10, points)


    #p3 = Polygon(1000000000000, [(20, 5), (21, 5), (21, 6), (20, 6)])
    t = Torque(p1, 10, 1, 10)
    g = Gravity(p1, p2)
    p1.v = Vector2D(0, 0)
    w.add_heap_unit(g)
    w.add_heap_unit(t)
    for i in [p1, p2, p3]:
        w.add_object(i)
    print(p1.points)
    print(p2.points)
    print("what?")
    w.rebuild_canvas()
    w.mainloop()