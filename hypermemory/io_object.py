# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import dill


class IoObject:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def save(self, _object):
        with open(self.path + self.name, "wb") as dill_file:
            dill.dump(_object, dill_file)

    def load(self):
        with open(self.path + self.name, "rb") as dill_file:
            _object = dill.load(dill_file)

        return _object
