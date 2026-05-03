from turtle import * # type: ignore
import colorsys

speed(0)
bgcolor("black")
h = 0
for i in range(16) :
    c = colorsys.hsv_to_rgb(h,1,1)
    color(c)
    h += 0.005
    rt(90)
    circle(150 - j * 6, 90 ) # pyright: ignore[reportUndefinedVariable]
    lt(90)
    circle(150 - j * 6, 90) # pyright: ignore[reportUndefinedVariable]
    rt(180)
    circle(40 , 24)
done()