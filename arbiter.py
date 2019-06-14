from collide import collide, FeaturePair
from body import Body
from maths import clamp
from config import POSITION_CORRECTION, WARM_STARTING, ACCUMULATE_IMPULSES

MAX_POINTS = 2


class Contact:

    def __init__(self):
        self.position = None
        self.normal = None
        self.r1 = None
        self.r2 = None
        self.separation = 0
        self.pn = 0
        self.pt = 0
        self.pnb = 0
        self.mass_normal = 0
        self.mass_tangent = 0
        self.bias = 0
        self.feature = FeaturePair()


def arbiter_key(b1, b2):
    if b1.mass < b2.mass:
        return (b1, b2)
    else:
        return (b2, b1)


class Arbiter:

    def __init__(self, b1, b2):

        if b1.mass < b2.mass:
            self.b1 = b1
            self.b2 = b2
        else:
            self.b1 = b2
            self.b2 = b1

        self.contacts = [Contact() for _ in range(MAX_POINTS)]

        self.num_contacts = collide(self.contacts, self.b1, self.b2)
        print('resolved', self.num_contacts)
        self.friction = (self.b1.friction * self.b2.friction)**0.5

    def update(self, new_contacts, num_new_contacts):
        merged_contacts = [Contact() for _ in range(MAX_POINTS)]

        for i in range(num_new_contacts):

            cNew = new_contacts[i] # should be a pointer
            k = -1
            for j in range(self.num_contacts):
                cOld = self.contacts[j]
                if cNew.feature.val == cOld.feature.val:
                    k = j
                    break
            if k > -1:
                c = merged_contacts[i]
                cOld = self.contacts[k]
                merged_contacts[i] = cNew

                if WARM_STARTING:
                    c.pn = cOld.pn
                    c.pt = cOld.pt
                    c.pnb = cOld.pnb
                else:
                    c.pn = 0
                    c.pt = 0
                    c.pnb = 0
            else:
                merged_contacts[i] = new_contacts[i]

        for i in range(num_new_contacts):
            self.contacts[i] = merged_contacts[i]

        self.num_contacts = num_new_contacts

    def pre_step(self, inv_dt):
        k_allowed_penetration = 0.01
        k_bias_factor = 0.2 if POSITION_CORRECTION else 0

        for i in range(self.num_contacts):

            c = self.contacts[i]
            print(sorted(c.__dict__.keys()))
            r1 = c.position - self.b1.position
            r2 = c.position - self.b2.position

            rn1 = r1 * c.normal
            rn2 = r2 * c.normal

            kNormal = self.b1.inv_mass + self.b2.inv_mass
            kNormal += self.b1.invI * (r1 * r1 - rn1 * rn1) + self.b2.invI * (r2 * r2 - rn2 * rn2)

            c.mass_normal = 1 / kNormal

            tangent = c.normal.cross(1)
            rt1 = r1 * tangent
            rt2 = r2 * tangent
            kTangent = self.b1.inv_mass + self.b2.inv_mass
            kTangent += self.b1.invI * (r1 * r1 - rt1 * rt1) + self.b2.invI * (r2 * r2 - rt2 * rt2)

            c.mass_tangent = 1 / kTangent
            c.bias = -k_bias_factor * inv_dt * min(0, c.separation + k_allowed_penetration)

            if ACCUMULATE_IMPULSES:
                P = c.pn * c.normal + c.pt * tangent
                self.b1.velocity -= self.b1.inv_mass * P
                self.b1.angular_velocity -= self.b1.invI *  r1.cross(P)

                self.b2.velocity += self.b2.inv_mass * P
                self.b2.angular_velocity += self.b2.invI * r2.cross(P)

    def apply_impulse(self):

        print('IMPULSE APPLIED\n\n\n\n')

        b1 = self.b1
        b2 = self.b2

        for i in range(self.num_contacts):

            c = self.contacts[i]
            c.r1 = c.position - b1.position
            c.r2 = c.position - b2.position

            dv = b2.velocity - c.r2.cross(b2.angular_velocity) - b1.velocity + c.r1.cross(b1.angular_velocity)

            vn = dv * c.normal

            dPn = c.mass_normal * (-vn + c.bias)

            if ACCUMULATE_IMPULSES:
                Pn0 = c.pn
                c.pn = max(Pn0 + dPn, 0)
                dPn = c.pn - Pn0
            else:
                dPn = max(dPn, 0)

            Pn = dPn * c.normal

            b1.velocity -= b1.inv_mass * Pn
            b2.angular_velocity -= b1.invI * c.r1.cross(Pn)

            b2.velocity += b2.inv_mass * Pn
            b2.angular_velocity += b2.invI * c.r2.cross(Pn)

            tangent = c.normal.cross(1)
            vt = dv * tangent
            dPt = c.mass_tangent * (-vt)
            print(c.normal, dPn, tangent)
            print(dPt, c.mass_tangent, -vt)
            if ACCUMULATE_IMPULSES:

                maxPt = self.friction * c.pn
                oldTangentImpulse = c.pt
                c.pt = clamp(oldTangentImpulse + dPt, -maxPt, maxPt)
                dPt = c.pt - oldTangentImpulse
            else:
                maxPt = self.friction * dPn
                dPt = clamp(dPt, -maxPt, maxPt)
            print('what the fuck', tangent, dPt)
            Pt = dPt * tangent
            # print('impulse', Pt)
            b1.velocity -= b1.inv_mass * Pt
            b1.angular_velocity -= b1.invI * c.r1.cross(Pt)

            b2.velocity += b2.inv_mass * Pt
            b2.angular_velocity += b2.invI * c.r2.cross(Pt)
