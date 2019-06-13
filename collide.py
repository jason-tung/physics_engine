from vector import Matrix22, Vector2D

NO_EDGE = 0
EDGE3 = 3
EDGE4 = 4
EDGE2 = 2
EDGE1 = 1

FACE_A_X = 5
FACE_A_Y = 6
FACE_B_X = 7
FACE_B_Y = 8


class FeaturePair:

    class Edges:

        def __init__(self):
            self.in1 = None
            self.out1 = None
            self.in2 = None
            self.out2 = None

    def __init__(self):
        self.val = 0
        self.e = self.Edges()


class ClipVertex:

    def __init__(self):
        self.v = Vector2D()
        self.fp = FeaturePair()

    def set(self, v, fp):
        self.v = v
        self.fp = fp


def flip(fp):

    fp.e.in1, fp.e.in2 = fp.e.in2, fp.e.in1
    fp.e.out1, fp.e.out2 = fp.e.out2, fp.e.out1


def clip_segment_to_line(vout, vin, normal, offset, clipedge):

    numout = 0

    d0 = normal * vin[0].v - offset
    d1 = normal * vin[1].v - offset

    if d0 <= 0:
        vout[numout] = vin[0]
        numout += 1
    if d1 <= 0:
        vout[numout] = vin[1]
        numout += 1

    if d0 * d1 < 0:

        interp = d0 / (d0 - d1)
        vout[numout].v = vin[0].v + interp * (vin[1].v - vin[0].v)

        if d0 > 0:
            vout[numout].fp = vin[0].fp
            vout[numout].fp.e.in1 = clipedge
            vout[numout].fp.e.in2 = NO_EDGE

        else:

            vout[numout].fp = vin[1].fp
            vout[numout].fp.e.out1 = clipedge
            vout[numout].fp.e.out2 = NO_EDGE
        numout += 1
    return numout


def compute_incident_edge(c, h, pos, rot, normal):
    # print('compute_incident_edge', c)
    rotT = rot.transpose()
    n = -(rotT * normal)
    nabs = abs(n)

    if nabs.x > nabs.y:

        if n.x >= 0:
            c[0].v.set(h.x, -h.y)
            c[0].fp.e.in2 = EDGE3
            c[0].fp.e.out2 = EDGE4

            c[1].v.set(h.x, h.y)
            c[1].fp.e.in2 = EDGE4
            c[1].fp.e.out2 = EDGE1

        else:

            c[0].v.set(-h.x, h.y)
            c[0].fp.e.in2 = EDGE1
            c[0].fp.e.out2 = EDGE2

            c[1].v.set(-h.x, -h.y)
            c[1].fp.e.in2 = EDGE2
            c[1].fp.e.out2 = EDGE3

    else:

        if n.y >= 0:
            c[0].v.set(h.x, h.y)
            c[0].fp.e.in2 = EDGE4
            c[0].fp.e.out2 = EDGE1

            c[1].v.set(-h.x, h.y)
            c[1].fp.e.in2 = EDGE1
            c[1].fp.e.out2 = EDGE2
        else:
            c[0].v.set(-h.x, -h.y)
            c[0].fp.e.in2 = EDGE2
            c[0].fp.e.out2 = EDGE3

            c[1].v.set(h.x, -h.y)
            c[1].fp.e.in2 = EDGE3
            c[1].fp.e.out2 = EDGE4

    c[0].v = pos + rot * c[0].v
    c[1].v = pos + rot * c[1].v

    # c[0].v = pos + rot * c[0].v
    # print(pos, rot, c[1].v)
    # pos * rot
    # c[1].v = pos * rot * c[1].v


def collide(contacts, bodyA, bodyB):
    # print('called collide', contacts)
    hA = 0.5 * bodyA.width
    hB = 0.5 * bodyB.width

    posA = bodyA.position
    posB = bodyB.position

    RotA = Matrix22(bodyA.rotation)
    RotB = Matrix22(bodyB.rotation)

    RotAT = RotA.transpose()
    RotBT = RotB.transpose()

    dp = posB - posA
    dA = RotAT * dp
    dB = RotBT * dp

    C = RotAT * RotB
    absC = abs(C)
    absCT = absC.transpose()

    # print(dA, hA, absC, hB)
    faceA = abs(dA) - hA - absC * hB

    if faceA.x > 0 or faceA.y > 0:
        return 0

    faceB = abs(dB) - absCT * hA - hB
    if faceB.x > 0 or faceB.y > 0:
        return 0

    print(faceA.x, faceA.y, faceB.x, faceB.y)

    axis = FACE_A_X
    separation = faceA.x
    normal = RotA.col1 if dA.x > 0 else -RotA.col1

    relativeTol = 0.95
    absoluteTol = 0.01

    if faceA.y > relativeTol * separation + absoluteTol * hA.y:

        axis = FACE_A_Y
        separation = faceA.y
        normal = RotA.col2 if dA.y > 0 else -RotA.col2

    if faceB.x > relativeTol * separation + absoluteTol * hB.x:

        axis = FACE_B_X
        separation = faceB.x
        normal = RotB.col1 if dB.x > 0 else -RotB.col1

    if faceB.y > relativeTol * separation + absoluteTol * hB.y:

        axis = FACE_B_Y
        separation = faceB.y
        normal = RotB.col2 if dB.y > 0 else -RotB.col2

    incidentEdge = [ClipVertex() for _ in range(2)]

    if axis == FACE_A_X:
        frontNormal = normal
        front = posA * frontNormal + hA.x
        sideNormal = RotA.col2
        side = posA * sideNormal
        negSide = -side + hA.y
        posSide = side + hA.y
        negEdge = EDGE3
        posEdge = EDGE1
        compute_incident_edge(incidentEdge, hB, posB, RotB, frontNormal)
    elif axis == FACE_A_Y:
        frontNormal = normal
        front = posA * frontNormal + hA.y
        sideNormal = RotA.col1
        side = posA * sideNormal
        negSide = -side + hA.x
        posSide = side + hA.x
        negEdge = EDGE2
        posEdge = EDGE4
        compute_incident_edge(incidentEdge, hB, posB, RotB, frontNormal)
    ###

    elif axis == FACE_B_X:
        frontNormal = -normal
        front = posA * frontNormal + hB.x
        sideNormal = RotB.col2
        side = posB * sideNormal
        negSide = -side + hB.y
        posSide = side + hB.y
        negEdge = EDGE3
        posEdge = EDGE1
        compute_incident_edge(incidentEdge, hB, posB, RotB, frontNormal)
    elif axis == FACE_B_Y:
        frontNormal = -normal
        front = posB * frontNormal + hB.y
        sideNormal = RotB.col1
        side = posA * sideNormal
        negSide = -side + hB.x
        posSide = side + hB.x
        negEdge = EDGE2
        posEdge = EDGE4
        compute_incident_edge(incidentEdge, hB, posB, RotB, frontNormal)
    else:
        assert False

    cpoints1 = [ClipVertex(), ClipVertex()]
    cpoints2 = [ClipVertex(), ClipVertex()]

    np = clip_segment_to_line(cpoints1, incidentEdge, -sideNormal, negSide, negEdge)
    print(np)
    if np < 2:
        return 0

    np = clip_segment_to_line(cpoints2, cpoints1, sideNormal, posSide, posEdge)
    print(np)
    if np < 2:
        return 0

    num_contacts = 0

    for i in range(2):
        separation = (frontNormal * cpoints2[i].v) - front

        if separation <= 0:

            contacts[num_contacts].separation = separation
            contacts[num_contacts].normal = normal

            contacts[num_contacts].position = cpoints2[i].v - separation * frontNormal
            contacts[num_contacts].feature = cpoints2[i].fp

            if axis == FACE_B_X or axis == FACE_B_Y:
                flip(contacts[num_contacts].feature)
            num_contacts += 1
    # print(bodyA, bodyB, num_contacts)
    return num_contacts