import cairo
import random

from dotmatrix.visualization.color import dot_color
from dotmatrix.visualization.layout import Dimension, padding, dot_slot_size
from dotmatrix.visualization.shapes import rectangle, circle


def draw(config):
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32,
        config['width'],
        config['height'])

    ctx = cairo.Context(surface)
    rectangle(
        ctx,
        p0=(0, 0),
        p1=(config['width'], config['height']),
        color=(1, 1, 1))

    ctx = cairo.Context(surface)
    ctx.translate(
        padding(config, Dimension.WIDTH),
        padding(config, Dimension.HEIGHT))
    draw_dots(ctx, config)

    surface.write_to_png("example.png")


def draw_dots(ctx, config):
    dots = config['dots']['colors']
    spacing_ratio = config['dots']['spacing']
    dot_slot = dot_slot_size(config)
    circumference = dot_slot * (1 / (1 + spacing_ratio))
    spacing = dot_slot - circumference
    radius = circumference / 2

    for yindex, row in enumerate(dots):
        for xindex, dot in enumerate(row):
            circle(
                ctx,
                x=(spacing / 2) + (xindex * dot_slot) + radius,
                y=(spacing / 2) + (yindex * dot_slot) + radius,
                r=radius,
                color=dot)


random.seed(1000)
# start = (95, 156, 67)
# start = (30, 71, 56)
# stop = (242, 195, 179)
start = (random.random() * 255, random.random()
         * 255, random.random() * 255)
stop = (random.random() * 255, random.random()
        * 255, random.random() * 255)
draw({
    #    'width': 3000,
    #    'height': 4000,
    'width': 600,
    'height': 1000,
    'padding-vertical': 0.125,
    'padding-horizontal': 0.025,
    'dots': {
        'spacing': 0.35,
        'colors': [
            [
                dot_color(
                    start,
                    stop,
                    (0.2 * ((random.random() * 2) - 1)) + (i+j)/18)
                for i in range(10)
            ]
            for j in range(14)
        ]
    }
})
