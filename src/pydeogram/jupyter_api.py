# -*- coding: utf-8 -*-

"""Jupyter plugins for pydeogram."""

from typing import TYPE_CHECKING, Iterable, Optional

from .constants import ENVIRONMENT
from .utils import get_ideogram_annotations

if TYPE_CHECKING:
    import IPython.display

__all__ = ["prepare_jupyter", "to_jupyter", "to_javascript"]

JUPYTER_TEMPLATE = ENVIRONMENT.get_template("ideogram_jupyter.js")
DEFAULT_ID = "ideo-container"


def prepare_jupyter(container: Optional[str] = None) -> "IPython.display.Javascript":
    """Prepare a Jupyter cell for Ideogram content."""
    from IPython.display import Javascript

    if container is None:
        container = DEFAULT_ID
    return Javascript(f"""element.append("<div id='{container}'></div>");""")


def to_jupyter(gene_symbols: Iterable[str], **kwargs) -> "IPython.display.Javascript":
    """Get an Ideogram as a Javascript object for a Jupyter notebook."""
    from IPython.display import Javascript

    return Javascript(to_javascript(gene_symbols=gene_symbols, **kwargs))


def to_javascript(
    gene_symbols: Iterable[str],
    *,
    container: Optional[str] = None,
) -> str:
    """Create the Ideogram Javascript string."""
    annotations = get_ideogram_annotations(gene_symbols)
    if container is None:
        container = DEFAULT_ID
    return JUPYTER_TEMPLATE.render(
        annotations=annotations,
        container=container,
    )
