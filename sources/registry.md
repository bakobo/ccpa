# Source registry — California consumer privacy law

Live URL ⇄ local copy ⇄ retrieval date. **Trust order** is the `authority_tier` column of each
manifest.

## 1. Statute (`../corpus/`) — CCPA as amended by the CPRA

All 46 sections of Civil Code Division 3, Part 4, Title 1.81.5 (§§ 1798.100–1798.199.100),
extracted from the California leginfo bulk database snapshot, not scraped from the web UI.

| Live | Local | Note |
|---|---|---|
| <https://downloads.leginfo.legislature.ca.gov/> | `../corpus/CIV-*.txt.gz` | Annual database snapshots back to 1989 plus daily deltas. Harvested from `pubinfo_2025.zip` (pubinfo@2026-07-26). Refetch with `tools/harvest-statute.py`. |
| <https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf> | — | CPPA's own statute PDF, effective 2026-01-01. An independent cross-check on the leginfo extraction. Not archived. |

## 2. Regulations (`../corpus-regs/`) — CCR Title 11, Division 6, Chapter 1

**61 sections in force**, plus 30 superseded 2023 wordings retained and
marked `amended`. There is no consolidated current text anywhere we can reach, so the chapter is
assembled from two CPPA rulemaking packages.

| Live | Local | Note |
|---|---|---|
| <https://cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_appr_text.pdf> | `../corpus-regs/CCR-11-*.txt.gz` | The 2025 package — CCPA updates, cybersecurity audits, risk assessments, ADMT, insurance. 49 sections. OAL-approved 2025-09-22, **effective 2026-01-01**. |
| <https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf> | `../corpus-regs/CCR-11-*{,@2023}.txt.gz` | The 2023 package. 42 sections. Twelve of them were untouched by the 2025 action and remain in force; the other thirty are stored with an `@2023` suffix and `validity: amended`. |
| <https://cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_noa.pdf> | — | **The OAL Notice of Approval** — the document that establishes which sections were adopted, amended, and repealed. Transcribed into `../tools/regs_sources.py` and used as a hard oracle at harvest time. |
| <https://govt.westlaw.com/calregs> | — | ❌ **403 to programmatic access.** The apparently canonical route is unusable, which is why the CPPA's own publications are the source of record. |

## 3. Not archived

- **Data broker / DROP regulations** — <https://cppa.ca.gov/regulations/data_broker_regulations.html>.
- **CPPA enforcement orders and AG settlements**, where 'reasonable' verification acquires
  operational meaning.

## Verification flags

1. **Match statute section numbers as strings, never numerically.** `1798.1` and `1798.100` both
   parse as the float `1798.1`. A numeric range filter silently pulls in the Information Practices
   Act (1977), a different statute sharing the 1798 prefix.
2. **The `.lob` payload is CAML XML, not text.** Subdivision labels are separated from their text
   by an empty `<span class="EnSpace"/>`, so a naive tag-strip yields `(a)A business`.
3. **Neither regulations PDF is the whole chapter.** The 2025 text reprints only the sections that
   action touched. Whether the other twelve were unchanged or repealed cannot be inferred from the
   two texts — the NOA says, and it lists no repeals.
4. **PDF extraction interleaves running headers and footers into sentences.** Handled by
   `lawcorpus.pdf`; a leakage check over all 91 items returns zero, with positive controls.
5. **A zero-hit search is a question, not an answer.** `verify the identity of the consumer` finds
   nothing in the statute; `verifiable consumer request` finds 21 lines across 8 sections. Likewise
   'Privacy Protection Agency' appears twice in the regulations, not because extraction failed but
   because everywhere else uses the defined term 'the Agency' (45 times) — confirmed with `zgrep`
   independently of `lawcite`.
