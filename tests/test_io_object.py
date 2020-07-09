# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import inspect
from hypermemory import IoObject


def test_():
    def obj_func(para):
        return para["x1"] ** 2

    search_space = {"x1": range(1, 100)}

    io_obj = IoObject("./", "objective_function.pkl")
    io_obj.save(obj_func)
    obj_func_new = io_obj.load()

    assert obj_func.__code__.co_code == obj_func_new.__code__.co_code

