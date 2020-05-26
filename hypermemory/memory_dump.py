# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json
import dill
import inspect
import random

import numpy as np
import pandas as pd

from operator import itemgetter
from .memory_io import MemoryIO
from .dataset_features import get_dataset_features
from .utils import object_hash


class MemoryDump(MemoryIO):
    def __init__(self, X, y, model, search_space, path):
        super().__init__(X, y, model, search_space, path)

    def dump_object(self, _object, path):
        with open(path, "wb") as dill_file:
            dill.dump(_object, dill_file)

    def dump_dict(self, _dict, path):
        with open(path, "w") as json_file:
            json.dump(_dict, json_file, indent=4)

    def dump_dataframe(self, _dataframe, path):
        path = self._get_file_path(self.model)

        if os.path.exists(path):
            _dataframe_old = pd.read_csv(path)

            assert len(_dataframe_old.columns) == len(
                _dataframe.columns
            ), "Warning meta data dimensionality does not match"

            _dataframe_final = _dataframe_old.append(_dataframe)

            columns = list(_dataframe_final.columns)
            noScore = ["_score_", "cv_default_score", "eval_time", "run"]
            columns_noScore = [c for c in columns if c not in noScore]

            _dataframe_final = _dataframe_final.drop_duplicates(subset=columns_noScore)
        else:
            _dataframe_final = _dataframe

        _dataframe_final.to_csv(path, index=False)

    def dump_short_term_memory(self, memory_dict, path):
        self._search_space_types()
        self._create_hash_list()

        tuple_list = list(memory_dict.keys())
        result_list = list(memory_dict.values())

        results_df = pd.DataFrame(result_list)
        np_pos = np.array(tuple_list)

        para_dict = {}
        for i, key in zip(range(np_pos.shape[1]), self.search_space):
            np_pos_ = list(np_pos[:, i])
            search_space_list = list(self.search_space[key])

            if self.search_space_types[key] == "object":
                search_space_list = self.object_hash_dict[key]

            para_list = list(itemgetter(*np_pos_)(search_space_list))
            para_dict[key] = para_list

        para_df = pd.DataFrame(para_dict)
        meta_data_df = pd.concat([para_df, results_df], axis=1)

        self.dump_dataframe(meta_data_df, path)

        print("\n self.object_hash_dict \n", self.object_hash_dict)

    def _get_file_path(self, model_func):
        if not os.path.exists(self.date_path):
            os.makedirs(self.date_path)

        return self.model_path + self.meta_data_name

    def _search_space_types(self):
        self.search_space_types = {}
        for key in self.search_space.keys():
            search_space_list = list(self.search_space[key])

            # sampled_list = random.sample(aList, 3)

            value = search_space_list[0]

            if isinstance(value, int):
                self.search_space_types[key] = "int"
            elif isinstance(value, float):
                self.search_space_types[key] = "float"
            elif isinstance(value, str):
                self.search_space_types[key] = "str"
            else:
                self.search_space_types[key] = "object"

    def _create_hash_list(self):
        self.object_hash_dict = {}

        for key in self.search_space.keys():
            if self.search_space_types[key] == "object":
                search_space_list = list(self.search_space[key])

                object_hash_list = []

                for value in search_space_list:
                    para_dill = dill.dumps(value)
                    para_hash = object_hash(para_dill)

                    with open(
                        self.model_path + str(para_hash) + ".pkl", "wb"
                    ) as pickle_file:
                        dill.dump(para_dill, pickle_file)

                    object_hash_list.append(para_hash)

                self.object_hash_dict[key] = object_hash_list


class MemoryDump1(MemoryIO):
    def __init__(self, X, y, model, search_space, path):
        super().__init__(X, y, model, search_space, path)

    def _save_memory(self, memory_dict, main_args):
        self.memory_dict = memory_dict

        # Save meta_data
        path = self._get_file_path(self.model)
        meta_data = self._collect(memory_dict)

        if meta_data is None:
            return

        meta_data["run"] = self.datetime
        self._save_toCSV(meta_data, path)

        # Save function
        obj_func_path = self.model_path + "objective_function.pkl"

        with open(obj_func_path, "wb") as pickle_file:
            dill.dump(self.model, pickle_file)

        # Save search space
        search_space_path = self.model_path + "search_space.pkl"

        with open(search_space_path, "wb") as pickle_file:
            dill.dump(self.search_space, pickle_file)

        # Save data_features
        data_features = get_dataset_features(self.X, self.y)

        if not os.path.exists(self.dataset_info_path):
            os.makedirs(self.dataset_info_path, exist_ok=True)

        with open(self.dataset_info_path + "data_features.json", "w") as f:
            json.dump(data_features, f, indent=4)

        if main_args:
            run_data = {
                "random_state": main_args.random_state,
                "max_time": main_args.random_state,
                "n_iter": main_args.n_iter,
                "optimizer": main_args.optimizer,
                "n_jobs": main_args.n_jobs,
                # "eval_time": main_args.eval_time,
                # "opt_time": main_args.opt_time,
                # "total_time": main_args.total_time,
            }

            with open(self.date_path + "run_data.json", "w") as f:
                json.dump(run_data, f, indent=4)

    def _get_func_str(self, func):
        return inspect.getsource(func)

    def _get_file_path(self, model_func):
        if not os.path.exists(self.date_path):
            os.makedirs(self.date_path)

        return self.model_path + self.meta_data_name

    def _collect(self, memory_dict):
        para_pd, metrics_pd = self._get_opt_meta_data(memory_dict)

        if para_pd is None:
            return None

        md_model = pd.concat([para_pd, metrics_pd], axis=1, ignore_index=False)

        return md_model

    def pos2para(self, pos):
        values_dict = {}
        for i, key in enumerate(self.search_space.keys()):
            pos_ = int(pos[i])
            values_dict[key] = list(self.search_space[key])[pos_]

        return values_dict

    def _get_opt_meta_data(self, memory_dict):
        results_dict = {}
        para_list = []
        score_list = []

        if not memory_dict:
            return None, None

        for key in memory_dict.keys():
            pos = np.fromstring(key, dtype=int)
            para = self.pos2para(pos)
            score = memory_dict[key]

            for key in para.keys():
                if (
                    not isinstance(para[key], int)
                    and not isinstance(para[key], float)
                    and not isinstance(para[key], str)
                ):

                    para_dill = dill.dumps(para[key])
                    para_hash = object_hash(para_dill)

                    with open(
                        self.model_path + str(para_hash) + ".pkl", "wb"
                    ) as pickle_file:
                        dill.dump(para_dill, pickle_file)

                    para[key] = para_hash

            if score != 0:
                para_list.append(para)
                score_list.append(score)

        results_dict["params"] = para_list
        results_dict["score"] = score_list

        return (
            pd.DataFrame(para_list),
            pd.DataFrame(score_list),
        )

    def _save_toCSV(self, meta_data_new, path):
        if os.path.exists(path):
            meta_data_old = pd.read_csv(path)

            assert len(meta_data_old.columns) == len(
                meta_data_new.columns
            ), "Warning meta data dimensionality does not match"

            meta_data = meta_data_old.append(meta_data_new)

            columns = list(meta_data.columns)
            noScore = ["_score_", "cv_default_score", "eval_time", "run"]
            columns_noScore = [c for c in columns if c not in noScore]

            meta_data = meta_data.drop_duplicates(subset=columns_noScore)
        else:
            meta_data = meta_data_new

        meta_data.to_csv(path, index=False)
