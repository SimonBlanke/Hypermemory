# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np
import pandas as pd


def convert_dataframe(dataframe1, search_space1, search_space2):
    dataframe2 = dataframe1.copy()

    for para1 in search_space1:
        if para1 not in search_space2:
            dataframe2.drop([para1], inplace=True)
            continue

        search_elements1 = search_space1[para1]
        search_elements2 = search_space2[para1]

        both = set(search_elements1).intersection(search_elements2)

        indices_A = [search_elements1.index(x) for x in both]
        indices_B = [search_elements2.index(x) for x in both]

        conv_dict = dict(zip(indices_A, indices_B))

        col = dataframe2[para1]
        col_conv = col.map(conv_dict)
        col_conv = col_conv.dropna(how="any")
        col_conv = col_conv.astype(int)

        dataframe2[para1] = col_conv

    return dataframe2


def memory_dict2dataframe(memory_dict, search_space):
    columns = list(search_space.keys())
    # columns = [col + ".index" for col in columns]

    pos_tuple_list = list(memory_dict.keys())
    result_list = list(memory_dict.values())

    results_df = pd.DataFrame(result_list)
    np_pos = np.array(pos_tuple_list)

    pd_pos = pd.DataFrame(np_pos, columns=columns)
    dataframe = pd.concat([pd_pos, results_df], axis=1)

    return dataframe


def dataframe2memory_dict(dataframe, search_space):
    columns = list(search_space.keys())
    # columns = [col + ".index" for col in columns]

    positions = dataframe[columns]
    scores = dataframe.drop(columns, axis=1)

    scores = scores.to_dict("records")
    positions_list = positions.values.tolist()

    # list of lists into list of tuples
    pos_tuple_list = list(map(tuple, positions_list))
    memory_dict = dict(zip(pos_tuple_list, scores))

    return memory_dict


"""
    def _dump_dataframe(self, _dataframe):
        if os.path.exists(path + name):
            _dataframe_old = pd.read_csv(path + name)

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

        _dataframe_final.to_csv(path + name, index=False)

    def _get_func_data_names(self):
        paths = []
        for id in self.con_ids:
            paths = paths + glob.glob(
                self.meta_path + model_path(id) + self.meta_data_name
            )

        return paths

    def _read_func_metadata(self, model_func):
        paths = self._get_func_data_names()

        meta_data_list = []
        for path in paths:
            meta_data = pd.read_csv(path)
            meta_data_list.append(meta_data)
            self.meta_data_found = True

        if len(meta_data_list) > 0:
            meta_data = pd.concat(meta_data_list, ignore_index=True)

            para = meta_data[self.para_names]
            score = meta_data[self.score_col_name]

            # _verb_.load_meta_data()
            return para, score

        else:
            # _verb_.no_meta_data(model_func)
            return None, None

    def save(self, memory_dict):
        self._search_space_types()
        self._create_hash_list(path)
        meta_data_df = self.memory_dict2dataframe(memory_dict)

        # meta_data_df["run"] = self.datetime

        self._dump_dataframe(meta_data_df, path, name)

    def load(self):
        para, score = self._read_func_metadata(self.model)
        if para is None or score is None:
            print("No meta data found")
            return {}

        memory_dict = self._load_data_into_memory(para, score)
        self.n_dims = len(para.columns)

        return memory_dict
"""

