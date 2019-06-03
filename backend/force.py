from backend.maths.vector import Vector2D
from constants import G


class Force:
    """
    Template for a force acting on object
    """

    def __init__(self, object):
        self.object = object
        self.object.forces.append(self)

    def __call__(self):
        return Vector2D()

    def __repr__(self):
        pass


class Gravity(Force):

    def __init__(self, obj1, obj2):
        """
        Create the force acting on obj1 by obj2
        :param obj1: Object force acts on
        :param obj2: Object "creating" the force
        """
        if obj1 == obj2: raise EnvironmentError("objects are the same")
        super(Gravity, self).__init__(obj1)

        self.obj1 = obj1
        self.obj2 = obj2

    def __call__(self):

        obj1, obj2 = self.obj1, self.obj2

        r = obj1.x.distance(obj2.x)
        magnitude = G * obj1.m * obj2.m / (r ** 2)

        return (obj2.x - obj1.x) / r * magnitude


class ConstantForce(Force):

    def __init__(self, object, frc, n_ticks):
        super(ConstantForce, self).__init__(object)
        self.force = frc
        self.n_ticks = n_ticks

    def __call__(self):
        if not self.n_ticks:
            return None
        self.n_ticks -= 1
        return self.force


class VarForce(Force):

    def __init__(self, object, force_iterable):
        super(VarForce, self).__init__(object)
        self.res = iter(force_iterable)

    def __call__(self):

        try:
            return next(self.res)
        except StopIteration:
            return None


class Torque:
    """
    Template for a torque acting on object
    """

    def __init__(self, object):
        self.object = object
        self.object.torques.append(self)

    def __call__(self):
        return 0

    def __repr__(self):
        pass


class ConstantTorque:

    def __init__(self, object, torque, n_ticks):
        super(ConstantTorque, self).__init__(object)
        self.torque = torque
        self.n_ticks = n_ticks

    def __call__(self):
        if not self.n_ticks:
            return None
        self.n_ticks -= 1
        return self.torque


class VarTorque(Force):

    def __init__(self, object, torque_iterable):
        super(VarTorque, self).__init__(object)
        self.res = iter(torque_iterable)

    def __call__(self):

        try:
            return next(self.res)
        except StopIteration:
            return None


def gen_gravs(objs):
    return [Gravity(objs[i], objs[j]) for i in range(len(objs)) for j in range(len(objs)) if i != j]

