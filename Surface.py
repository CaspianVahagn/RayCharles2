# -*- coding: utf-8 -*-

from WorldGeometry import Vector
import random
import math

# Höhster Farbwert
MAXC = 255

class Color(Vector):

    def __init__(self, r, g=0, b=0):
        Vector.__init__(self, r, g, b)
        self.r = self.x
        self.g = self.y
        self.b = self.z

    def realColor(self):
        (r, g, b) = self.vec
        c = [r, g, b]
        c = (Color(tuple([MAXC if x > MAXC else x for x in c])))
        return c

    def __mul__(self, other):
        return super(Color, self).__mul__(other)

    def __add__(self, other):
        return super(Color, self).__add__(other)

    def toHexString(self):
        return '#%02X%02X%02X' % (self.r, self.g, self.b)

    def randomColor(self):
        def r(): return random.randint(0,255)

        return Color(r(), r(), r())



black = Color(1, 1, 1)
white = Color(255, 255, 255)
bgColor = Color(97, 97, 130)


class Surface(object):

    def __init__(self, color=None, ambient=0, diffuse=0.8, specular=0.2, texture=0.05):
        self.color = color
        if not color:
            self.color = Color(128, 128, 128)

        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.texture = texture

    def renderColor(self, lightRay, normal, lightIntensity, rayDirection):
        color = black
        reflectedLight = (lightRay.direction).reflect(normal)
        diffuseFactor = lightRay.direction.dot(normal)
        expo = MAXC / 4 * self.texture + 1
        if (diffuseFactor > 0):
            color += self.color * (diffuseFactor * self.diffuse) * lightIntensity
            specularFactor = reflectedLight.dot(rayDirection * -1)
            if specularFactor > 0:
                specConst = (expo + 2) / (math.pi * 2)

                color += white * specConst * ((specularFactor ** expo) * self.specular) * lightIntensity
        return color




class ComplexSurface():
    def __init__(self, color=Color(30, 30, 30), color2=Color(200, 200, 200), ambient=0, diffuse=0.8, specular=0.2,
                 texture=0.05):
        self.color = color
        self.color2 = color2
        self.checksize = 0.05
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.texture = texture

    def renderColor(self, lightRay, normal, lightIntensity, rayDirection):

        color = black
        reflectedLight = (lightRay.direction).reflect(normal)
        diffuseFactor = lightRay.direction.dot(normal)
        v = reflectedLight
        v = v.scale(1.0 / self.checksize)
        expo = MAXC / 4 * self.texture + 1
        if (int(abs(v.x) + 0.5) + int(abs(v.y) + 0.5) + int(abs(v.z) + 0.5)) % 2 == 1:
            color = self.color
            if (diffuseFactor > 0):
                color += self.color * (diffuseFactor * self.diffuse) * lightIntensity
                specularFactor = reflectedLight.dot(rayDirection * -1)
                if specularFactor > 0:
                    specConst = (expo + 2) / (math.pi * 2)
                    color += white * specConst * (specularFactor ** expo * self.specular) * lightIntensity
            return color

        else:
            color = self.color2
            if (diffuseFactor > 0):
                color += self.color2 * (diffuseFactor * self.diffuse) * lightIntensity
                specularFactor = reflectedLight.dot(rayDirection * -1)
                if specularFactor > 0:
                    specConst = (expo + 2) / (math.pi * 2)
                    color += white * specConst * (specularFactor ** expo * self.specular) * lightIntensity
            return color

