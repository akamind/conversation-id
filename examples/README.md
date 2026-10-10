# Synthetic message examples

These four `.eml` files illustrate the rewritten `Message-ID` path discussed
in Appendix A of `draft-primavesi-conversation-id-00`. They were constructed
locally and were not sent through a mail service. They contain CRLF line
endings, reserved example addresses, and no DKIM signatures.

| File | Role | Message-ID | Conversation-ID |
| --- | --- | --- | --- |
| `01-origin.eml` | Alice's message before submission | `<m1@example.com>` | Present |
| `02-delivered-rewritten.eml` | The same message after a hypothetical rewrite | `<wire1@example.org>` | Preserved |
| `03-participating-reply.eml` | Bob's reply from a participating client | `<m2@example.net>` | Reused |
| `04-legacy-reply.eml` | Alternative reply from a nonparticipating client | `<m3@example.net>` | Absent |

The third and fourth files are alternative replies to the second file. Both
use the delivered identifier `<wire1@example.org>` in `In-Reply-To` and
`References`; neither replies to the other.

In the participating case, a matching `Conversation-ID` supplies an additional
hint. The receiver still applies the evidence and access-boundary rules in
Sections 3.3 and 6 of the draft.

In the legacy case, conventional reply fields and a trusted local mapping
from `<wire1@example.org>` to `<m1@example.com>` may establish the relationship.
That mapping is application state and is not embedded in these fixtures. If
the available evidence is insufficient, the receiver can leave the reply
ungrouped. Absence of the optional field is not a delivery error and does not
by itself create a new conversation. A later participating response may reuse
an identifier from trusted local state under Section 3.5; this does not add a
field to Bob's stored message.

The UUID is a fixed example. Generate fresh UUIDv4 identifiers with a
cryptographically secure random source for actual new conversations.

`validate_syntax.py` runs the separate JSON vector set. It does not consume
these `.eml` files or simulate the application state, transport, or replies
described here.
