import cairo
import numpy
import random

from dotmatrix.visualization.color import background_color, dot_color
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
        color=background_color(config))

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


def _allow_none(f):
    def _f(v):
        if v is None:
            return v
        else:
            return f(v)
    return _f


def _flatten(xs):
    return [x for xss in xs for x in xss]


if __name__ == "__main__":
    random.seed(1000)

    blue = {'population': [(144, 221, 240)],
            'weights': [1]}
    dark_green = {'population': [(30, 71, 56)]}
    green = {'population': [(117, 183, 146)]}
    light_grey = {'population': [(200, 200, 200)]}
    hot_pink = {'population': [(255, 148, 148)]}
    orange = {'population': [(255, 148, 0)]}
    blood_orange = {'population': [(237, 114, 0)]}

    config = {
        'dataset': {
            'filename': 'data/population_density.ascii',
            'size': (10, 14),
            'cache_directory': 'cache/',
            'top_left_coordinate': (38.294140, -122.642074),
            'scale': 2,
        },
        'color': {
            'quantiles': _flatten([
                [blue] * 2,
                [dark_green] * 33,
                [green] * 9,
                [light_grey] * 3,
                [hot_pink] * 3,
                [orange] * 1,
                [blood_orange] * 1,
            ]),
            'water': blue,
        },
        'draw': {
            'background_color': (255, 255, 255),
            'width': 650,
            'height': 1000,
            'padding-vertical': 0.10,
            'padding-horizontal': 0.04,
            'dot-spacing': 0.35,
        },
    }

    dataset = load(config['dataset'])

    max_value = (
        dataset.filter(lambda v: v is not None)
        .reduce(max))

    num_quantiles = len(config['color']['quantiles']) - 1
    dataset_list = [v for v in dataset.iterable() if v is not None]
    quantiles = (
        numpy.quantile(
            dataset_list,
            [
                q / num_quantiles
                for q in range(num_quantiles)]))

    def find_quantile(v): return next(
        (index for index, x in enumerate(quantiles) if v <= x), num_quantiles)

    dots = (
        dataset
        .map(lambda v: _allow_none(find_quantile)(v))
        .map(lambda v: dot_color(config['color'], v, len(quantiles) - 1))
        .matrix())

    draw(config['draw'], dots)

    print('>>>>>>>')
