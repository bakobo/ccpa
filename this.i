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
