# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np


from .memory_load import MemoryLoad
from .memory_dump import MemoryDump

from .paths import _paths_


class Hypermemory:
    def __init__(self, X, y, model, search_space, path=None):
        self.memory_dict = None
        self.meta_data_found = False
        self.n_dims = None

        self._load_ = MemoryLoad(X, y, model, search_space, path=path)
        self._dump_ = MemoryDump(X, y, model, search_space, path=path)

    def load(self):
        self.memory_dict = self._load_._load_memory()
        self.meta_data_found = self._load_.meta_data_found

        self.score_best = self._load_.score_best
        self.pos_best = self._load_.pos_best

        return self.memory_dict

    def dump(self, memory, path="default"):
        self._dump_.dump_short_term_memory(memory, _paths_[path])

    def _get_para(self):
        if self.memory_dict is None:
            print("Error")
            return
        para_pd, metrics_pd = self._dump_._get_opt_meta_data(self.memory_dict)

        return para_pd.values, np.expand_dims(metrics_pd["score"].values, axis=1)
