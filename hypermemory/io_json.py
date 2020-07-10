# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json


class IoJson:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def save(self, data_features):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        with open(self.path + self.name + ".json", "w") as f:
            json.dump(data_features, f, indent=4)

    def load(self):
        with open(self.path + self.name + ".json", "r") as f:
            data_features = json.load(f)

        return data_features
