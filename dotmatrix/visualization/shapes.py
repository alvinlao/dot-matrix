import math


def rectangle(ctx, p0, p1, color):
    ctx.set_source_rgb(*color)
    ctx.rectangle(*p0, *p1)
    ctx.fill()


def circle(ctx, x, y, r, color):
    ctx.set_source_rgb(*color)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.fill()
