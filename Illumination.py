from WorldGeometry import *

class Light(object):

    def __init__(self, position, intensity=1):
        assert(type(position) is Point)
        self.position = position
        self.intensity = intensity


class Ray(object):
    def __init__(self, origin, direction):
        assert(type(origin) is Point and type(direction is Vector))
        self.origin = origin # point
        self.direction = direction.normalized() # vector

    def __repr__(self):
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)

    def reflect(self, normal, newPoint=None):
        if not newPoint:
            newPoint = self.origin
        return Ray(newPoint, self.direction.reflect(normal))