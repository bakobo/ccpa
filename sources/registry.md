# Source registry — California consumer privacy law

Live URL ⇄ local copy ⇄ retrieval date. **Trust order** is the `authority_tier` column of
`../corpus/MANIFEST.tsv`.

## 1. Statute (`../corpus/`) — CCPA as amended by the CPRA

All 46 sections of Civil Code Division 3, Part 4, Title 1.81.5 (§§ 1798.100–1798.199.100),
extracted from the California leginfo bulk database snapshot, not scraped from the web UI.

| Live | Local | Note |
|---|---|---|
| <https://downloads.leginfo.legislature.ca.gov/> | `../corpus/CIV-*.txt.gz` | Annual database snapshots back to 1989 plus daily deltas. Harvested from `pubinfo_2025.zip` (pubinfo@2026-07-26). Per-section URL, hash, and size in `../corpus/MANIFEST.tsv`. Refetch with `tools/harvest-statute.py`. |
| <https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CIV&title=1.81.5.> | — | The human-readable view of the same text; each manifest row links to its own section. |
| <https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf> | — | CPPA's own statute PDF, effective 2026-01-01. Useful as an independent cross-check on the leginfo extraction. Not archived. |

## 2. Regulations (CCR Title 11, div. 6) — ⚠️ NOT YET ARCHIVED

`this.i` @pgu273 records that an empty rules layer is not an acceptable state: utah-id-law found
its fishing-licence identity requirement *only* in the rules, with nothing in the statute. This
repo is currently in that unacceptable state. Tracked as a tick.

The route is settled, only the work remains:

| Source | Status |
|---|---|
| <https://govt.westlaw.com/calregs> | ❌ **403 to programmatic access.** The apparently canonical route is not usable, which is why the CPPA's own publications are the source of record. |
| <https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf> | ✅ Reachable, 515 KB. The CCPA regulations as finalised 2023-03-29. |
| <https://cppa.ca.gov/regulations/ccpa_updates.html> | Later rulemaking packages (ADMT, risk assessments, cybersecurity audits). Which are currently operative needs checking, not guessing. |
| <https://cppa.ca.gov/regulations/data_broker_regulations.html> | Data broker / DROP regulations. |

Harvesting these needs a PDF text-extraction module in `../id-law-kit`, with tests — PDF
extraction has failure modes (column order, ligatures, dropped headers) that Formex and CAML do
not, and a bad extraction is worse than none because it looks like text.

## 3. Enforcement — not archived

CPPA enforcement orders and Attorney General settlements. This is where 'reasonable' verification
acquires operational meaning; none of it is here.

## Verification flags

1. **Match section numbers as strings, never numerically.** `1798.1` and `1798.100` both parse as
   the float `1798.1`. A numeric range filter silently pulls in the Information Practices Act
   (1977), a different statute that happens to share the 1798 prefix.
2. **The `.lob` payload is CAML XML, not text.** Subdivision labels are separated from their text
   by an empty `<span class="EnSpace"/>`, so a naive tag-strip yields `(a)A business` and a
   search for `(a) A business` finds nothing. Handled by `lawcorpus.caml`.
3. **Not every section has a heading.** Some open straight into operative text. `heading()`
   returns empty rather than putting a sentence fragment in the title column.
4. **A zero-hit search is a question, not an answer.** `verify the identity of the consumer`
   returns nothing here; `verifiable consumer request` returns 21 lines across 8 sections. The
   statute's term of art is the second one.
