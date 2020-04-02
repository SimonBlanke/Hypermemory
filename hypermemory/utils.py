# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import inspect
import hashlib
import datetime


def function_string(function):
    return inspect.getsource(function)


def object_hash(object):
    return hashlib.sha1(object).hexdigest()


def model_id(model):
    return str(object_hash(function_string(model).encode("utf-8")))


def get_datetime():
    return datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S:%f")


def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True
