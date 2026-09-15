<!-- >>> bakobo standards >>> (managed by dev/sync-tier1) -->

## Bakobo engineering standards

How every Bakobo repo builds is governed by cross-cutting standards, canonical in the sibling
[`bakobo/dev`](../dev) repo. If `../dev` is not checked out beside this one, clone it before design
work: `git clone --depth 1 https://github.com/bakobo/dev`. Always on:

- **Intent-first** development and **strict TDD at 100% branch coverage of new code** — see the
  sections below and [`dev/methodology.md`](../dev/methodology.md). A `this.i` node's `id:` is
  opaque base32 — `^[a-z2-7]{8}$`, from a real random source
  (`tr -dc 'a-z2-7' < /dev/urandom | head -c 8`), never a semantic label and never hand-typed.
- **Fail closed.** Untrusted input never carries authority; when something can't be checked, the
  effect does not land ([`org` principle 8](../org/design/purpose-and-principles.md)).
- **High-quality errors.** Every error carries a stable symbolic code, says whether retrying could
  help (permanent vs. transient), and reads as complete, plain sentences in the house voice — never
  "something went wrong." Full standard: [`dev/standards/error-handling.md`](../dev/standards/error-handling.md).
- **Error codes are named, not invented.** A code is `<sorter>.<descriptor>[.<sub>].<disposition>` —
  `e.state.conflict.r`, `w.feature.deprecated.f` — classified by what the *obstacle* was rather than
  by which component raised it, with retryability in the trailing token so a caller can prefix-match
  a whole branch of meaning. Codes are globally unique across Bakobo and declared as module-scope
  literals. **Declarative configuration is in scope** — an OpenTofu `precondition`, an Ansible
  `assert` — and carries its code as a literal prefix on the message, `"<code>: <sentence>"`, since
  no single module-scoped value can represent a per-instance one; test-assertion messages are the
  one exclusion. Full standard: [`dev/standards/error-codes.md`](../dev/standards/error-codes.md);
  the HTTP wire format is [`dev/standards/http-errors.md`](../dev/standards/http-errors.md) and the
  declarative binding is [`dev/standards/config-errors.md`](../dev/standards/config-errors.md).
- **Repo layout.** Architecture and developer docs live in `docs/`; the root holds only repo-level
  files (`README`, `LICENSE`, `CONTRIBUTING`), the instruction/config files, build manifests, and
  `this.i` at the root as the source of truth. Don't leave `design.md` loose at the root. Full
  standard, including the content-repo nuance: [`dev/standards/repo-layout.md`](../dev/standards/repo-layout.md).
- **Terminology.** Bakobo's architecture has a precise vocabulary (`core`, `steward`, `mint`, …). Its
  single source of truth is [`bakobo/glossary`](https://github.com/bakobo/glossary), reached via the
  `glossary` MCP server. Where a word is doing a Bakobo concept's work, reconcile prose to the
  glossary (not the reverse), mint/amend terms in-band through the MCP (never hand-edit), and don't
  let a general word masquerade as a formal term. **Consulting the glossary before using a term is a
  suggestion, not a requirement** — it is often a good idea and sometimes noise, because plenty of
  words are ordinary English doing ordinary work, and there is no point defining nouns that generic.
  A term earns an entry by being load-bearing, not by appearing. Full standard:
  [`dev/standards/terminology.md`](../dev/standards/terminology.md).
- **Reviews are permanent, which is not the same as published.** `reviews/` is tracked, never
  gitignored, one directory per run named `<YYYY-MM-DD>-<milestone>`, and never deleted or pruned on
  triage — it is the evidence behind what `this.i` decided, not a worklist. Open findings become
  **ticks**; a synthesis carries a `status:` header line naming what is still open. A repo that goes
  **public** moves its tree to the private `bakobo/reviews` and purges it from history in the same
  change — a security review is a map of a running system's weak points, and untracking at the tip
  leaves it one `git log` away. Full standard:
  [`dev/standards/reviews.md`](../dev/standards/reviews.md).
- **Going public is a checklist, not a toggle.** If this repo is public — or you are about to make it
  one — it owes a posture: `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md` and `CODE_OF_CONDUCT.md`
  (copy from `bakobo/template`'s `oss-*` files and drop the prefix), private vulnerability reporting,
  Dependabot, secret scanning **with push protection**, CodeQL, a default-branch ruleset requiring a
  PR, the `reviews/` tree moved to the private `bakobo/reviews` **and purged from history**, and a
  dependency closure a stranger can resolve with no credential. GitHub announces none of this when
  visibility flips, so assume it was missed and check. Full standard:
  [`dev/standards/oss-posture.md`](../dev/standards/oss-posture.md); audit with `dev/oss-posture`.
- **Input is bounded before it is trusted.** Size, then shape, then meaning — each only
  trustworthy if the one before it ran. Nothing crosses a boundary unbounded, every input kind
  enters through a named door, and the set of doors is kept complete by a test rather than by
  memory. Full standard: [`dev/standards/input-handling.md`](../dev/standards/input-handling.md).
- **Tasks and tech debt in `tick`** — see the tick stanza below, not an external tracker.
- **Craftsman working posture.** Development follows the `cc` craftsman methodology — interview at
  intent level, dispatch briefs to worker sub-agents, verify against oracles, and learn from every
  failure. It is Daniel Hardman's personal craft (the private `cc` repo), adopted across Bakobo; the
  operational rules for *this* repo are in [`dev/methodology.md`](../dev/methodology.md).

<!-- <<< bakobo standards <<< -->
## Intent methodology

Bakobo develops intent-first. If this repo has design decisions worth explaining, its source of
truth is `this.i` (the intent tree) at the repository root — code and `docs/` are derived from it.
Record each consequential decision in `this.i` **first**, in its own commit, **before** the code
commit it justifies. The full rules — what `this.i` is, when a repo needs one, the speculative
interview, the `why` rebuttal-surface standard, the gate ceremony, and adversarial review — are in
[`dev/methodology.md`](../dev/methodology.md), in the sibling `bakobo/dev` repo. Read it before
making design decisions here.

If this repo has no `this.i` yet and warrants one, see [`dev/methodology.md`](../dev/methodology.md)
§2 and the shipped `this.i.seed`. A trivial repo (pure content/assets/config, where no one will
later need to know *why*) may skip intent entirely — just delete `this.i.seed`.

## This is a content repo

The product is the corpus and the registry, not software. `tools/` is a thin harvesting layer over
[`id-law-kit`](../id-law-kit), which is where the real code and its test suite live — add
behaviour there, with tests, not here.

```sh
python3 -m venv .venv && .venv/bin/pip install -e ../id-law-kit
.venv/bin/python tools/harvest-statute.py --download   # ~1.1 GB snapshot, then filter
.venv/bin/python tools/harvest-regs.py                # the two rulemaking PDFs
```

`harvest-regs.py` needs **poppler-utils** (`pdftotext`) on PATH.

There is no CI beyond the template's review gate, and that is deliberate: nothing here builds, and
a workflow that refetched a 1.1 GB snapshot on every push would prove nothing the manifest does
not already prove.

## Working rules for this repo

1. **Quote-or-drop.** Every claim about EU law needs a citation *and* a verbatim quote retrievable
   from `corpus/` via `lawcite`. If the quote cannot be reproduced, delete the claim — do not
   soften it. Models fabricate legal citations fluently; the corpus is what makes a citation
   checkable rather than trusted.
2. **Scope is the CCPA/CPRA only** — Civil Code Title 1.81.5. The Information Practices Act,
   CalOPPA, and the Delete Act share the 1798 prefix and are different statutes. `CCPA_SECTION` in
   the harvester is the boundary.
3. **Match section numbers as strings, never numerically.** `1798.1` and `1798.100` both parse as
   the float `1798.1`. A numeric filter silently swallows a statute from 1977.
4. **Counts are pointers to read, never findings.** A sweep tells you where to look. `utah-id-law`
   published a false "zero requirements" claim from a count, and the pattern that produced it
   matched nothing at all.
5. **Say which layer a claim rests on.** Enacting terms, recital, implementing decision, and
   judgment are different things. A recital is not binding in the way an article is, and the
   corpus keeps them distinct so a finding can say which it used.
6. **Both layers are here — use both.** `corpus/` is the statute, `corpus-regs/` the regulations.
   `utah-id-law` twice reached a wrong answer from statute alone. Check both before concluding.
7. **Sweep the regulations with `--in-force-only` unless you mean otherwise.** `corpus-regs/` holds
   30 superseded 2023 wordings alongside the current text, so an unfiltered count mixes law with
   former law.
8. **The OAL Notice of Approval is the oracle for what changed.** `tools/regs_sources.py` carries
   the adopted/amended/repealed lists transcribed from it, and `harvest-regs.py` aborts if the PDF
   stops matching. Do not relax that check to make a harvest succeed — a partial chapter that looks
   complete is worse than a failed run.

<!-- >>> tick stanza >>> (managed by `tick init`) -->

## Task tracking: `tick`

This repo tracks tasks, tech debt, and ideas in a local [`tick`](https://github.com/dhh1128/tick)
ledger (an orphan `tick` branch; the `tick` CLI is the interface). Reads are plain
files — do **not** use an external API for task tracking.

- **First, if a `tick` command says the repo isn't initialized**, run `tick init`
  once to connect this clone to the ledger — it adopts the existing remote ledger
  if a colleague already set one up, or creates a new one otherwise.
- **A tick mark is the sigil `~` immediately followed by a digit-first 4-char
  base32 id** (the id part looks like `4mz3`, so the full mark is that id with a
  leading `~`). It pins a tick to a code location.
- **Before editing a file**, grep it for marks and read what they reference:
  `rg '~[2-7][a-z2-7]{3}\b' <file>` then `tick show <id>`. A mark means recorded
  context exists for that spot — read it first.
- **Search** existing ticks with `tick grep <text>`; **list** with `tick ls`.
- **Capture** new work with `tick add "<title>"` and place the printed mark
  (`~` + the new id) at the relevant code spot.
- When your change **resolves** a tick, run `tick off <id>` and **delete the
  mark(s)** it reports still in the code.

<!-- <<< tick stanza <<< -->
