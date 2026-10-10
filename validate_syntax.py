#!/usr/bin/env python3
"""Check the draft's ABNF against the committed Conversation-ID vectors.

This checks syntax, cardinality, normalized-value comparison, and local XML
consistency. It does not read the .eml examples or test UUID randomness, DKIM,
authorization, conversation grouping, or interoperability. It is not a full
RFCXML schema validator or a mail implementation. Author metadata is reported
separately and does not affect the protocol checks.

The source and vector files are read only. Results go to build/ by default.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

from abnf import ParseError, Rule
from abnf.grammars.rfc5322 import Rule as MailRule
from lxml import etree


ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE = ROOT / "draft-primavesi-conversation-id-00.xml"
VECTORS = ROOT / "validation" / "syntax-vectors.json"
DEFAULT_OUTPUT = ROOT / "build" / "syntax-results.json"
CANONICAL = "urn:uuid:550e8400-e29b-41d4-a716-446655440000"


def read_vectors(data):
    vectors = json.loads(data)
    if not isinstance(vectors, list) or not vectors:
        raise ValueError("The vector file must contain a nonempty JSON array.")
    names = set()
    for vector in vectors:
        if not isinstance(vector, dict) or not {"name", "fields", "expected"} <= vector.keys():
            raise ValueError("Each vector must have name, fields, and expected entries.")
        name = vector["name"]
        fields = vector["fields"]
        expected = vector["expected"]
        if not isinstance(name, str) or not name or name in names:
            raise ValueError("Vector names must be nonempty, unique strings.")
        if not isinstance(fields, list) or not all(isinstance(value, str) for value in fields):
            raise ValueError(f"Vector {name!r}: fields must be an array of strings.")
        if expected is not None and not isinstance(expected, str):
            raise ValueError(f"Vector {name!r}: expected must be a string or null.")
        names.add(name)
    return vectors


def load_field_rule(doc):
    grammars = [
        "".join(block.itertext()).strip() + "\n"
        for block in doc.xpath('//sourcecode[@type="abnf"]')
        if re.search(r"(?m)^\s*conversation-id\s*=", "".join(block.itertext()))
    ]
    if len(grammars) != 1:
        raise ValueError("Expected one ABNF sourcecode block defining conversation-id.")

    class ConversationRule(Rule):
        pass

    ConversationRule("FWS", MailRule("FWS").definition)
    ConversationRule.load_grammar(grammars[0])
    return ConversationRule("conversation-id")


def correlation_value(fields, field_rule):
    # A null result means unusable for correlation, not rejected delivery.
    cid_fields = [
        value for value in fields
        if value.partition(":")[0].lower() == "conversation-id"
    ]
    if len(cid_fields) != 1:
        return None
    raw = cid_fields[0]
    try:
        field_rule.parse_all(raw)
    except ParseError:
        return None
    body = raw.split(":", 1)[1][:-2]
    unfolded = re.sub(r"\r\n(?=[ \t])", "", body)
    return unfolded.strip(" \t").lower()


def check(source, output):
    if output.resolve() in {source.resolve(), VECTORS.resolve()}:
        raise ValueError("The output file must not overwrite the XML or vector input.")
    source_bytes = source.read_bytes()
    vector_bytes = VECTORS.read_bytes()
    doc = etree.fromstring(
        source_bytes, parser=etree.XMLParser(resolve_entities=False, no_network=True)
    )
    vectors = read_vectors(vector_bytes)
    field_rule = load_field_rule(doc)

    failures = []
    for vector in vectors:
        actual = correlation_value(vector["fields"], field_rule)
        if actual != vector["expected"]:
            failures.append({
                "name": vector["name"],
                "expected": vector["expected"],
                "actual": actual,
            })

    token_octets = len(CANONICAL.encode("ascii"))
    field_octets = len(("Conversation-ID: " + CANONICAL + "\r\n").encode("ascii"))
    anchors = doc.xpath("//@anchor")
    missing_targets = sorted(set(doc.xpath("//xref/@target")) - set(anchors))
    local_checks = {
        "canonical_token_is_45_octets": token_octets == 45,
        "canonical_field_is_64_octets_including_crlf": field_octets == 64,
        "unique_xml_anchors": len(anchors) == len(set(anchors)),
        "resolved_internal_references": not missing_targets,
        "no_xinclude": not doc.xpath(
            "//xi:include", namespaces={"xi": "http://www.w3.org/2001/XInclude"}
        ),
    }
    email = doc.findtext("front/author/address/email")
    organization = doc.findtext("front/author/organization")
    now = datetime.now(timezone.utc)
    result = {
        "result": "pass" if not failures and all(local_checks.values()) else "fail",
        "date": now.date().isoformat(),
        "checked_at_utc": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": {
            "file": source.name,
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
        },
        "vectors": {
            "file": "validation/syntax-vectors.json",
            "sha256": hashlib.sha256(vector_bytes).hexdigest(),
            "count": len(vectors),
        },
        "scope": "ABNF, syntax/cardinality/normalized-value vectors, and local XML consistency only.",
        "passed": len(vectors) - len(failures),
        "failed": len(failures),
        "failures": failures,
        "token_octets": token_octets,
        "canonical_field_octets_including_crlf": field_octets,
        "local_checks": local_checks,
        "unresolved_internal_references": missing_targets,
        "editorial_metadata": {
            "scope": "Project contact information; not protocol conformance.",
            "affects_test_result": False,
            "first_author_email": email,
            "first_author_organization": organization,
            "matches_project_email": email == "jprimavesi@akamind.net",
            "matches_project_organization": organization == "Akamind Inc.",
        },
        "cross_system_interoperability_tested": False,
        "live_messages_sent": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source", nargs="?", type=Path, default=DEFAULT_SOURCE,
        help="RFCXML source (default: draft-primavesi-conversation-id-00.xml beside this script)",
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="result JSON path (default: build/syntax-results.json beside this script)",
    )
    args = parser.parse_args()
    try:
        result = check(args.source, args.output)
    except (OSError, ValueError, etree.XMLSyntaxError, ParseError) as error:
        print(f"Validation could not run: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
