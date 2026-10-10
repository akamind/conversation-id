# Contributing

This repository supports an individual Internet-Draft. The author uses it to
track proposed changes, reproducible examples, and implementation experience.
Repository changes do not establish IETF consensus or working group adoption.

## IETF contribution notice

This work is intended for contribution to the IETF. Contributions intended
for the draft are subject to the IETF contribution rules described in the
[IETF Note Well](https://www.ietf.org/about/note-well/), including
[BCP 78](https://www.rfc-editor.org/info/bcp78) and
[BCP 79](https://www.rfc-editor.org/info/bcp79). Please read these before
submitting text, examples, issues, or pull requests intended to inform the
specification.

The published document contains its copyright notice and refers to the
[IETF Trust Legal Provisions](https://trustee.ietf.org/documents/trust-legal-provisions/).
Preserve those notices when redistributing the document.

## Raise an issue

Describe the observed problem, identify the draft revision and section, and
give a small example when one helps. Distinguish an editorial correction from
a change to syntax, processing rules, or the experiment.

For substantial protocol questions, the author welcomes discussion on
[MAILMAINT](https://datatracker.ietf.org/group/mailmaint/about/)
(<mailmaint@ietf.org>). Link the issue and the public mailing-list thread so
that participants can follow the reasoning in either place. The author will
bring substantive proposals and outcomes to the list; closing an issue only
records a repository decision.

## Propose an edit

Use a focused pull request. Explain the problem, proposed behavior, and any
compatibility implications. Change the XML source and regenerate local
renderings. Run the validation command documented in the README when the
grammar, vectors, or XML structure changes. Explain changes to expected test
results.

The `draft-00` tag preserves the published `-00` XML and TXT with the initial
review tools and examples. Keep published tags unchanged. When preparing a subsequent
revision, rename the working XML to the next revision and update `docName`,
date, README commands, and the validator's default source together. Git tags
and the IETF archive retain earlier versions. A repository tag is a record
of a revision; it does not submit a document to the IETF.

Keep `publication.json` aligned with files actually published by the IETF.
Do not label working changes as a published revision. Generate working TXT
and HTML under `build/`; do not edit the published TXT by hand.

## Report an experiment

Use synthetic messages or fixtures suitable for public disclosure. Include
the implementation and version at each endpoint, the software that composed
each reply, the transport path, configuration, and test date.

Describe the baseline using conventional reply fields and any available
mapping between original and delivered `Message-ID` values. Record transport
preservation and reply propagation separately. Report correct correlations,
false merges, false splits, and integration effort, including negative results
and cases where the proposed field gives no additional benefit.

Include enough data for another implementer to reproduce the result. Identify
which implementations were developed independently. Checks performed on local
fixtures alone do not establish interoperability between systems. See Section
5 of the draft for the evaluation plan.

## Contact

Juliano Primavesi, Akamind Inc.

<jprimavesi@akamind.net>
