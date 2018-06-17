#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: __init__.py.py

@time: 22/01/2018 2:59 PM
"""

import inspect
import logging
import pkgutil
import sys
import time
import traceback
from datetime import datetime

from importlib import import_module, reload
from os.path import join
from urllib.parse import urlparse

from jinja2 import Template
from scrapy import Spider

from PyScraper.settings import SCRIPT_TEMPLATES_DIR, GOV_SPIDER_DIR, GOV_SPIDER_MODULE

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
    module = import_module(cl[0:d])
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
    reload(mod)
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
                if not class_type or (
                                class_type and issubclass(obj,
                                                          class_type) and obj.__qualname__ != class_type.__qualname__):
                    classes.append(obj)
    return classes


def load_spiders(*, submodules, class_type=Spider):
    return get_classes_from_submodules(submodules, class_type=class_type)


def get_full_classname(klass):
    return klass.__module__ + "." + klass.__qualname__


def create_script(*, script_name, rules, start_url, mail_to, script_type=None):
    if script_type == 'gov':
        return create_gov_script(script_name, rules, start_url)


def create_gov_script(spider_name, rules, start_url):
    """
    to create a new government script
    :param spider_name: the spider name
    :param rules: the rules for government error correction
    :param start_url: start url for spider
    :param mail_to: mail receiver when rule error occurs
    :return: new government script path
    """
    if not spider_name or not start_url:
        raise Exception("parameters should not be None")
    if not start_url.startswith("http"):
        start_url = "http://" + start_url
    allowed_domain = urlparse(start_url).netloc
    timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    with open(SCRIPT_TEMPLATES_DIR + '/gov_template', 'r') as f:
        script_template = Template(f.read())
    result = script_template.render(spider_name=spider_name, rules=rules, start_url=start_url,
                                    allowed_domain=allowed_domain, datetime=timestamp)
    today = str(datetime.today().date())
    path = join(GOV_SPIDER_DIR, today + "_{spider_name}.py".format(spider_name=spider_name))
    with open(path, 'w+') as f:
        f.write(result)
    spider_modulename = GOV_SPIDER_MODULE + ".{today}_{spider_name}.{spider_name}Spider".format(today=today,
                                                                                                spider_name=spider_name)
    return spider_modulename


def convert_module_name2path(module_name):
    return sys.modules[module_name].__file__