# -*- coding: utf-8 -*-

"""Download functions for :mod:`pydeogram`."""

import csv
import gzip
import logging
import os
from typing import Mapping

from tqdm import tqdm

from .constants import RESOURCES, module

__all__ = [
    'ensure_human_refseq',
    'get_chromosome_map',
]

logger = logging.getLogger(__name__)

REFSEQ_HUMAN_PATH = os.path.join(RESOURCES, "refseq_human.tsv")
GENE_REFSEQ_URL = "ftp://ftp.ncbi.nih.gov/gene/DATA/gene2refseq.gz"
GENE_INFO_URL = "https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/Homo_sapiens.gene_info.gz"


def ensure_human_refseq(
    force_extract: bool = False,
    force_download: bool = False,
    cleanup: bool = True,
) -> str:
    """Return the path of the human filtered RefSeq file if it exists, otherwise download and generate it.

    :param force_extract: If true, forces the regeneration of the human filtered RefSeq file
    :param force_download: If true, forces the re-download of the RefSeq file
    :param cleanup:If true, deletes the large (~1GB RefSeq file after filtering for human content)
    :returns: The path to the human filtered RefSeq file
    """
    if os.path.exists(REFSEQ_HUMAN_PATH) and not force_extract:
        return REFSEQ_HUMAN_PATH

    chromosome_map = get_chromosome_map(force_download=force_download)
    full_path = module.ensure(url=GENE_REFSEQ_URL, force=force_download)
    rows = []
    with gzip.open(full_path, "rt") as file:
        reader = csv.reader(file, delimiter="\t")
        _ = next(reader)  # skip header
        # there are about 46.3M rows, takes about 3 minutes
        for row in tqdm(reader, desc="Processing refseq data", unit_scale=True, total=46_400_000):
            if row[0] != "9606":  # skip non-human genes
                continue
            if row[12] != "Reference GRCh38.p13 Primary Assembly":  # only keep primary assembly
                continue
            if row[2] == "SUPPRESSED":  # skip suppressed records
                continue
            rows.append((
                row[1],  # ncbigene identifier
                row[15],  # symbol
                chromosome_map.get(row[1], ""),  # chromosome
                row[9],  # start
                row[10],  # stop
            ))

    rows = sorted(set(rows), key=lambda x: int(x[0]))
    with open(REFSEQ_HUMAN_PATH, "w") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(("ncbigene_id", "name", "chr", "start", "stop"))
        writer.writerows(rows)

    if cleanup:
        os.remove(full_path)

    return REFSEQ_HUMAN_PATH


def get_chromosome_map(force_download: bool = False) -> Mapping[str, str]:
    """Get the chromosome map."""
    path = module.ensure(url=GENE_INFO_URL, force=force_download)
    with gzip.open(path, "rt") as file:
        reader = csv.reader(file, delimiter="\t")
        _ = next(reader)
        return {row[1]: row[6] for row in reader}
