#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: __init__.py.py

@time: 22/01/2018 2:59 PM
"""
import importlib
import inspect
import logging
import pkgutil
import sys
import time
import traceback
from importlib import import_module

from scrapy import Spider

logger = logging.getLogger(__name__)


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


def get_all_submodules(*, root_module_name):
    """
    load submodule and get_all_submodules
    :param module_name: abstract module path
    :return: submodules

    """
    start = time.process_time()
    mods = []
    mod_names = []
    mod = import_module(root_module_name)
    sys.modules[root_module_name] = mod

    for loader, module_name, is_pkg in pkgutil.walk_packages(mod.__path__, onerror=lambda x: print(x)):
        try:
            sub_module_name = module_name
            loader.find_module(sub_module_name).load_module(sub_module_name)
            if is_pkg:
                logger.debug(sub_module_name, "is pkg")
                pass
            else:
                mod_names.append(root_module_name + "." + sub_module_name)
                mods.append(import_module(sub_module_name))
        except Exception as e:
            traceback.print_exc()
    print('load_cost_time:', time.process_time() - start)
    return mods, mod_names

def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scrapy.utils')
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in pkgutil.iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods

def get_classes_from_submodules(submodules, class_type=None):
    """
    get classes from modules
    :param submodules:
    :param class_type: if specify class_type, return the subclass of the class_type
    :return:
    """
    
    classes = []
    for module in submodules:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if not class_type or (class_type and issubclass(obj, class_type) and obj.__qualname__ != class_type.__qualname__):
                    classes.append(obj)
    return classes


def load_spiders(*, submodules, class_type=Spider):
    return get_classes_from_submodules(submodules, class_type=class_type)

def get_full_classname(klass):
    return klass.__module__ + "." + klass.__qualname__