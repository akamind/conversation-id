# Conversation-ID

Source and review material for **The Conversation-ID Email Header Field**,
an individual Internet-Draft by Juliano Primavesi, Akamind Inc.

**Intended status: Experimental.** The proposal is a work in progress. It has
not been adopted by an IETF working group or published as an RFC.

## The proposal

`Conversation-ID` carries a UUIDv4 URN that participating originators can reuse
across messages in a conversation:

```text
Conversation-ID: urn:uuid:550e8400-e29b-41d4-a716-446655440000
```

It complements `Message-ID`, `In-Reply-To`, and `References`. The experiment
asks whether an explicit conversation identifier improves correlation across
independently operated applications, including delivery paths that rewrite
`Message-ID`, compared with correctly constructed reply fields and available
provider identifier mappings.

Matching identifiers alone are insufficient for grouping. The field grants
no authorization. Preserving a field in transit and copying it into a newly
composed reply require separate support; existing clients are not assumed to
propagate it. The draft defines the complete processing and trust rules.

## Published draft

- [Datatracker: status and revision history](https://datatracker.ietf.org/doc/draft-primavesi-conversation-id/)
- [Revision -00: formatted text](https://www.ietf.org/archive/id/draft-primavesi-conversation-id-00.txt)
- [Revision -00: XML source](https://www.ietf.org/archive/id/draft-primavesi-conversation-id-00.xml)

The XML and TXT in the [`draft-00` tag](https://github.com/akaMind/conversation-id/tree/draft-00) are byte-for-byte copies
of revision `-00`, published on 10 October 2026. Their source URLs and SHA-256
hashes are recorded in [publication.json](publication.json). XML is the editable
source; TXT is its published rendering. See [CONTRIBUTING.md](CONTRIBUTING.md)
for revision handling.

The author plans to evaluate the proposal in [Oveyon](https://oveyon.com/), an
email service operated by [Akamind](https://akamind.net/). Revision `-00` reports
no implementation or interoperability results.

## Repository contents

| Path | Purpose |
| --- | --- |
| `draft-primavesi-conversation-id-00.xml` | Published RFCXML source |
| `draft-primavesi-conversation-id-00.txt` | Published text, including pagination |
| `examples/` | Four synthetic email fixtures and an explanation of each case |
| `validate_syntax.py` | Local ABNF, field cardinality, and normalization checks |
| `validation/syntax-vectors.json` | 60 test vectors with explicit expected results |
| `requirements-validation.txt` | Pinned dependencies for checking and rendering |
| `publication.json` | Provenance and hashes of the published revision |

## Run the checks

Use Python 3.11 or later. From the repository directory, create a virtual
environment and run:

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-validation.txt
python validate_syntax.py
```

The script reads the ABNF from the XML and runs the versioned JSON vectors.
It writes `build/syntax-results.json`, including the UTC run time and the hash
of the XML tested. The process exits with a nonzero status if a check fails.
An optional positional argument selects another XML file; `--output` selects
the report path. Run `python validate_syntax.py --help` for details.

These checks cover syntax, duplicate fields, case normalization, and selected
XML structure checks. In a vector, `null` means that no identifier is available
for correlation; it does not mean that delivery should be rejected. The checks
do not exercise the `.eml` fixtures, message transport, reply propagation,
DKIM, UUID generation, grouping policy, or authorization.

To render the XML locally after running the checks:

```sh
xml2rfc draft-primavesi-conversation-id-00.xml --text --out build/draft-00.txt
xml2rfc draft-primavesi-conversation-id-00.xml --html --out build/draft-00.html
```

Local build output is ignored by Git. The published TXT remains the reference
copy for revision `-00`.

## Feedback and participation

[Issues](https://github.com/akaMind/conversation-id/issues) and
[pull requests](https://github.com/akaMind/conversation-id/pulls) are welcome. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) and the
[IETF Note Well](https://www.ietf.org/about/note-well/) before contributing.
The document's copyright notice refers to the
[IETF Trust Legal Provisions](https://trustee.ietf.org/documents/trust-legal-provisions/).

The author welcomes technical feedback on the
[MAILMAINT mailing list](https://datatracker.ietf.org/group/mailmaint/about/)
at <mailmaint@ietf.org>, and contact from implementers interested in an
independent interoperability experiment. The
[list archive](https://mailarchive.ietf.org/arch/browse/mailmaint/) is public.

**Author:** Juliano Primavesi, Akamind Inc.

**Contact:** <jprimavesi@akamind.net>
