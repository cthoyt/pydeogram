# -*- coding: utf-8 -*-

"""Constants for :mod:`pydeogram`."""

import os

import pystow

__all__ = [
    'module',
    'RESOURCES',
    'TEMPLATES',
]

module = pystow.module('pydeogram')

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
RESOURCES = os.path.join(HERE, 'resources')
TEMPLATES = os.path.join(HERE, 'templates')
