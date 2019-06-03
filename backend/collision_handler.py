from backend.entity import Polygon
from backend.maths.vector import Vector2D
from backend.convex.collision import broad_sweep
from time import time
from config import collision_epsilon
from backend.convex.gjk import collide_poly_poly


class Handler:

    def __init__(self, world):
        # enqueue all lasting forces here
        # for each object compute all forces acting on it
        # get a net force
        self.world = world
        self.objects = world.objects

    def tick(self):
        return self.iterate_forces()

    @staticmethod
    def compute(obj1: Polygon, obj2: Polygon, point):
        # return the forces acted on object one by object two
        # first check for possible collision
        m = obj1.m + obj2.m

        v1 = obj1.velocity(point)
        v2 = obj2.velocity(point)

        # assume the collision is elastic
        # velocities now must be decomposed into v_com and v_point
        # for now decompose everything into v_com

        v1_f = (obj1.m - obj2.m) / m * v1 + (2 * obj2.m) / m * v2
        v2_f = (2 * obj1.m) / m * v1 + (obj1.m - obj2.m) / m * v2

        def decomp(obj, vec, point):
            v_vec = obj.v.project(vec)
            opp = vec - v_vec
            w = opp.magnitude() / (obj.x - point).magnitude()
            if point.y > obj.x.y:
                if point.x < 0:
                    w *= -1
            else:
                if point.x > 0:
                    w *= -1
            return vec, w * 0

        # w1_f = (obj1.m - obj2.m) / m * w1 + (2 * obj2.m) / m * w2
        # w2_f = (2 * obj1.m) / m * w1 + (obj1.m - obj2.m) / m * w2

        if obj1.m > 10:
            # print('\n\n\nCOLLISION\n', obj1, obj2, v1_f, v2_f, '\n\n\n')
            pass
        # if v1_f == v1 or v2_f == v2:
        #     return False
        # collision_time = max(obj1.col_ticks, obj2.col_ticks)

        # obj1.v += f1 * obj1.loss / obj1.m
        # obj2.v += f2 * obj2.loss / obj2.m

        v1, w1 = decomp(obj1, v1_f, point)
        v2, w2 = decomp(obj2, v2_f, point)

        obj1.v = v1 * obj1.loss
        obj2.v = v2 * obj2.loss
        if obj1.m > 10:
            # print(obj1.v, obj2.v)
            pass
        obj1.w = w1 * obj1.loss
        obj2.w = w2 * obj2.loss

        return True

    def iterate_forces(self):
        objs = self.objects

        # all_inter = broad_sweep(objs)
        for i in range(len(objs)):
            # print(objs)
            if objs[i].static: continue
            objs[i].x += objs[i].v
            objs[i].o += objs[i].w
            # collision = False
            # obj1 = objs[i]
            # for j in range(len(objs)):
            #     if i == j:
            #         continue
            #     obj2 = objs[j]
            #     collision |= self.compute(obj1, obj2)
            # if collision:
            #     objs[i].x = orig_x
            #     objs[i].o = orig_o
            # else:
            #     break
        b = [list(i) for i in broad_sweep(objs)]
        print('SWEPT', b)
        res = []

        for a, b in b:
            d = a.distance(b)
            if d[0] <= collision_epsilon:
                res.append([a, b, d[1]])

        for a, b, c in res:
            if not a.static:
                a.x -= a.v
                a.o -= b.w
            self.compute(a, b, (c[0] + c[1][0] + c[1][1]) / 3)
