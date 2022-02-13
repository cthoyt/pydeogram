# -*- coding: utf-8 -*-

"""Download functions for :mod:`pydeogram`."""

import csv
import gzip
import logging
import os
from pathlib import Path
from typing import Any, Iterable, List, Mapping

from tqdm import tqdm

from .constants import MODULE

__all__ = [
    "ensure_human_refseq",
    "get_chromosome_map",
    "get_ideogram_annotations",
]

logger = logging.getLogger(__name__)

REFSEQ_HUMAN_PATH = MODULE.join(name="refseq_human.tsv")
GENE_REFSEQ_URL = "ftp://ftp.ncbi.nih.gov/gene/DATA/gene2refseq.gz"
GENE_INFO_URL = "https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/Homo_sapiens.gene_info.gz"


def ensure_human_refseq(
    force_extract: bool = False,
    force: bool = False,
    cleanup: bool = True,
) -> Path:
    """Return the path of the human filtered RefSeq file if it exists, otherwise download and generate it.

    :param force_extract: If true, forces the regeneration of the human filtered RefSeq file
    :param force: If true, forces the re-download of the RefSeq file
    :param cleanup:If true, deletes the large (~1GB RefSeq file after filtering for human content)
    :returns: The path to the human filtered RefSeq file
    """
    if os.path.exists(REFSEQ_HUMAN_PATH) and not force_extract:
        return REFSEQ_HUMAN_PATH

    chromosome_map = get_chromosome_map(force=force)
    full_path = MODULE.ensure(url=GENE_REFSEQ_URL, force=force)
    rows = []
    with gzip.open(full_path, "rt") as file:
        reader = csv.reader(file, delimiter="\t")
        _ = next(reader)  # skip header
        # there are about 46.3M rows, takes about 3 minutes
        for row in tqdm(reader, desc="Processing refseq data", unit_scale=True, total=54_000_000):
            if row[0] != "9606":  # skip non-human genes
                continue
            if row[12] != "Reference GRCh38.p13 Primary Assembly":  # only keep primary assembly
                continue
            if row[2] == "SUPPRESSED":  # skip suppressed records
                continue
            rows.append(
                (
                    row[1],  # ncbigene identifier
                    row[15],  # symbol
                    chromosome_map.get(row[1], ""),  # chromosome
                    row[9],  # start
                    row[10],  # stop
                )
            )

    rows = sorted(set(rows), key=lambda x: int(x[0]))
    with REFSEQ_HUMAN_PATH.open("w") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(("ncbigene_id", "name", "chr", "start", "stop"))
        writer.writerows(rows)

    if cleanup:
        os.remove(full_path)

    return REFSEQ_HUMAN_PATH


def get_chromosome_map(force: bool = False) -> Mapping[str, str]:
    """Get the chromosome map from RefSeq."""
    with MODULE.ensure_open_gz(url=GENE_INFO_URL, force=force, mode="rt") as file:
        reader = csv.reader(file, delimiter="\t")
        _ = next(reader)
        return {row[1]: row[6] for row in reader}


def get_ideogram_annotations(gene_symbols: Iterable[str]) -> List[Mapping[str, Any]]:
    """Get the list of annotations for Ideogram."""
    gene_symbols = set(gene_symbols)
    with ensure_human_refseq().open() as file:
        return [
            _fix_row_types(row)
            for row in csv.DictReader(file, delimiter="\t")
            if row["name"] in gene_symbols
        ]


def _fix_row_types(row):
    row["start"] = int(row["start"])
    row["stop"] = int(row["stop"])
    return row
