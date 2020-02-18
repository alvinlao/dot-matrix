from statistics import mean


def transform(config, dataset):
    dataset_mean = mean(dataset.filter(lambda v: v is not None).iterable())
    anchors = _anchors(config, dataset)
    return (
        dataset
        .map_with_key(
            lambda key, v: _neighbor_reduce(
                dataset,
                key,
                config['scale'],
                _outlier(dataset_mean)))
        .filter_by_key(lambda key: key in anchors))


def _anchors(config, dataset):
    """
    An anchor is the top left key of a square group of elements
    """
    scale = config['scale']
    def is_anchor_index(index): return index % scale == 0
    return set(
        (x, y)
        for x, y in dataset.keys()
        if is_anchor_index(x) and is_anchor_index(y)
    )


def _neighbor_reduce(dataset, key, size, f):
    return _reducer(
        [
            dataset.get(neighbor_key)
            for neighbor_key in _neighbor_keys(dataset, key, size)
        ],
        f)


def _neighbor_keys(dataset, key, size):
    x, y = key
    return [
        (x + x_index, y + y_index)
        for x_index in range(size)
        for y_index in range(size)
    ]


def _reducer(iterable, f):
    if not iterable or None in iterable:
        return None
    else:
        return f(iterable)


def _outlier(avg):
    def _inner(xs):
        return sorted(xs, key=lambda x: abs(x - avg), reverse=True)[0]
    return _inner
