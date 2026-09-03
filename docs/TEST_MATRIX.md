# Test matrix

| Requirement | Direct verification | Hosted-network evidence |
| --- | --- | --- |
| Constructor validation | Empty market ID/question, malformed JSON, empty sources, duplicate URLs, oversized specs, naive/unordered deadlines | Current StudioNet deployment validates accepted constructor inputs |
| URL safety | HTTP, localhost, private IPv4, internal suffixes, IPv6 loopback, IPv4-mapped loopback, multicast, malformed hostnames | Current deployment successfully fetched a public IANA HTTPS source |
| Deadline enforcement | Trigger and outcome reject early resolution | Current StudioNet deployment exercised both ordered deadlines |
| Stage ordering | Outcome cannot resolve while the trigger is open | Current StudioNet deployment exercised trigger then outcome |
| Positive two-stage route | Trigger `TRUE`, outcome `FALSE`, final `SETTLED / NO` | Current StudioNet manifest records `SETTLED / YES` |
| False trigger | Stores terminal `VOID` outcome | Not separately exercised live |
| Unavailable evidence | HTTP 503 and request exception both produce retryable `TRIGGER_UNRESOLVED` | Not separately exercised live |
| Retry behavior | An unresolved trigger can later become `TRIGGER_CONFIRMED` | Not separately exercised live |
| Replay/idempotency | Repeating terminal trigger resolution preserves state and attempt count | Historical stages finalized once each |
| Malicious leader | Validator rejects altered trigger and outcome decisions | Current receipts record majority agreement at both stages |
| Validator coverage | AST test requires every returned consensus field to be compared with zero tolerance | Current receipts record 3 agree / 2 idle at both stages |
| Storage isolation | AST test rejects `self` capture in leader/validator closures | Current receipts contain no storage warning |

## Current local result — 2026-09-03

- `genvm-lint check`: passed against `GENVM_VERSION=v0.3.0-rc7` with three AST
  checks and SDK schema validation.
- Standalone direct suite: 26 passed.
- Runner: pinned `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.

## Current hosted result — 2026-09-03

- Source commit: `cefc42751267706b506afab65e4d6bfadca0eb9e`.
- StudioNet deployment, trigger, and outcome: finalized with successful
  execution.
- Consensus: `MAJORITY_AGREE`, 3 agree / 2 idle at each stage.
- Final state: `SETTLED / YES`, trigger `TRUE`, two attempts.
- The Bradbury manifest remains historical pre-hardening evidence.
