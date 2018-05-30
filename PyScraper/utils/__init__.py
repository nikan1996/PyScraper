#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: __init__.py.py

@time: 22/01/2018 2:59 PM
"""
import importlib


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
