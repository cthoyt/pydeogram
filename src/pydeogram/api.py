# -*- coding: utf-8 -*-

"""Generate HTML files."""

import logging
import os
from typing import Iterable, Optional

from .constants import ENVIRONMENT
from .utils import get_ideogram_annotations

__all__ = [
    "to_html_path",
    "to_html_file",
    "to_html_str",
]

logger = logging.getLogger(__name__)

HTML_TEMPLATE = ENVIRONMENT.get_template("ideogram_template.html")


def to_html_path(gene_symbols: Iterable[str], path: os.PathLike, **kwargs):
    """Write an Ideogram HTML document to a file."""
    with open(path, "w") as file:
        to_html_file(gene_symbols=gene_symbols, file=file, **kwargs)


def to_html_file(gene_symbols: Iterable[str], *, file=None, **kwargs):
    """Write an Ideogram HTML document to a file."""
    print(to_html_str(gene_symbols, **kwargs), file=file)  # noqa:T001


def to_html_str(
    gene_symbols: Iterable[str], container: Optional[str] = None, title: Optional[str] = None
) -> str:
    """Get an Ideogram HTML document as a string."""
    annotations = get_ideogram_annotations(gene_symbols)
    logger.info("using %d annotations in ideogram", len(annotations))
    return HTML_TEMPLATE.render(
        annotations=annotations,
        container=container or "body",
        title=title or "Ideogram",
    )
