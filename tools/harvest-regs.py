#!/usr/bin/env python3
"""Harvest CCR Title 11, Division 6, Chapter 1 — the CCPA regulations.

`this.i` @pgu273 records why an empty rules layer was not an acceptable state:
`utah-id-law` found its fishing-licence identity requirement *only* in the administrative rules,
with nothing in the statute, so a statute-only corpus answers the wrong question confidently.

There is no consolidated current text we can reach — Westlaw 403s — so the chapter is assembled
from two CPPA rulemaking packages, and the Office of Administrative Law's Notice of Approval says
which sections each one touched. See `regs_sources.py` for the lists and why they are transcribed
rather than parsed.

The harvest is **checked against the NOA before anything is stored**: the sections split out of
the 2025 text must be exactly the adopted set plus the amended set. If they are not, the shape of
the source has changed and a silent partial harvest is the worst possible outcome, so it aborts.

    python3 tools/harvest-regs.py            # download what is missing, then harvest
    python3 tools/harvest-regs.py --cached   # use PDFs already in the work directory
"""

import argparse
import datetime
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from regs_sources import (  # noqa: E402
    ADOPTED_2025,
    AMENDED_2025,
    PACKAGES,
    REPEALED_2025,
    SUPERSEDED_NOTE,
)

from lawcorpus.errors import LawcorpusError  # noqa: E402
from lawcorpus.manifest import Manifest, ManifestItem  # noqa: E402
from lawcorpus.pdf import extract  # noqa: E402
from lawcorpus.store import CorpusStore  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus-regs"

# A section heading opens a line: "§ 7001. Definitions." Cross-references inside the prose say
# "section 7015" or "Civil Code section 1798.140" and carry no section sign, so they cannot match.
SECTION_HEADING = re.compile(r"^\s*§\s*(7\d{3}(?:\.\d+)?)\.\s*(.*)$")


class HarvestError(LawcorpusError):
    code = "BK_CCPA_REGS"


def split_sections(text: str) -> dict:
    """Split an extracted regulations text into {section_number: (heading, body)}."""
    sections, current, buffer = {}, None, []
    for line in text.splitlines():
        m = SECTION_HEADING.match(line)
        if m:
            if current:
                sections[current[0]] = (current[1], "\n".join(buffer).strip())
            current, buffer = (m.group(1), m.group(2).strip()), [line]
        elif current:
            buffer.append(line)
    if current:
        sections[current[0]] = (current[1], "\n".join(buffer).strip())
    return sections


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--work", type=Path, default=Path("/tmp"), help="where PDFs are cached")
    p.add_argument("--cached", action="store_true", help="do not download; use cached PDFs")
    args = p.parse_args(argv)

    texts = {}
    for pkg in PACKAGES:
        path = args.work / Path(pkg["url"]).name
        if not path.exists():
            if args.cached:
                raise HarvestError(f"No cached PDF at {path}, and --cached was given.")
            print(f"Downloading {pkg['url']}...")
            urllib.request.urlretrieve(pkg["url"], path)
        texts[pkg["key"]] = split_sections(extract(path))
        print(f"{pkg['key']} package: {len(texts[pkg['key']])} sections")

    # ---- Oracle: the 2025 text must match the OAL Notice of Approval, exactly. ----
    expected = ADOPTED_2025 | AMENDED_2025
    found = set(texts["2025"])
    if found != expected:
        raise HarvestError(
            "The 2025 approved text does not match the OAL Notice of Approval. Missing from the "
            f"text: {sorted(expected - found) or 'none'}. Present but not in the notice: "
            f"{sorted(found - expected) or 'none'}. Either the PDF changed or the section splitter "
            "is wrong; storing a partial chapter would produce a corpus that looks complete."
        )
    print(f"NOA check: {len(found)} sections match the notice exactly "
          f"({len(ADOPTED_2025)} adopted + {len(AMENDED_2025)} amended).")

    if REPEALED_2025:
        raise HarvestError(
            "regs_sources.REPEALED_2025 is non-empty, but this harvester assumes nothing was "
            "repealed. Handle repeals explicitly before continuing."
        )

    store = CorpusStore(CORPUS)
    retrieved = datetime.date.today().isoformat()
    pkg_by_key = {pkg["key"]: pkg for pkg in PACKAGES}
    items = []

    # Current chapter: every 2025 section, plus the 2023 sections that action left untouched.
    unchanged = set(texts["2023"]) - expected
    for section, (heading, body) in sorted(texts["2025"].items()):
        items.append(_item(store, section, heading, body, pkg_by_key["2025"], retrieved))
    for section in sorted(unchanged):
        heading, body = texts["2023"][section]
        items.append(_item(store, section, heading, body, pkg_by_key["2023"], retrieved))

    # The superseded 2023 wording of every amended section, kept because a question about conduct
    # before 2026-01-01 needs it. Marked `amended`, so cite.py banners it rather than passing it
    # off as current law.
    superseded = 0
    for section in sorted(set(texts["2023"]) & expected):
        heading, body = texts["2023"][section]
        items.append(
            _item(
                store,
                section,
                heading,
                body,
                pkg_by_key["2023"],
                retrieved,
                item_suffix="@2023",
                validity="amended",
                validity_note=SUPERSEDED_NOTE,
            )
        )
        superseded += 1

    Manifest(items).write(CORPUS / "MANIFEST.tsv")
    in_force = len(items) - superseded
    print(
        f"\nStored {len(items)} item(s): {in_force} in force "
        f"({len(texts['2025'])} from the 2025 package, {len(unchanged)} unchanged from 2023), "
        f"{superseded} superseded 2023 wordings."
    )
    print(f"Manifest: {CORPUS / 'MANIFEST.tsv'}")
    return 0


def _item(store, section, heading, body, pkg, retrieved, item_suffix="",
          validity="in-force", validity_note=""):
    item_id = f"CCR-11-{section}{item_suffix}"
    if not body.strip():
        raise HarvestError(
            f"Section {section} extracted to an empty body. That is a splitter or extraction "
            f"failure, not a section with no text."
        )
    written = store.write(item_id, body + "\n")
    return ManifestItem(
        item_id=item_id,
        citation=f"11 CCR § {section}{(' ' + pkg['citation_suffix']) if pkg['citation_suffix'] and item_suffix else ''}".strip(),
        title=heading or f"CCR Title 11 section {section}",
        authority_tier="delegated",
        validity=validity,
        validity_note=validity_note,
        version_id=pkg["version_id"],
        lang="eng",
        source_url=pkg["url"],
        retrieved=retrieved,
        media_type="application/pdf",
        bytes=written.bytes,
        sha256=written.sha256,
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LawcorpusError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
