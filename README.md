# ccpa — the California Consumer Privacy Act, as amended

**This is a share of primary sources and the tooling to quote them. Nothing more.**

Offered **without warranty** and **without any claim of legal gravitas**. Assembled by non-lawyers
doing textual research with substantial AI assistance. Not legal advice. Every claim is tied to a
citation you can check — check it.

## What is here

**All 46 sections of the CCPA as amended by the CPRA** — Civil Code Division 3, Part 4,
Title 1.81.5, §§ 1798.100–1798.199.100. About 25,000 words. Harvested 2026-07-31 from the
California leginfo bulk database snapshot published 2026-07-26.

```
corpus/CIV-*.txt.gz          one file per section
corpus/MANIFEST.tsv          citation, authority tier, validity, version, URL, date, bytes, SHA-256
tools/harvest-statute.py     filter the bulk database, render CAML, store, manifest
sources/registry.md          live URL ⇄ local copy ⇄ retrieval date
```

## Why the bulk database rather than scraping

`downloads.leginfo.legislature.ca.gov` publishes full annual snapshots back to 1989 alongside daily
deltas. That is a *better* provenance story than `utah-id-law` managed: a citation can be pinned to
the text as of a published date, rather than reconstructed by diffing successive fetches.

The cost is that a snapshot is a **1.1 GB database dump, not a document set** — `LAW_SECTION_TBL.dat`
plus one CAML XML `.lob` per section. The harvester filters to the 46 sections it wants and touches
nothing else.

## Using it

```sh
python3 -m venv .venv && .venv/bin/pip install -e ../id-law-kit

.venv/bin/lawcite --corpus corpus CIV-1798.140                   # Definitions
.venv/bin/lawcite --corpus corpus 'Cal. Civ. Code § 1798.130'    # by citation
.venv/bin/lawcite --corpus corpus --grep 'verifiable consumer request'
```

## Known gaps

1. **The regulations are not here.** CCR Title 11, division 6 — the CPPA's implementing rules —
   are **not archived**, and this is the repo's most serious gap. `this.i` @pgu273 records that an
   empty rules layer is not acceptable: `utah-id-law` found its fishing-licence identity
   requirement *only* in the rules, with nothing in the statute. The route is settled
   (`sources/registry.md` §2) and the work is tracked as a tick; until it lands, **no negative
   claim about California law from this repo is safe.**
2. **Enforcement.** CPPA orders and AG settlements, where "reasonable" verification acquires
   operational meaning. Absent.
3. **Other California privacy statutes.** The Information Practices Act (§§ 1798–1798.78),
   CalOPPA (§§ 1798.80–1798.84), the Delete Act, SB 362, the CMIA. Out of scope — this repo is the
   CCPA/CPRA specifically.
4. **Federal preemption and sectoral overlay.** GLBA, HIPAA, FCRA. Several CCPA exemptions turn on
   them; none are here.

## Provenance

`version_id` records the snapshot's **publication** date, taken from the archive's own member
timestamps rather than from the downloaded file's mtime — otherwise two people harvesting the same
published snapshot would disagree about its version.

## Licence

The **original work** — tooling, registry, findings — is **[CC BY 4.0](LICENSE)**. Attribution:
Bakobo, *ccpa*.

The **corpus is not ours to license.** It is the text of California statutes — edicts of
government, which carry no copyright under US law. Redistributed as retrieved, with provenance in
the manifest. The authoritative source remains
[leginfo.legislature.ca.gov](https://leginfo.legislature.ca.gov).

Note this basis is US-specific and does **not** transfer to the EU or India corpora in the sibling
repos, which state their own.
