# ccpa — Intent Tree (this.i)

A checkable corpus of California consumer privacy law = goal:
  id: nihog2
  why: >
    Harvest the CCPA as amended by the CPRA (Civil Code §1798.100 et seq.), the CPPA's implementing
    regulations, and the enforcement record, with provenance strong enough to support later
    analysis without repeating the online research. This is the closest of the five regimes to
    utah-id-law's model — statute plus agency rules carries most of the answer — so the driving
    constraint is not methodological novelty but reuse: it is the cheapest place to prove that the
    id-law-kit tooling generalizes off the Utah case it was written for. Tradeoff accepted: a
    corpus whose headline instrument is short, in exchange for exercising the shared toolchain
    against a second US jurisdiction before the harder non-US ones.
  children:
    Statutory text comes from the leginfo bulk snapshots, not page scraping = decision:
      id: 3cpktv
      why: >
        downloads.leginfo.legislature.ca.gov publishes full annual database snapshots back to 1989
        alongside daily deltas. Chose the bulk snapshots over scraping the leginfo web UI, which is
        the obvious route and is what most such projects do. This is a better provenance story than
        utah-id-law achieved: the historical snapshots let a citation be pinned to a text as of a
        date without diffing successive fetches, which is what utah-id-law has to do with SHA-256
        comparison. Tradeoff: the snapshots are database table dumps rather than documents, so
        extraction is a real step with its own failure modes, and the extractor must be validated
        against the live text before any finding rests on it.

    The regulations come from CPPA's own PDFs = decision:
      id: pgu273
      why: >
        Title 11 of the California Code of Regulations is served through govt.westlaw.com/calregs,
        which returns 403 to programmatic access — so the apparently canonical route is not a
        source we can use, and pretending otherwise would leave the rules layer empty. utah-id-law
        established that the rules layer changes answers (the fishing-licence requirement lived
        only there), so an empty rules layer is not an acceptable state. Chose CPPA's published
        PDFs on cppa.ca.gov as the source of record. Tradeoff: PDF extraction quality becomes a
        correctness dependency, and the text we hold is the agency's publication rather than the
        official codified version, which must be stated wherever it is quoted.
      children:
        CCR-11-7026@2023 is pinned at its 2026-08-01 wording, against the current extractor = decision:
          id: xzybrnsx
          why: >
            The re-extract of 2026-09-16 against id-law-kit a0bad96 moved five of the 91 stored
            regulation texts. Four are corrections: a wrapped "section\n 7003." is now rejoined,
            which is what the kit's narrowed number-opener was for. The fifth is a regression.
            id-law-kit now unions every drafting tradition into STRUCTURAL_OPENERS by default, and
            the Indonesian entry `[a-z0-9]{1,3}\.[ \t]` matches the English line " out. Illustrative
            examples follow:", so the rejoiner refuses to attach it to a line ending "…choice to
            opt-" and splits a sentence the 2023 wording does not split. Measured: restricting the
            pattern to `common-law` changes exactly one section across both PDFs — 7026 in the 2023
            package — and reproduces this repo's stored text byte for byte. The same PDF renders a
            line-broken "opt-out" as "opt- out" on one line in two other places, so the split is
            unique to this instance rather than a house rendering.
            Chose to keep the 2026-08-01 text and its manifest row for that one item, over storing
            what the current kit produces. Storing it would put a paragraph break in the corpus that
            is not in the document, and the corpus is what a quotation is checked against. The
            alternative of selecting the tradition here was refused: `structural_pattern()` takes
            the argument but `pdf.extract` does not plumb it through, so this repo could only reach
            it by assigning `lawcorpus.pdf._STRUCTURAL`, and reaching into a private module global
            is the kind of behaviour AGENTS.md says belongs in the kit with tests, not here.
            Tradeoff accepted, and it is a real one: `tools/harvest-regs.py` no longer reproduces
            this item, which is the provenance property the rest of the corpus has. That divergence
            is the reason this node exists, and it ends when the kit either narrows the Indonesian
            opener or lets a caller name its traditions.
