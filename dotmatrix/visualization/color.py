def dot_color(start, stop, scale):
    return normalize_rgb(interpolate(start, stop, scale))


def normalize_rgb(color):
    return (
        color[0] / 255,
        color[1] / 255,
        color[2] / 255,
    )


def interpolate(start, stop, scale):
    return (
        scale * stop[0] + (1 - scale) * start[0],
        scale * stop[1] + (1 - scale) * start[1],
        scale * stop[2] + (1 - scale) * start[2],
    )
