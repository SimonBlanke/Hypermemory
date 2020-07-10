# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import dill


class IoDill:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def save(self, _object):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        with open(self.path + self.name + ".pkl", "wb") as dill_file:
            dill.dump(_object, dill_file)

    def load(self):
        with open(self.path + self.name + ".pkl", "rb") as dill_file:
            _object = dill.load(dill_file)

        return _object
