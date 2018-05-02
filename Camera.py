# -*- coding: utf-8 -*-
from Illumination import Ray, Light
import Surface
import math

class Camera(object):
    def __init__(self, eye, up, focalpoint, fov):

        self.eye = eye
        self.up = up
        self.focalpoint = focalpoint
        self.fov = fov

        # Weltkoordinatensystem
        self.z = (focalpoint - eye).normalized()
        self.x = self.z.cross(up).normalized()
        self.y = self.x.cross(self.z)

    def setScreenSize(self, width, height):
        # Definition der Betrachtungsgeometrie
        # Bildgröße in Pixel
        # höhe und breite.
        # Hier wird für das Kamera Objet ein Verhältnis zum aspektRatio ausgerechnet

        self.width = width
        self.height = height
        ratio = width / float(height)
        alpha = self.fov / 2.0
        self.sceneHeight = 2 * math.tan(alpha)
        self.sceneWidth = ratio * self.sceneHeight
        # Auflösungsberechnung
        self.pixelWidth = self.sceneWidth / (width - 1)
        self.pixelHeight = self.sceneHeight / (height - 1)

    def build_ray(self, x, y):
        #Vorlesung Folie 33
        xComp = self.x * (x * self.pixelWidth - self.sceneWidth / 2.0)
        yComp = self.y * (y * self.pixelHeight - self.sceneHeight / 2.0)
        return Ray(self.eye, self.z + xComp + yComp)

    def getMinDistAndObj(self, ray, objectList):
        closer = None
        minimum = float('inf')
        for obj in objectList:
            dist = obj.intersectionParameter(ray)
            if dist and dist > 0 and dist < minimum:
                minimum = dist
                closer = obj
        return minimum, closer

    def shading(self, objectList, lightRay):
        for obj in objectList:
            t = obj.intersectionParameter(lightRay)
            if t > 0:
                return t
        return 0

    def calculateColor(self, objectList, lightList, rayDir, point, obj):
        # Richtung des Strahls auf den Punkt der berechnet werden soll
        normal = obj.normalAt(point)
        color = obj.surface.color * obj.surface.ambient
        # Farbe des zurberechneten Objekts

        for light in lightList:
            lightRay = Ray(point, light.position - point)
            if not self.shading(objectList, lightRay):
                color += obj.surface.renderColor(lightRay, normal, light.intensity, rayDir)

        # Objektfarbe ohne Spiegelung!!!!!!
        return color

    def renderRay(self, objectList, lightList, ray, bgColor, level):
        (dist, obj) = self.getMinDistAndObj(ray, objectList)
        if dist and dist > 0 and dist < float('inf'):
            point = ray.origin + ray.direction * dist
            normal = obj.normalAt(point)
            if level == 0:
                return self.calculateColor(objectList, lightList, ray.direction, point, obj)
            else:
                color = self.calculateColor(objectList, lightList, ray.direction, point, obj)
                reflectedRay = Ray(point, ray.direction.reflect(normal) * -1)
                reflectedColor = self.renderRay(objectList, lightList, reflectedRay, bgColor, level - 1)
                return (color * (1 - obj.surface.texture) + reflectedColor * obj.surface.texture).realColor()
        else:
            return bgColor

    def render(self, render_func, objectList, lightList, bgColor=Surface.bgColor, level=1):
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                ray = self.build_ray(x, y)
                color = self.renderRay(objectList, lightList, ray, bgColor, level)
                render_func(x, y, color)

    def __repr__(self):
        return 'Camera(position:%s, up:%s, f_point:%s, fieldOfView:%s, x:%s, y:%s, z:%s)' % (
            repr(self.eye), repr(self.up), repr(self.focalpoint), repr(self.fov), repr(self.x), repr(self.y),
            repr(self.z))
