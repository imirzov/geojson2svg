#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import inspect
import logging
from pathlib import Path

import settings
from settings import report as r


def initialize_logging(erase: bool = True, test: bool = False,
                       level: int = settings.log_level,
                       caller: str | None = None) -> Path:
    # Define log file name and subfolder
    if caller is None:
        caller = inspect.stack()[1][1]
    subfolder = ''
    for name in ('tests', 'app1', 'app2', 'app3'):
        if os.sep + name in caller:
            subfolder = name
            break
    log_dir = settings.logs / subfolder
    log_dir.mkdir(parents=True, exist_ok=True)
    caller = os.path.basename(caller)
    log_file = log_dir / (caller[:-3] + '.log')
    if erase and log_file.is_file():
        try:
            log_file.unlink()
        except Exception:
            logging.error(f'Failed to delete log file:\n{log_file}')

    class ClassAwareFormatter(logging.Formatter):

        def format(self, record: logging.LogRecord) -> str:
            if '.' not in record.funcName:
                frame = inspect.currentframe()
                # Go back 8 frames to match the original logic
                for _ in range(8):
                    if frame is not None:
                        frame = frame.f_back
                while frame:
                    local_self = frame.f_locals.get('self')
                    local_cls = frame.f_locals.get('cls')
                    obj = local_self or local_cls
                    if obj is not None:
                        cls = obj if isinstance(obj, type) else type(obj)
                        if cls.__name__ not in ('Logger', 'RootLogger'):
                            record.funcName =\
                                f'{cls.__name__}.{record.funcName}'
                            break
                    frame = frame.f_back
            return super().format(record)

    fmt = '%(levelname)s: %(module)s.%(funcName)s()\n%(message)s\n'
    # fmr = logging.Formatter(fmt)
    fmr = ClassAwareFormatter(fmt)

    # Close opened log files before opening a new one
    for handler in r.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()

    if not test:
        fh = logging.FileHandler(log_file, encoding=settings.encoding)
        fh.setFormatter(fmr)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmr)

        r.setLevel(level)
        r.handlers = [fh, sh]

    s = 'START' if erase else 'UPDATE'
    t = settings.time_now()
    r.info(f'{s} {t}\n\n\n')
    return log_file
