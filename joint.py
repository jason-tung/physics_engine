from vector import Matrix22, Vector2D
from config import WARM_STARTING, POSITION_CORRECTION


class Joint:

    def __init__(self):

        self.b1 = None
        self.b2 = None
        self.M = Matrix22()
        self.local_anchor1 = None
        self.local_anchor2 = None
        self.r1 = Vector2D()
        self.r2 = Vector2D()
        self.bias = Vector2D()
        self.P = Vector2D()

        self.biasfactor = 0
        self.softness = 0.2

    def set(self, b1, b2, anchor):

        self.b1 = b1
        self.b2 = b2

        Rot1 = Matrix22(b1.rotation)
        Rot2 = Matrix22(b2.rotation)
        Rot1T = Rot1.transpose()
        Rot2T = Rot2.transpose()
        print(Rot1T, anchor - b1.position)
        self.local_anchor1 = Rot1T * (anchor - b1.position)
        self.local_anchor2 = Rot2T * (anchor - b2.position)

    def pre_step(self, inv_dt):

        Rot1 = Matrix22(self.b1.rotation)
        Rot2 = Matrix22(self.b2.rotation)

        self.r1 = Rot1 * self.local_anchor1
        self.r2 = Rot2 * self.local_anchor2

        K1 = Matrix22(
            Vector2D(self.b1.inv_mass + self.b2.inv_mass,
                     0),
            Vector2D(0,
                     self.b1.inv_mass + self.b2.inv_mass)
        )

        K2 = Matrix22(
            Vector2D(self.b1.invI * self.r1.y * self.r1.y,
                     -self.b1.invI * self.r1.x * self.r1.y),
            Vector2D(-self.b1.invI * self.r1.x * self.r1.y,
                     self.b1.invI * self.r1.x * self.r1.x)
        )

        K3 = Matrix22(
            Vector2D(self.b1.invI * self.r2.y * self.r2.y,
                     -self.b2.invI * self.r2.x * self.r2.y),
            Vector2D(-self.b1.invI * self.r2.x * self.r2.y,
                     self.b2.invI * self.r2.x * self.r2.x)
        )

        K = K1 + K2 + K3

        K.col1.x += self.softness
        K.col2.y += self.softness

        self.M = K.invert()

        p1 = self.b1.position + self.r1
        p2 = self.b2.position + self.r2
        dp = p2 - p1

        if POSITION_CORRECTION:
            self.bias = -self.biasfactor * inv_dt * dp
        else:
            self.bias = Vector2D()

        if WARM_STARTING:

            self.b1.velocity -= self.b1.inv_mass * self.P
            self.b1.angular_velocity -= self.b1.invI * self.r1.cross(self.P)

            self.b2.velocity += self.b2.inv_mass * self.P
            self.b2.angular_velocity += self.b2.invI * self.r2.cross(self.P)
        else:
            self.P = Vector2D()

    def apply_impulse(self):

        dv = self.b2.velocity - self.r2.cross(self.b2.angular_velocity) - self.b1.velocity + self.r1.cross(self.b1.angular_velocity)
        impulse = self.M * (self.bias - dv - self.softness * self.P)

        self.b1.velocity -= self.b1.inv_mass * impulse
        self.b1.angular_velocity -= self.b1.invI * self.r2.cross(impulse)

        self.P += impulse
