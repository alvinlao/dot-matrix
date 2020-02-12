from enum import Enum


class Dimension(Enum):
    WIDTH = 1
    HEIGHT = 2


config_key = {
    Dimension.WIDTH: {
        'size': lambda c: c['width'],
        'padding-ratio': lambda c: c['padding-horizontal'],
        'num_dots': lambda c: len(c['dots']['colors'][0]),
    },
    Dimension.HEIGHT: {
        'size': lambda c: c['height'],
        'padding-ratio': lambda c: c['padding-vertical'],
        'num_dots': lambda c: len(c['dots']['colors']),
    },
}


def get(config, dimension, attribute):
    return config_key[dimension][attribute](config)


def padding(config, dimension):
    if fixed_dimension(config) == dimension:
        return fixed_padding(config, dimension)
    else:
        return free_padding(config, dimension)


def fixed_padding(config, dimension):
    size = get(config, dimension, 'size')
    padding_ratio = get(config, dimension, 'padding-ratio')
    return size * padding_ratio


def free_padding(config, dimension):
    size = get(config, dimension, 'size')
    return (size - used_space(config, dimension)) / 2


def used_space(config, dimension):
    num_dots = get(config, dimension, 'num_dots')
    return num_dots * dot_slot_size(config)


def allocated_space(config, dimension):
    size = get(config, dimension, 'size')
    return size - (2 * fixed_padding(config, dimension))


def dot_slot_size(config):
    return min(
        fixed_dot_slot_size(config, Dimension.WIDTH),
        fixed_dot_slot_size(config, Dimension.HEIGHT))


def fixed_dot_slot_size(config, dimension):
    space = allocated_space(config, dimension)
    num_dots = get(config, dimension, 'num_dots')
    return space / num_dots


def fixed_dimension(config):
    return min(
        Dimension.WIDTH,
        Dimension.HEIGHT,
        key=lambda d: fixed_dot_slot_size(config, d))


def free_dimension(config):
    return max(
        Dimension.WIDTH,
        Dimension.HEIGHT,
        key=lambda d: fixed_dot_slot_size(config, d))
