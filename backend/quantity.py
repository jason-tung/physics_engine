from backend.entity import Polygon
from constants import G


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

    def __init__(self, object, force, n_ticks, applier=None):

        if n_ticks == 0:
            raise ValueError("duration of force cannot be 0")
        super(Force, self).__init__()
        self.obj = object
        self.applier = applier

        if hasattr(force, '__call__'):
            self.frc_func = force
        else:
            self.frc_func = lambda: force

        self.n_ticks = n_ticks

    def apply(self):
        # newton's second law
        if not self.n_ticks:
            return False
        vec = self.frc_func()
       # print(vec, self.n_ticks)
        self.obj.v += vec / self.obj.m
        self.n_ticks -=1
        return True

    def __repr__(self):
        return str(self.frc_func())


class Torque(Quantity):

    def __init__(self, object: Polygon, magnitude, direction, n_ticks, applier=None):
        super(Torque, self).__init__()
        # direction == 1 -> clockwise
        # direction == -1 -> counter clockwise

        self.obj = object
        self.t = magnitude * direction
        self.n_ticks = n_ticks
        self.applier = applier

    def apply(self):
        # torque = I * alpha
        if not self.n_ticks:
            return False
        self.obj.w += self.t / self.obj.i
        self.n_ticks -= 1
        return True

    def __repr__(self):
        return f'T<{self.t}>'


class Gravity(Force):
    """
    Gravity(obj1, obj2)
    :returns force on obj1 by obj2
    """

    def __init__(self, obj1, obj2):
        def gen_frc():
            r = obj1.x.distance(obj2.x)
            magnitude = G * obj1.m * obj2.m / (r ** 2)

            return (obj2.x - obj1.x) / r * magnitude

        super(Gravity, self).__init__(obj1, gen_frc, float('inf'))


class VarForce(Force):

    def __init__(self, object: Polygon, app_tuple):
        self.i = iter(app_tuple)

        def frc_func():
            return next(self.i)

        super(VarForce, self).__init__(object, frc_func(), len(app_tuple))


def gen_gravs(objs):
    return [Gravity(objs[i], objs[j]) for i in range(len(objs)) for j in range(len(objs)) if i != j]

