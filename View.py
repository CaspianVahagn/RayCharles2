# -*- coding: utf-8 -*-
from Tkinter import *
from Camera import Camera
from Illumination import *
from Surface import *
from WorldObjects import *
from  WorldGeometry import *

default = 400
fov = math.radians(45)
scale = 1
width = int(default * scale)
height = int(default * scale)
# Default colors
floor = Color(118,118,118)
magenta = Color(255,90,148)
turkis = Color(42,152,105)
blue = Color(94,146,255)
yellow = Color(200, 240, 178)

# Default surfaces (Farbe, ambient, diffuser anteil, specularer Anteil, Glattheit)
surf_floor = Surface(floor, 1, 0.5, 0.2, 0.2)
surf_m = Surface(magenta, 0.3, 0.8, 0.2, 0.2)
surf_t = Surface(turkis, 0.3, 0.8, 0.2, 0.2)
surf_b = Surface(blue, 0.3, 0.8, 0.2, 0.2)
surf_y = Surface(yellow, 0.3, 0.8, 0.2, 0.2)
surf_check = ComplexSurface()

lightList = [Light(Point(30, 30, 30),1), Light(Point(-1, 29, -10), 0.2)]
objectList = [Triangle(Point(2.5, 3, -10),Point(-2.5, 3, -10), Point(0, 7, -10), surf_y),
              Sphere(Point(2.5, 3, -10), 2, surf_m),
              Sphere(Point(-2.5, 3, -10), 2, surf_t),
              Sphere(Point(0, 7, -10), 2, surf_b),
              Plane(Point(0, 0, 0), Vector(0, 1, 0), surf_check)]



def rainbow(list):
    #zufällig gefärbte Objekte
    for e in list:
        if type(e.surface) is type(surf_check):
            print "check"
        else:
            e.surface = randomcolored()

def removeCheck(list):
    for e in list:
        if type(e.surface) is type(surf_check):
            e.surface = surf_floor



def putpixel(x, y, color):
    canvas.create_line(x, height - y, x + 1, height - (y + 1), fill=color.toHexString())

def randomcolored():

    return Surface(floor.randomColor(), 0.3, 0.8, 0.2, 0.2)


if __name__ == '__main__':

    promptval = raw_input("Willkommen bei RayTracer\nStarten mit zufälligen Farben ? j/n \n")

    if(promptval == "j" ):
        rainbow(objectList)

    promptval = raw_input("Schachbrett ? j/n \n")
    if(promptval == "n"):
        removeCheck(list)


    promptval = raw_input("Wie tief soll gerendert werden? Level 0-5 \n")

    level = int(promptval)

    root = Tk()
    root._root().wm_title("Ray Charles")
    frame = Frame(root, width=width, height=height)
    frame.pack()
    canvas = Canvas(frame, width=width, height=height, bg="white")
    canvas.pack()
    camera = Camera(Point(0,2,10), Vector(0,1,0), Point(0,3,0), fov)
    camera.setScreenSize(width, height)
    #           (renderfunktion, objekte, lichter, hindergrund , rendertiefe)
    print "Start rendering"
    print  "Anzahl Lichter: %d \nAnzahl Objekte: %d \n" % (len(lightList),len(objectList))
    camera.render(putpixel, objectList, lightList, Color(97,97,130), level)
    root.mainloop()