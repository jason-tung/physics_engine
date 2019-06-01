from collections import defaultdict
from maths.geometry import segment_intersection
from backend.entity import Polygon
from backend.quantity import Force, Torque
from maths.vector import Vector2D
from math import sin, cos
from itertools import chain
from debug_tools.collision import assert_collisions
from functools import lru_cache
from collections import deque

class Handler:

    def __init__(self, world):
        # enqueue all lasting forces here
        # for each object compute all forces acting on it
        # get a net force
        self.objects = []
        self.world = world
        self.ledger = deque(maxlen=5)

    def tick(self):
        return self.iterate_forces()

    @staticmethod
    def compute(obj1: Polygon, obj2: Polygon):
        # return the forces acted on object one by object two
        # first check for possible collision

        inters = obj1.intersections(obj2)

        if not inters:
            return None, None
        else:
            point = sum(inters) / len(inters)
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
                w = opp.magnitude() / (obj.x-point).magnitude()
                if point.y > obj.x.y:
                    if point.x < 0:
                        w *= -1
                else:
                    if point.x > 0:
                        w *= -1
                return v_vec, w



            # w1_f = (obj1.m - obj2.m) / m * w1 + (2 * obj2.m) / m * w2
            # w2_f = (2 * obj1.m) / m * w1 + (obj1.m - obj2.m) / m * w2

            print('\n\n\nCOLLISION\n', obj1, obj2, v1_f, v2_f, '\n\n\n')
            if v1_f == v1 or v2_f == v2:
                return None, None
            collision_time = max(obj1.col_ticks, obj2.col_ticks)

            def decompose(obj, force_vec, point):
                # print(force_vec)
                ang = force_vec.angle(obj.x - point)
                dist = point.distance(obj.x)
                a, b = obj.velocity(point)
                t_magnitude = 1 if a * b < 0 else -1
                t_magnitude *= force_vec.magnitude() * dist * sin(ang) / obj.radius * 0.17
                f_vec = force_vec * cos(ang)

                return f_vec, t_magnitude



            f1, t1 = decompose(obj1, obj1.m * (v1_f - v1) / collision_time, point)
            f2, t2 = decompose(obj2, obj2.m * (v2_f - v2) / collision_time, point)

            # obj1.v += f1 * obj1.loss / obj1.m
            # obj2.v += f2 * obj2.loss / obj2.m

            v1, w1 = decomp(obj1, v1_f, point)
            v2, w2 = decomp(obj2, v2_f, point)

            obj1.v = v1 * obj1.loss
            obj2.v = v2 * obj2.loss
            print(obj1.v, obj2.v)

            obj1.w = w1 * obj1.loss
            obj2.w = w2 * obj2.loss

            #print)obj1.w

            if f1.magnitude() > f2.magnitude():
                f1 = -f2
            # f1 = min(f1, f2, key = lambda x: x.magnitude())
            # print(t1, t2)
            return (Force(obj1, f1, collision_time, applier=obj2),
                    Torque(obj1, abs(t1), 1 if t1 > 0 else -1, collision_time, applier=obj2)), \
                   (Force(obj2, -f1, collision_time, applier=obj1),
                    Torque(obj2, abs(t1), -1 if t1 > 0 else 1, collision_time, applier=obj1))

    def iterate_forces(self):

        apply = defaultdict(dict)
        collided = set()

        for i in range(len(self.objects)):
            update_fail = False
            for v_vect, w in [(self.objects[i].v, self.objects[i].w),
                              (Vector2D(), self.objects[i].w),
                              (self.objects[i].v, 0)]:
                # print(self.objects)
                assert_collisions(self.objects)
                orig_x = self.objects[i].x
                orig_o = self.objects[i].o
                self.objects[i].x += v_vect
                self.objects[i].o += w
                collision = False
                obj1 = self.objects[i]
                for j in range(len(self.objects)):
                    if i == j:
                        continue
                    obj2 = self.objects[j]

                    a, b = self.compute(obj1, obj2)
                    print(a, b)
                    #print(a, b, i, j)
                    # if a: print(a, b), i, j, update_fail
                    if a:
                        collision = True
                        collided.add(self.objects[i])
                        collided.add(self.objects[j])
                    if a and not update_fail and obj2 not in apply[obj1]:
                        apply[obj1][obj2] = a
                        apply[obj2][obj1] = b
                        collision = True

                if collision:
                    self.objects[i].x = orig_x
                    self.objects[i].o = orig_o
                    assert_collisions(self.objects)
                    update_fail = True
                else:
                    break
            # if collision:
            #     self.objects[i].v *= 1
            #     self.objects[i].w *= 1

        print(apply)

        assert_collisions(self.objects)


        self.ledger.append(collided)

        return [k for i in apply.values() for j in i.values() for k in j]

    def equilibrium(self):
        if len(self.ledger) > 5:
            for obj in self.objects:
                if all(obj in col for col in self.ledger):
                    obj.w /= 1
                    obj.v /= 1
