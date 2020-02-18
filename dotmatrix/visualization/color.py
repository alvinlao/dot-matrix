import random


def background_color(config):
    return _normalize_rgb(config['background_color'])


def dot_color(config, value, max_value):
    if value is None:
        return _color_noise(
            _normalize_rgb(_choose(config['water'])),
            0)

    scale = value / max_value
    quantiles = config['quantiles']
    group = _group(scale, len(quantiles))
    return _color_noise(_normalize_rgb(_choose(quantiles[group])), 0)


def _normalize_rgb(color):
    try:
        alpha = color[3]
    except IndexError:
        alpha = 1

    return (
        color[0] / 255,
        color[1] / 255,
        color[2] / 255,
        alpha,
    )


def _color_noise(color, effect):
    return (
        _noise(color_channel, effect)
        for color_channel in color
    )


def _noise(value, effect):
    return (effect * random.randrange(-1, 1)) + value


def _group(value, num_groups):
    return min(int(value * num_groups), num_groups - 1)


def _choose(color):
    return random.choices(**color)[0]
