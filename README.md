# ccpa — the California Consumer Privacy Act, as amended

**This is a share of primary sources and the tooling to quote them. Nothing more.**

Offered **without warranty** and **without any claim of legal gravitas**. Assembled by non-lawyers
doing textual research with substantial AI assistance. Not legal advice. Every claim is tied to a
citation you can check — check it.

## What is here

Both layers — statute and regulations. About **94,000 words**.

| | Items | Words | What |
|---|---|---|---|
| `corpus/` | 46 | 25,104 | **The statute.** All of Civil Code Title 1.81.5, §§ 1798.100–1798.199.100 |
| `corpus-regs/` | 91 | 68,685 | **The regulations.** CCR Title 11, div. 6, ch. 1 — 61 sections in force, plus 30 superseded 2023 wordings marked `amended` |

```
corpus/CIV-*.txt.gz          one file per statutory section
corpus-regs/CCR-11-*.txt.gz  one file per regulation section; @2023 suffix = superseded wording
*/MANIFEST.tsv               citation, authority tier, validity, version, URL, date, bytes, SHA-256
tools/harvest-statute.py     filter the bulk database, render CAML, store, manifest
tools/harvest-regs.py        extract the rulemaking PDFs, split sections, store, manifest
tools/regs_sources.py        the two packages, and what the OAL notice says happened to each section
sources/registry.md          live URL ⇄ local copy ⇄ retrieval date
```

## Assembling the regulations

There is **no consolidated current text of CCR Title 11 that we can reach** — `govt.westlaw.com`
returns 403 to programmatic access — so the chapter is assembled from two CPPA rulemaking packages:
the 2023 regulations (42 sections) and the 2025 CCPA-updates/cyber/risk/ADMT/insurance package
(49 sections, effective 2026-01-01).

Neither is the whole chapter, and twelve sections appear only in the 2023 text. **Whether those are
unchanged or repealed cannot be inferred from the two texts.** Guessing would be exactly the failure
this repo exists to avoid, so the answer comes from the Office of Administrative Law's Notice of
Approval, which lists 19 sections adopted, 30 amended, and none repealed.

Those lists are transcribed into `tools/regs_sources.py` and used as a **hard oracle**: the harvest
aborts unless the sections it splits out of the 2025 PDF are exactly *adopted ∪ amended*. If a
future rulemaking changes the shape, it stops rather than producing a plausible partial corpus.

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

.venv/bin/lawcite --corpus corpus-regs CCR-11-7001              # regulation, in force
.venv/bin/lawcite --corpus corpus-regs CCR-11-7001@2023         # its superseded wording — bannered
.venv/bin/lawcite --corpus corpus-regs --grep 'risk assessment' --in-force-only
```

`--in-force-only` is what you usually want on the regulations: without it a sweep counts the 2023
wordings alongside the current ones.

## Known gaps

1. **Data broker / DROP regulations** are not here — the Delete Act rules at
   <https://cppa.ca.gov/regulations/data_broker_regulations.html>. Out of scope for now, but they
   are the nearest adjacent rules layer.
2. **Enforcement.** CPPA orders and AG settlements, where "reasonable" verification acquires
   operational meaning. Absent.
3. **Other California privacy statutes.** The Information Practices Act (§§ 1798–1798.78),
   CalOPPA (§§ 1798.80–1798.84), the Delete Act, SB 362, the CMIA. Out of scope — this repo is the
   CCPA/CPRA specifically.
4. **Federal preemption and sectoral overlay.** GLBA, HIPAA, FCRA. Several CCPA exemptions turn on
   them; none are here.

## Provenance

For the statute, `version_id` records the snapshot's **publication** date, taken from the archive's
own member timestamps rather than the downloaded file's mtime — otherwise two people harvesting the
same published snapshot would disagree about its version.

For the regulations, `version_id` names the rulemaking package, and `validity_note` on a superseded
section says what replaced it and when. Quoting a `@2023` item prints that note above the text, so
a wording that was in force from 2023-03-29 to 2025-12-31 cannot be passed off as current law.

The regulations come from PDFs, which is the least trustworthy of the three extraction routes used
across these repos — a PDF is a page description, so extraction infers a reading order and
interleaves running headers and footers into the middle of sentences. `lawcorpus.pdf` strips that
furniture; a leakage check over all 91 items returns zero hits, with positive controls to prove the
search itself works. Spot-check anything load-bearing against the source PDF.

## Licence

The **original work** — tooling, registry, findings — is **[CC BY 4.0](LICENSE)**. Attribution:
Bakobo, *ccpa*.

The **corpus is not ours to license.** It is the text of California statutes — edicts of
government, which carry no copyright under US law. Redistributed as retrieved, with provenance in
the manifest. The authoritative source remains
[leginfo.legislature.ca.gov](https://leginfo.legislature.ca.gov).

Note this basis is US-specific and does **not** transfer to the EU or India corpora in the sibling
repos, which state their own.
