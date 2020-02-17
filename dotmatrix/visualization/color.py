import math
import random


def dot_color(config, value, max_value):
    if value is None or value == 0:
        return _color_noise(_normalize_rgb(config['none']), 0.2)

    scale = math.log(value) / math.log(max_value)
    start = _normalize_rgb(config['start'])
    stop = _normalize_rgb(config['stop'])
    return _color_noise(_interpolate(start, stop, scale), 0.1)


def _normalize_rgb(color):
    return (
        color[0] / 255,
        color[1] / 255,
        color[2] / 255,
    )


def _interpolate(start, stop, scale):
    return (
        scale * stop[0] + (1 - scale) * start[0],
        scale * stop[1] + (1 - scale) * start[1],
        scale * stop[2] + (1 - scale) * start[2],
    )


def _color_noise(color, effect):
    return (
        _noise(color_channel, 0.1)
        for color_channel in color
    )


def _noise(value, effect):
    return (effect * random.randrange(-1, 1)) + value
