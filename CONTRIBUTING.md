# Contributing to ccpa

This is a corpus of primary sources, not a software project. What it needs from a contributor is different from what code needs, so this document is short.

**Corrections are the most valuable contribution.** A passage that does not faithfully reproduce its source, a citation that points at the wrong section, a document that has been amended since it was harvested, a source that has moved. Open an issue or a pull request; either is fine.

**A good correction carries its evidence.** Name the authority, quote the passage as it actually reads, and link the official source rather than a summary of it. We cannot act on "this looks wrong" and we would rather not re-do the research to find out. If the official source is a PDF behind a form, say so and quote what you can — that is still useful.

**We are not lawyers and this corpus is not legal advice.** It was assembled by non-lawyers doing textual research with substantial AI assistance, offered without warranty and without any claim of legal gravitas. Corrections to *what a source says* are welcome. Interpretation of what it means is outside what this repository claims to offer.

**Scope.** This repository holds sources and the notes that organise them. The tooling that harvests and cites them lives in [id-law-kit](https://github.com/bakobo/id-law-kit), and corrections to the machinery belong there.

## Sign off your commits

Every commit needs a `Signed-off-by:` trailer:

```sh
git commit -s -m "..."
```

That trailer is the [Developer Certificate of Origin](https://developercertificate.org/) — you are certifying you wrote the change, or have the right to contribute it under this repository's license. It is not a copyright assignment and there is no CLA to sign.

## Using AI to write your contribution

That is fine, and we do it too — say so in the pull request, and be able to defend what you submit. For a corpus the risk is specific and worth naming: a model will produce a plausible citation to a section that does not exist. **Check every quotation and every section number against the actual source before you send it.** A fabricated citation in a corpus of primary sources is the one failure that would make this repository worthless.

## Reporting a problem privately

Use the *Report a vulnerability* button under the **Security** tab, or email `security@bakobo.com`. See `SECURITY.md`.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Report unacceptable behaviour to `conduct@bakobo.com`.

## License

By contributing, you agree your contribution is licensed under this repository's license — see `LICENSE`.
