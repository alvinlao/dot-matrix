import os
import pickle


class Cache():
    def __init__(self, directory, key):
        self.directory = directory
        self.key = key
        self.data = {}

    def load(self):
        try:
            self.data = pickle.load(
                open(_cache_filename(self.directory, self.key), 'rb'))
        except Exception:
            self.data = {}

        return self

    def save(self, data):
        filename = _cache_filename(self.directory, self.key)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.data = data
        pickle.dump(data, open(filename, 'wb'))

        return self


def _cache_filename(cache_directory, key):
    cache_filename = hash(key)
    return cache_directory + str(cache_filename) + '.cache'
