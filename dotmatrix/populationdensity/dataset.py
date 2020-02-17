import itertools
import functools

from dotmatrix.populationdensity.cache import Cache
from dotmatrix.populationdensity.coordinate import to_index
from dotmatrix.populationdensity.transform import transform


class DataSet():
    def __init__(self, dataset):
        """
        dataset: a 2D array
        """
        self.dataset = dataset

    def map(self, f):
        return DataSet([
            [f(v) for v in row]
            for row in self.dataset
        ])

    def map_with_key(self, f):
        return DataSet([
            [f((x_index, y_index), v) for x_index, v in enumerate(row)]
            for y_index, row in enumerate(self.dataset)
        ])

    def reduce(self, f, v=0):
        return functools.reduce(f, self.iterable(), v)

    def filter(self, f):
        return DataSet(
            DataSet.remove_empty_rows([
                [v for v in row if f(v)]
                for row in self.dataset
            ]))

    def filter_by_key(self, f):
        return DataSet(
            DataSet.remove_empty_rows([
                [
                    v
                    for x_index, v in enumerate(row)
                    if f((x_index, y_index))
                ]
                for y_index, row in enumerate(self.dataset)
            ]))

    def remove_empty_rows(dataset):
        return [
            row
            for row in dataset
            if row
        ]

    def iterable(self):
        for row in self.dataset:
            for v in row:
                yield v

    def matrix(self):
        return self.dataset

    def get(self, key):
        x, y = key
        try:
            return self.dataset[y][x]
        except IndexError:
            return None

    def keys(self):
        if not self.dataset:
            return []

        return list(itertools.product(
            range(len(self.dataset[0])),
            range(len(self.dataset))))


def load(config):
    return transform(config, _load_dataset(config))


def _load_dataset(config):
    header = _header(config['filename'])
    cache = Cache(config['cache_directory'], _cache_key(header))
    keys = _keys(config, header)

    return (
        _dataset_from_cache(config, header, cache, keys) or
        _dataset_from_source(config, header, cache, keys))


def _dataset_from_cache(config, header, cache, keys):
    if set(cache.load().data.keys()).issuperset(keys):
        return _dataset(config, header, cache, keys)
    else:
        return None


def _dataset_from_source(config, header, cache, keys):
    raw_data = _get_raw_data(config, _parsefile(config['filename']))
    return _dataset(
        config,
        header,
        cache.save({**cache.data, **raw_data}),
        keys)


def _header(filename):
    with open(filename) as f:
        return _parse_header(f)


def _parsefile(filename):
    """
    Parses the dataset obtained from:
    https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11
    """
    with open(filename) as f:
        return {
            'header': _parse_header(f),
            'data': [
                _parseline(line)
                for line in f.readlines()
            ],
        }


def _parse_header(f):
    return {
        'ncols': int(_parseline(f.readline())[1]),
        'nrows': int(_parseline(f.readline())[1]),
        'xllcorner': _parseline(f.readline())[1],
        'yllcorner': _parseline(f.readline())[1],
        'cellsize': _parseline(f.readline())[1],
        'NODATA_value': _parseline(f.readline())[1],
    }


def _parseline(line):
    return [v for v in line.strip().split(" ") if v]


def _keys(config, header):
    dataset_size = (header['nrows'], header['ncols'])
    x_size, y_size = (v * config['scale'] for v in config['size'])
    x0, y0 = to_index(dataset_size, config['top_left_coordinate'])
    x1, y1 = x0 + y_size, y0 + x_size

    return set(
        itertools.product(
            range(x0, x1),
            range(y0, y1)))


def _get_raw_data(config, parsed_file):
    keys = _keys(config, parsed_file['header'])
    data = parsed_file['data']
    return {
        (x, y): data[x][y]
        for x, y in keys
    }


def _cache_key(header):
    return (header['nrows'], header['ncols'])


def _dataset(config, header, cache, keys):
    ncols = config['size'][0] * config['scale']
    nodatavalue = header['NODATA_value']
    dataset = DataSet(
        _grouper(
            ncols,
            (cache.data[key] for key in sorted(keys))))

    return dataset.map(
        lambda v: None if v == nodatavalue else float(v))


def _grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)
