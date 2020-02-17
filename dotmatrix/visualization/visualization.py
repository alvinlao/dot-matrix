import cairo
import random

from dotmatrix.visualization.color import dot_color
from dotmatrix.visualization.layout import Dimension, padding, dot_slot_size
from dotmatrix.visualization.shapes import rectangle, circle
from dotmatrix.populationdensity.dataset import load


def draw(config, dots):
    config['dots'] = dots
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
    dots = config['dots']
    spacing_ratio = config['dot-spacing']
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


if __name__ == "__main__":
    config = {
        'dataset': {
            'filename': 'data/population_density.ascii',
            'size': (10, 14),
            'cache_directory': 'cache/',
            # 'top_left_coordinate': (38.294140, -122.642074),
            'top_left_coordinate': (38.294140, -122.642074),
            'scale': 2,
        },
        'color': {
            # 'start': (235, 64, 52),
            # 'stop': (52, 100, 235),
            'start': (30, 71, 56),
            'stop': (242, 193, 178),
            'none': (88, 195, 245),
        },
        'draw': {
            'width': 600,
            'height': 1000,
            'padding-vertical': 0.125,
            'padding-horizontal': 0.025,
            'dot-spacing': 0.35,
        },
    }

    dataset = load(config['dataset'])

    max_value = (
        dataset.filter(lambda v: v is not None)
        .reduce(max))

    dots = (
        dataset.map(lambda v: dot_color(config['color'], v, max_value))
        .matrix())

    random.seed(1000)
    draw(config['draw'], dots)

    print('>>>>>>>')
