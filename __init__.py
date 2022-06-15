__all__ = ["factory_method"]

import os
import importlib


def factory_method(name):
    return __CLASS_DICT__[name]


__CLASS_DICT__ = dict()


def register_function(name):
    def register_function_fn(cls):
        if name in __CLASS_DICT__:
            raise ValueError("Name %s already registered!" % name)
        __CLASS_DICT__[name] = cls
        return cls

    return register_function_fn


for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith('.py') and not file.startswith('_'):
        module_name = file[:file.find('.py')]
        module = importlib.import_module('models.' + module_name)
