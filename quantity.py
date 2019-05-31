from entity import Polygon
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

    def __init__(self, object: Polygon, force, n_ticks):
        """
        :param object:
        :param n_ticks:
        :param fx:
        :param fy:
        :param magnitude:
        :param target:
        """
        if n_ticks == 0: raise ValueError("duration of force cannot be 0")
        super(Force, self).__init__()
        self.obj = object

        if hasattr(force, '__call__'):
            self.frc_func = force
        else:
            self.frc_func = lambda: force

        self.n_ticks = n_ticks
        self.ticked = False

    def apply(self):
        # newton's second law
        vec = self.frc_func()
        if not self.ticked:
            self.ticked = True
        else:
            self.obj.a -= vec
        if not self.n_ticks: return False

        m = self.obj.m

        self.ax = fx / m
        self.ay = fy / m

        self.obj.ax += self.ax
        self.obj.ay += self.ay
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


class Gravity(Force):
    """
    Gravity(obj1, obj2)
    :returns force on obj1 by obj2
    """
    def __init__(self, obj1, obj2):
        def gen_frc():

            x, y = obj1.x - obj2.x
            r = obj1.x.distance(obj2.x)
            magnitude = G * obj1.m * obj2.m / (r**2)

            fx = x / r * magnitude
            fy = y / r * magnitude

            return fx, fy

        super(Gravity, self).__init__(obj1, gen_frc, float('inf'))


class VarForce(Force):

    def __init__(self, object: Polygon, app_tuple):

        self.i = iter(app_tuple)

        def frc_func():
            return next(self.i)

        super(VarForce, self).__init__(object, frc_func(), len(app_tuple))
