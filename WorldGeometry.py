# -*- coding: utf-8 -*-

import math


class Vector(object):
    # Vector enthält punkte x,y,z
    # Vector enthält ebenfalls einen Tupel der Punkte (x,y,z)
    # safety first

    def __init__(self, vec, y=0, z=0):
        # Akzeptiert tuple und einzelne Werte
        # wenn vec ein tuple ist (x,y,z)
        if type(vec) is tuple:
            self.vec = vec
        else:
            self.vec = (vec, y, z)
        (self.x, self.y, self.z) = self.vec
        self.vec = tuple(map(float, self.vec))

    def __repr__(self):
        return 'Vector(%s, %s, %s)' % (repr(self.x), repr(self.y), repr(self.z))

    def __add__(self, v2):
        # vector1 + vector2
        assert (type(v2) == type(self))
        result = (self.x + v2.x, + self.y + v2.y, self.z + v2.z)
        return type(self)(result)

    def __sub__(self, v2):
        # vector1 - vector2
        assert (type(v2) == type(self))
        result = (self.x - v2.x, + self.y - v2.y, self.z - v2.z)
        return type(self)(result)

    def __div__(self, num):
        # Skalieren.
        assert (type(num) == int or type(num) == float)
        scaled_v = (self.x / num, self.y / num, self.z / num)
        # Tuple aus sklaierten vectorwerten casten zu vector
        return type(self)(scaled_v)

    def __mul__(self, num):
        # vector * saklierungswert = skalierter Vektor
        assert (type(num) == int or type(num) == float)
        scaled_v = (self.x * num, self.y * num, self.z * num)
        # Tuple aus sklaierten vectorwerten casten zu vector
        return type(self)(scaled_v)

    def __eq__(self, v2):
        return self.vec == v2.vec

    def length(self):
        # sqrt(x^2, y^2, z^2) = Länge des vectors
        vLenght = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return vLenght

    def dot(self, v2):
        #  scalar   =    x1 * x2   +   y1 * y2  +  z1 * z2
        assert (type(v2) == Vector)
        scalar = self.x * v2.x + self.y * v2.y + self.z * v2.z
        return scalar

    def cross(self, v2):
        # Kreuzprodukt siehe vorlesung oder formelsammlung
        # NICHT MIT PUUNKTEN !!!!
        assert (type(v2) == type(self))
        x = self.y * v2.z - self.z * v2.y
        y = self.z * v2.x - self.x * v2.z
        z = self.x * v2.y - self.y * v2.x
        return type(self)(x, y, z)

    def scale(self, scalar):

        return self * scalar

    def normalized(self):
        # vector Einheitsvektor hat die länge 1.
        # um einen normierten Vektor zu erhalten  v /||v||
        return self / self.length()

    def inversed(self):
        # vector ^(-1)
        v = tuple(map(lambda coord: 1.0 / coord, self.vec))
        return type(self)(v)

    def angle(self, v2):
        # alpha = acos ( <v1,v2> / ||v1|| * ||v2|| )
        return math.acos(self.dot(v2) / (self.length() * v2.length()))

    def reflect(self, vReflector):

        # vector und reflectionsVector Spannen eine Ebene auf
        # die aufgespannte ebene und der Reflectionsvetor spannen dann die Spiegelebene auf
        # print(vReflector)
        ebene = self.cross(vReflector)
        spiegel = ebene.cross(vReflector).normalized()
        d = self.cross(vReflector.normalized()).length()

        # hier sollte eigentlich ein minus hin aber ich weiss nicht warums mit Plus klappt
        # Folie 48 ?
        newDirection = self + spiegel * d * 2
        return type(self)(newDirection.vec)


class Point(object):

    def __init__(self, point, y=0, z=0):
        # Point hat 3 punkte thats it. kann als Tupel initiiert werden oder mit 3 übergabe parametern
        # kommt aufs selbe hinaus
        if (type(point) == tuple):
            self.point = point
        else:
            self.point = (point, y, z)

    def __repr__(self):
        return 'Point(%s, %s, %s)' % (repr(self.point[0]), repr(self.point[1]), repr(self.point[2]))

    def __eq__(self, p2):
        return self.point == p2.point

    def __sub__(self, p2):
        # Subtraktion von 2 punkten ergibt einen Vector NICHT punkt
        assert (type(p2) == Point)
        v = (self.point[0] - p2.point[0], self.point[1] - p2.point[1], self.point[2] - p2.point[2])
        return Vector(v)

    def __add__(self, v):
        # Punkt + vector = Punkt
        assert (type(v) == Vector)
        p = (self.point[0] + v.x, self.point[1] + v.y, self.point[2] + v.z)
        return type(self)(p)
