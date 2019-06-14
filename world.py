from body import Body
from joint import Joint
from arbiter import Arbiter, arbiter_key
from canvas import Canvas


class World:

    def __init__(self, gravity, iterations):
        self.gravity = gravity
        self.iterations = iterations
        self.bodies = []
        self.joints = []
        self.arbiters = {}
        self.canvas = Canvas()

    def clear(self):

        self.bodies = []
        self.joints = []
        self.arbiters = {}

    def add(self, other):
        # print(type(other))
        if type(other) == Body:
            self.bodies.append(other)
        elif type(other) == Joint:
            self.joints.append(other)
        else:
            assert False

    def broad_phase(self):

        for i in range(len(self.bodies)):

            bi = self.bodies[i]

            for j in range(i+1, len(self.bodies)):

                bj = self.bodies[j]

                if bi.inv_mass == 0 and bj.inv_mass == 0:
                    continue

                newArb = Arbiter(bi, bj)
                key = arbiter_key(bi, bj)
                if newArb.num_contacts > 0:

                    if key not in self.arbiters:
                        self.arbiters[key] = newArb
                    else:
                        self.arbiters[key].update(newArb.contacts, newArb.num_contacts)
                else:
                    # print(key == list(self.arbiters.keys())[0])
                    # print(key in self.arbiters.keys())
                    if key in self.arbiters:
                        print('tried')
                        del self.arbiters[key]

    def step(self, dt):
        self.canvas.build(self.bodies)
        self.canvas.update()

        inv_dt = 1 / dt if dt > 0 else 0

        self.broad_phase()

        for i in range(len(self.bodies)):
            b = self.bodies[i]

            if b.inv_mass == 0:
                continue

            b.velocity += dt * (self.gravity + b.inv_mass * b.force)
            b.angular_velocity += dt * b.invI * b.torque
        print(list(self.arbiters.values()))
        for arb in self.arbiters.values():
            arb.pre_step(inv_dt)

        for joint in self.joints:
            joint.pre_step(inv_dt)
        for i in range(self.iterations):

            for arb in self.arbiters.values():
                arb.apply_impulse()

            for joint in self.joints:
                joint.apply_impulse()

        for b in self.bodies:
            if b.mass == 10000:
                ...
                # continue

            b.position += dt * b.velocity
            b.rotation += dt * b.angular_velocity
            b.force.set(0, 0)
            b.torque = 0


if __name__ == '__main__':

    from vector import Vector2D

    w = World(Vector2D(0, -2), 100)
    b1 = Body(10000, Vector2D(50, 40))

    b1.position = Vector2D(0, -0.5 * b1.width.y)
    b1.rotation = -0.1
    w.add(b1)

    b2 = Body(10, Vector2D(10, 10))
    b2.velocity = Vector2D(0, -1)
    b2.position = Vector2D(0, 30)
    w.add(b2)

    # j = Joint()
    # j.set(b1, b2, Vector2D(0, 11))
    # w.add(j)

    for i in range(1000000):
        # print(w.arbiters)
        # print(b2.position, b1.position)
        w.step(0.1)
