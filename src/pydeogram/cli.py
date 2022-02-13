# -*- coding: utf-8 -*-

"""Command line interface for :mod:`pydeogram`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m pydeogram`` python will execute``__main__.py`` as a script.
  That means there won't be any ``pydeogram.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``pydeogram.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import logging
import sys

import click

__all__ = ["main"]

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main():
    """CLI for pydeogram."""


@main.command()
def build():
    """Build the resource files from scratch."""
    from .utils import ensure_human_refseq

    ensure_human_refseq(force=True, force_extract=True, cleanup=True)


@main.command()
@click.argument("symbols", nargs=-1)
@click.option("-o", "--output", type=click.File("w"), default=sys.stdout)
def write(symbols, output):
    """Write an Ideogram HTML file."""
    from .api import to_html_file

    to_html_file(gene_symbols=symbols, file=output)


if __name__ == "__main__":
    main()
