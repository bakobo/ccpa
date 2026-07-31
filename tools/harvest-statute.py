#!/usr/bin/env python3
"""Harvest the CCPA/CPRA statutory text from the California leginfo bulk database.

California publishes full annual snapshots of its legislative database at
`downloads.leginfo.legislature.ca.gov`, back to 1989, alongside daily deltas. That is a better
provenance story than scraping the web UI: a citation can be pinned to the text as of a date
without diffing successive fetches. See `this.i` @3cpktv.

The cost is that a snapshot is a **database dump, not a document set**, and it is ~1.1 GB:

    LAW_SECTION_TBL.dat   backtick-quoted, tab-separated; one row per codified section
    LAW_SECTION_TBL_*.lob one CAML XML file per section, named in column 15 of the row

So the pipeline is: filter rows to the sections we want, pull only those .lob members out of the
zip, render CAML to text. Nothing else in the 1.1 GB is touched.

    python3 tools/harvest-statute.py --zip /path/to/pubinfo_2025.zip
    python3 tools/harvest-statute.py --download        # fetch the current annual snapshot first
"""

import argparse
import datetime
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

from lawcorpus.caml import CamlError, heading, to_text
from lawcorpus.errors import LawcorpusError
from lawcorpus.manifest import Manifest, ManifestItem
from lawcorpus.store import CorpusStore

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
SNAPSHOT_URL = "https://downloads.leginfo.legislature.ca.gov/pubinfo_2025.zip"

SECTIONS_TABLE = "LAW_SECTION_TBL.dat"

# The CCPA as amended by the CPRA: Civil Code Division 3, Part 4, Title 1.81.5,
# sections 1798.100 through 1798.199.100.
#
# Matched as a STRING, deliberately. Numeric comparison conflates '1798.1' with '1798.100' — both
# parse as the float 1798.1 — which would silently pull in the Information Practices Act, a
# different statute from 1977.
CCPA_SECTION = re.compile(r"^1798\.(1[0-9][0-9]|199)")
CODE = "CIV"


class HarvestError(LawcorpusError):
    code = "BK_CCPA_HARVEST"


def rows_for_code(dat_path: Path, code: str):
    """Yield the parsed rows of LAW_SECTION_TBL.dat belonging to one code."""
    marker = f"`{code}`"
    with dat_path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 15 or cols[1] != marker:
                continue
            yield [c.strip("`") for c in cols]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--zip", type=Path, help="a pubinfo_*.zip already on disk")
    p.add_argument("--download", action="store_true", help=f"fetch {SNAPSHOT_URL} first")
    p.add_argument("--work", type=Path, default=Path("/tmp"), help="scratch directory")
    args = p.parse_args(argv)

    snapshot = args.zip
    if args.download or snapshot is None:
        snapshot = args.work / "pubinfo_2025.zip"
        if not snapshot.exists():
            print(f"Downloading {SNAPSHOT_URL} (~1.1 GB)...")
            urllib.request.urlretrieve(SNAPSHOT_URL, snapshot)
    if not snapshot.exists():
        raise HarvestError(
            f"No snapshot at {snapshot}. Pass --zip with a downloaded pubinfo_*.zip, or "
            f"--download to fetch the current annual snapshot."
        )

    archive = zipfile.ZipFile(snapshot)
    dat = args.work / SECTIONS_TABLE
    if not dat.exists():
        print(f"Extracting {SECTIONS_TABLE}...")
        archive.extract(SECTIONS_TABLE, args.work)

    wanted = {}
    for cols in rows_for_code(dat, CODE):
        section = cols[2].rstrip(".")
        if CCPA_SECTION.match(section) and cols[14].endswith(".lob"):
            # A section can appear more than once across historical versions; the snapshot's active row is
            # the one flagged 'Y' in column 16.
            if len(cols) > 15 and cols[15] != "Y" and section in wanted:
                continue
            wanted[section] = (cols[14], cols[13])

    if not wanted:
        raise HarvestError(
            f"No {CODE} sections matched {CCPA_SECTION.pattern} in {dat}. The table layout may "
            f"have changed — check that column 2 is the code and column 15 the .lob filename."
        )
    print(f"{len(wanted)} CCPA section(s) identified.")

    store = CorpusStore(CORPUS)
    retrieved = datetime.date.today().isoformat()
    # The zip's own member timestamps, NOT the local file mtime. curl does not preserve
    # Last-Modified unless asked, so file mtime records when *we* downloaded it — which would
    # make two people harvesting the same published snapshot disagree about its version.
    snapshot_date = _snapshot_date(archive)
    items, failures = [], []

    for section in sorted(wanted, key=_section_key):
        lob, _history = wanted[section]
        item_id = f"CIV-{section}"
        try:
            text = to_text(archive.read(lob))
            title = heading(archive.read(lob)) or f"Civil Code section {section}"
            written = store.write(item_id, text)
        except (CamlError, KeyError) as e:
            print(f"  {section}: FAILED — {e}")
            failures.append(section)
            continue
        items.append(
            ManifestItem(
                item_id=item_id,
                citation=f"Cal. Civ. Code § {section}",
                title=title,
                authority_tier="legislative",
                validity="in-force",
                validity_note="",
                # The snapshot date IS the version: leginfo keeps annual snapshots back to 1989,
                # so a citation pins the text as published on that date.
                version_id=f"pubinfo@{snapshot_date}",
                lang="eng",
                source_url=(
                    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
                    f"?lawCode=CIV&sectionNum={section}"
                ),
                retrieved=retrieved,
                media_type="application/xml;type=caml",
                bytes=written.bytes,
                sha256=written.sha256,
            )
        )
        print(f"  {section}: {written.bytes:,} bytes — {title[:70]}")

    Manifest(items).write(CORPUS / "MANIFEST.tsv")
    print(f"\nManifest: {len(items)} item(s) at {CORPUS / 'MANIFEST.tsv'}")
    if failures:
        print(f"{len(failures)} failure(s): {', '.join(failures)}")
        return 1
    return 0


def _snapshot_date(archive: zipfile.ZipFile) -> str:
    """The publication date of the snapshot, taken from the archive's member timestamps."""
    latest = max(info.date_time for info in archive.infolist())
    return datetime.date(latest[0], latest[1], latest[2]).isoformat()


def _section_key(section: str):
    return tuple(int(part) if part.isdigit() else 0 for part in section.split("."))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LawcorpusError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
