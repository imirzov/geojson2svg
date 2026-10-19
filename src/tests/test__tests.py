#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A tool to find missing unittests."""

import os
import unittest
import time
import importlib
import core.utils
import inspect
import re
import types
from typing import Any, Callable
import enum
from pathlib import Path

import core
import log
import settings
from settings import report as r

t = ' ' * 4
SEP = '__'
SKIP = ['abstractmethod', 'override', 'cast', 'Counter',
        'dataclass', 'field', 'Any', 'main', 'Path',
        '__init__', '__eq__', '__repr__', '_plot_lines']


def get_modules(directory: str, recursive: bool = True) \
        -> list[types.ModuleType]:
    modules: list[types.ModuleType] = []
    plist: list[str | Path] = [settings.src, directory, '**', '*.py']
    for f in core.utils.glob_files(plist, recursive=recursive):
        f = f.relative_to(settings.src)
        mpath = str(f).replace(os.sep, '.')[:-3]
        if '__init__' not in mpath:
            m = importlib.import_module(mpath)
            modules.append(m)
    return sorted(modules, key=lambda x: x.__name__)


def get_module(mname: str) -> types.ModuleType:
    mpath = mname.replace(os.sep, '.')[:-3]
    return importlib.import_module(mpath)


def get_src_modules() -> list[types.ModuleType]:
    modules: list[types.ModuleType] = []
    modules.extend(get_modules('base'))
    modules.extend(get_modules('core'))
    modules.append(get_module('settings.py'))
    # TODO Add other source files as needed
    return sorted(modules, key=lambda x: x.__name__)


def get_classes(my_module: types.ModuleType) -> dict[str, type[Any]]:
    classes: dict[str, type[Any]] = {}
    for name, c in inspect.getmembers(my_module, inspect.isclass):
        if c.__module__ == my_module.__name__:
            if not issubclass(c, enum.Enum) and name not in SKIP:
                classes[name] = c
    return classes


def get_function_names(my_module: types.ModuleType) -> list[str]:
    functions: list[str] = []
    for name, _ in inspect.getmembers(my_module, inspect.isfunction):
        if name not in SKIP:
            functions.append(name)
    return functions


def get_methods(my_class: type) -> list[Callable[..., Any]]:
    abstract_methods: set[str] = set()
    if hasattr(my_class, '__abstractmethods__'):
        abstract_methods = set(getattr(my_class, '__abstractmethods__'))
    methods: list[Callable[..., Any]] = []
    for name, func in inspect.getmembers(my_class, inspect.isfunction):
        if name not in abstract_methods \
            and name not in SKIP \
                and func.__qualname__.startswith(my_class.__name__):
            # and not name.startswith('_') \
            methods.append(func)
            # r.info(func.__qualname__)
    return methods


def get_existing_unittests() -> list[str]:
    test_names: list[str] = []
    for m in get_modules('tests/unit'):
        for _, c in inspect.getmembers(m, inspect.isclass):
            for method_name, _ in inspect.getmembers(c, inspect.isfunction):
                if method_name.startswith('test_'):
                    test_names.append(method_name)
    return test_names


def get_needed_tests() -> list[str]:
    test_names: list[str] = []
    for m in get_src_modules():
        mpath = re.sub(r'_\d\d_', '', m.__name__)
        mpath = mpath.replace('.', SEP)
        for fname in get_function_names(m):
            tname = f'test{SEP}{mpath}{SEP}{fname}'
            test_names.append(tname)
        for class_name, c in get_classes(m).items():
            for method in get_methods(c):
                method_name = method.__name__
                tname = f'test{SEP}{mpath}{SEP}{class_name}{SEP}{method_name}'
                test_names.append(tname)
    return test_names


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    def test_self(self) -> None:
        msg = ''
        for m in get_src_modules():
            for fname in get_function_names(m):
                msg += f'{m.__name__}.{fname}\n'
            for class_name, c in get_classes(m).items():
                msg += f'{m.__name__}.{class_name}\n'
                for method in get_methods(c):
                    msg += f'{m.__name__}.{class_name}.{method.__name__}\n'
        r.info(msg)

    def test_missing(self) -> None:
        existing_test_names = get_existing_unittests()
        for test_name in get_needed_tests():
            with self.subTest(test_name):
                bool_ = test_name in existing_test_names
                msg = f'\n\n{t}@unittest.skip(\'TODO: implement test\')\n' \
                    + f'{t}def {test_name}(self) -> None:\n' \
                    + f'{t * 2}# ' + 'f = ...\n' \
                    + f'{t * 2}# ' + 'try:\n' \
                    + f'{t * 2}# {t}' + 'f(...)\n' \
                    + f'{t * 2}# ' + 'except Exception as e:\n' \
                    + f'{t * 2}# {t}' + "msg = f'{f.__name__} raised ' \\\n" \
                    + f'{t * 2}# {t * 2}' + "  f'{e.__class__.__name__}: " \
                    + "{e}\\n' \\\n" \
                    + f'{t * 2}# {t * 2}' + "  + traceback.format_exc()\n" \
                    + f'{t * 2}# {t}' + "r.error(msg)\n" \
                    + f'{t * 2}# {t}' + "self.fail(msg)\n" \
                    + f'{t * 2}' + 'pass\n'

                if not bool_:
                    r.error(msg)
                self.assertTrue(bool_, msg)

    def test_redundant(self) -> None:
        needed_test_names = get_needed_tests()
        for tname in get_existing_unittests():
            with self.subTest(tname):
                bool_ = tname in needed_test_names
                msg = 'Redundant ' + tname
                if not bool_:
                    r.error(msg)
                self.assertTrue(bool_, msg)

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
