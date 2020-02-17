import pickle

from dotmatrix.populationdensity.dataset import get_dataset


def populationdensity(config):
    return (
        _load_dataset_from_cache(config) or
        _cache_dataset(config, get_dataset(config)))


def _load_dataset_from_cache(config):
    try:
        return pickle.load(open(_cache_filename(config), 'rb'))
    except Exception:
        return None


def _cache_dataset(config, dataset):
    pickle.dump(dataset, open(_cache_filename(config), 'wb'))
    return dataset


def _cache_filename(config):
    cache_filename = hash((config['top_left_coordinate'], config['size']))
    return config['cache_directory'] + str(cache_filename) + '.cache'
