#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A tool to find missing, redundant, and misplaced unittests."""

import enum
import importlib
import inspect
import os
from pathlib import Path
import time
import types
from typing import Any, Callable
import unittest

from base.log import r, initialize_logging, log_time_delta
import settings

t = ' ' * 4
SEP = '__'
SKIP = ['main', '__init__']


def get_modules(directory: Path, skip: list[Path] = []) \
        -> list[types.ModuleType]:
    modules: list[types.ModuleType] = []
    for f in directory.rglob('*.py'):
        if any(d in f.parents for d in skip):
            continue
        # NOTE import_module('__main__') returns the running test runner
        if f.name == '__main__.py':
            continue
        f = f.relative_to(settings.src)
        mpath = str(f).replace(os.sep, '.')[:-3]
        m = importlib.import_module(mpath)
        modules.append(m)
    return sorted(modules, key=lambda x: x.__name__)


def get_module(mname: str) -> types.ModuleType:
    mpath = mname.replace(os.sep, '.')[:-3]
    return importlib.import_module(mpath)


def get_src_modules() -> list[types.ModuleType]:
    return get_modules(directory=settings.src, skip=[settings.src_tests])


def get_classes(my_module: types.ModuleType) -> dict[str, type[Any]]:
    classes: dict[str, type[Any]] = {}
    for name, c in inspect.getmembers(my_module, inspect.isclass):
        if c.__module__ == my_module.__name__:
            if not issubclass(c, enum.Enum) and name not in SKIP:
                classes[name] = c
    return classes


def get_function_names(my_module: types.ModuleType) -> list[str]:
    functions: list[str] = []
    for name, func in inspect.getmembers(my_module, inspect.isfunction):
        if name in SKIP:
            continue
        if func.__module__ == my_module.__name__:
            functions.append(name)
    return functions


def is_any_method(obj: Any) -> bool:
    """Check for both regular functions and bound class methods."""
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def get_methods(my_class: type) -> list[Callable[..., Any]]:
    abstract_methods: set[str] = set()
    if hasattr(my_class, '__abstractmethods__'):
        abstract_methods = set(getattr(my_class, '__abstractmethods__'))
    methods: list[Callable[..., Any]] = []
    for name, func in inspect.getmembers(my_class, is_any_method):
        if name in abstract_methods:
            continue
        if name in SKIP:
            continue
        is_owned = False
        if inspect.ismethod(func):
            is_owned = func.__self__ is my_class
        else:
            is_owned = func.__qualname__.startswith(my_class.__name__)
        if is_owned:
            methods.append(func)
    return methods


def get_existing_unittests() -> dict[str, list[Path]]:
    test_names: dict[str, list[Path]] = {}
    dpath = settings.src_tests / 'unit'
    for m in get_modules(directory=dpath):
        if m.__file__ is None:
            continue
        test_path = Path(m.__file__).resolve()
        for _, c in inspect.getmembers(m, inspect.isclass):
            for method_name, _ in inspect.getmembers(c, inspect.isfunction):
                if method_name.startswith('test' + SEP):
                    test_names.setdefault(method_name, []).append(test_path)
    return test_names


def get_test_path(my_module: types.ModuleType) -> Path:
    if my_module.__file__ is None:
        raise ValueError(f'Module {my_module.__name__} has no file')
    source_path = Path(my_module.__file__).relative_to(settings.src)
    test_name = f'test__{source_path.stem}.py'
    return settings.src_tests / 'unit' / source_path.parent / test_name


def get_needed_tests() -> dict[str, Path]:
    test_names: dict[str, Path] = {}
    for m in get_src_modules():
        mpath = m.__name__.replace('.', SEP)
        for fname in get_function_names(m):
            tname = f'test{SEP}{mpath}{SEP}{fname}'
            test_names[tname] = get_test_path(m)
        for class_name, c in get_classes(m).items():
            for method in get_methods(c):
                method_name = method.__name__
                tname = f'test{SEP}{mpath}{SEP}{class_name}' \
                        f'{SEP}{method_name}'
                test_names[tname] = get_test_path(m)
    return test_names


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

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

    def test_test_location(self) -> None:
        needed_test_paths = get_needed_tests()
        for test_name, paths in get_existing_unittests().items():
            with self.subTest(test_name):
                expected_path = needed_test_paths.get(test_name)
                if expected_path is None:
                    continue
                for test_path in paths:
                    bool_ = test_path == expected_path.resolve()
                    msg = f'{test_name} must be in {expected_path}'
                    if not bool_:
                        r.error(msg)
                    self.assertTrue(bool_, msg)

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
