from turtle import * # type: ignore
from colorsys import * # type: ignore
tracer(10)
bgcolor("black")
pensize(2)
h = 0 
def draw(od, ih , dr):
    global h 
    if od == 0:
        color(hsv_to_rgb(h, 1, 1))
        h = (h + 0.005) % 1
        fd(ih)
    else: 
        draw(od - 1, ih / 1.414, 1)
        rt(90 * dr)
        draw(od - 1, ih / 1.414, -1)
pu()
goto(-100, 0)
pd()
lt(90)
draw(12, 200, 1)
done()