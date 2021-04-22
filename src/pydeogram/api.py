# -*- coding: utf-8 -*-

"""User-facing code."""

import csv
import logging
import os
from functools import lru_cache
from typing import Iterable

from jinja2 import Template

from .constants import TEMPLATES
from .download import ensure_human_refseq

__all__ = [
    'write_ideogram_html',
    'to_ideogram_html',
    'to_ideogram_html_str',
    'get_ideogram_annotations',
]

logger = logging.getLogger(__name__)


def to_ideogram_html(gene_symbols: Iterable[str]):
    """Get an Ideogram HTML document as an HTML object."""
    from IPython.display import HTML
    return HTML(to_ideogram_html_str(gene_symbols))


def write_ideogram_html(gene_symbols: Iterable[str], file=None):
    """Write an Ideogram HTML document to a file."""
    print(to_ideogram_html_str(gene_symbols), file=file)


def to_ideogram_html_str(gene_symbols: Iterable[str]) -> str:
    """Get an Ideogram HTML document as a string."""
    annotations = get_ideogram_annotations(gene_symbols)
    logger.info("using %d annotations in ideogram", len(annotations))
    return get_ideogram_template().render(annotations=annotations)


def get_ideogram_annotations(gene_symbols: Iterable[str]):
    """Get the list of annotations for Ideogram."""
    gene_symbols = set(gene_symbols)
    with open(ensure_human_refseq()) as file:
        return [
            _fix_row_types(row)
            for row in csv.DictReader(file, delimiter="\t")
            if row["name"] in gene_symbols
        ]


def _fix_row_types(row):
    row["start"] = int(row["start"])
    row["stop"] = int(row["stop"])
    return row


@lru_cache(maxsize=1)
def get_ideogram_template() -> Template:
    """Get the Ideogram template."""
    with open(os.path.join(TEMPLATES, "ideogram_template.html"), "rt") as f:
        return Template(f.read())
