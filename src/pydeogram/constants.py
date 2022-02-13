# -*- coding: utf-8 -*-

"""Constants for :mod:`pydeogram`."""

from pathlib import Path

import pystow
from jinja2 import Environment, FileSystemLoader

__all__ = [
    "MODULE",
    "TEMPLATES",
    "ENVIRONMENT",
]

HERE = Path(__file__).parent.resolve()
TEMPLATES = HERE / "templates"

MODULE = pystow.module("pydeogram")

#: The Jinja2 file system loader
LOADER = FileSystemLoader(TEMPLATES)

#: The Jinja2 environment for the package
ENVIRONMENT = Environment(
    autoescape=True,
    loader=LOADER,
    trim_blocks=False,
)
ENVIRONMENT.globals["STATIC_PREFIX"] = HERE / "static"
