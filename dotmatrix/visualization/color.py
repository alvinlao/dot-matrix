from colormath.color_objects import sRGBColor, LCHabColor
from colormath.color_conversions import convert_color


def dot_color(start, stop, scale):
    start_rgb = sRGBColor(*normalize_rgb(start))
    stop_rgb = sRGBColor(*normalize_rgb(stop))
    start_lch = convert_color(start_rgb, LCHabColor)
    stop_lch = convert_color(stop_rgb, LCHabColor)

    color_lch = linear(
        start_lch.get_value_tuple(),
        stop_lch.get_value_tuple(),
        scale)

    return convert_color(LCHabColor(*color_lch), sRGBColor).get_value_tuple()


def normalize_rgb(color):
    return (
        color[0] / 255,
        color[1] / 255,
        color[2] / 255,
    )


def linear(start, stop, scale):
    return (
        scale * stop[0] + (1 - scale) * start[0],
        scale * stop[1] + (1 - scale) * start[1],
        scale * stop[2] + (1 - scale) * start[2],
    )
