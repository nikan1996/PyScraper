#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: __init__.py.py

@time: 22/01/2018 2:59 PM
"""
import importlib
import inspect
import pkgutil
import sys
import time
import traceback
from importlib import import_module

from scrapy import Spider


def run_in_thread(func, *args, daemon=True, **kwargs):
    """Run function in thread, return a Thread object"""
    from threading import Thread
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = daemon
    thread.start()
    return thread


def import_class(cl):
    d = cl.rfind(".")
    classname = cl[d + 1:len(cl)]
    module = importlib.import_module(cl[0:d])
    return getattr(module, classname)


def get_class_source(kls_name):
    cls = import_class(kls_name)
    source = inspect.getsource(cls)
    return source


def get_all_submodules(module_name):
    """

    :param module_name: abstract module path
    :return: submodules

    """
    start = time.process_time()
    mods = []
    mod = import_module(module_name)
    sys.modules[module_name] = mod
    for loader, module_name, is_pkg in pkgutil.walk_packages(mod.__path__, onerror=lambda x: print(x)):
        try:
            loader.find_module(module_name).load_module(module_name)
            if is_pkg:
                print('pkg:', module_name)
            else:
                mods.append(import_module(module_name))
        except Exception as e:
            traceback.print_exc()
    print('load_cost_time:', time.process_time() - start)
    return mods


def get_classes_from_submodules(submodules, class_type=None):
    classes = []
    for module in submodules:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if not class_type or (class_type and issubclass(obj, class_type)):
                    classes.append(obj)
    return classes


def load_spiders(submodules, class_type=Spider):
    return get_classes_from_submodules(submodules, class_type=class_type)
