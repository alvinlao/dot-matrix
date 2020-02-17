def to_index(dataset_size, coordinate):
    """
    Converts a (latitude, longitude) coordinate tuple to a
    (x, y) array index tuple.
    """
    lat, long = coordinate
    return (_from_lat(dataset_size, lat), _from_long(dataset_size, long))


def _from_lat(dataset_size, lat):
    nrows, _ = dataset_size
    return int((abs(lat - 90) / 180) * nrows)


def _from_long(dataset_size, long):
    _, ncols = dataset_size
    return int(((long + 180) / 360) * ncols)
