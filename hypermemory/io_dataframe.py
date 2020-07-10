# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import pandas as pd


class IoDataframes:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def save(self, _dataframe):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        _dataframe_final.to_csv(self.path + self.name + ".csv"), index=False)

    def load(self):
        paths = paths + glob.glob(
            self.path + "*.csv"
        )

        dataframe_list = []
        for path in paths:
            dataframe_list.append(pd.read_csv(path))

        return dataframe_list

