import math
from Surface import Surface


class Triangle(object):

    def __init__(self, a, b, c, material=None):
        self.a = a
        self.b = b
        self.c = c
        self.u = self.b -self.a # direction Vector
        self.v = self.c -self.a # direction Vector

        self.surface = material
        if not material:
            self.surface = Surface()

    def __repr__(self):
        return 'Trangle(%s%s&s)' %(repr(self.a), repr(self.b), repr(self.c))


    def intersectionParameter(self, ray):
        w = ray.origin - self.a

        dv= ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross (self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction)/ dvu
        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return wu.dot(self.v) /dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()




class Sphere(object):
    def __init__(self, center, radius, surface=None):
        self.center = center # point
        self.radius = radius # scalar

        self.surface = surface
        if not surface:
            self.surface = Surface()



    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v**2 - co.dot(co) + self.radius**2
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalized()




class Plane(object):

    def __init__(self, point, normal, surface=None):
        self.point = point
        self.normal = normal.normalized()

        self.surface = surface
        if not surface:
            self.surface = Surface()

    def __repr__(self):
        return "Plane(%s, %s)" % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a / b
        else:
            return None

    def normalAt(self, p):
        return self.normal

