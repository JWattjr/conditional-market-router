# Test matrix

| Requirement | Direct verification | Hosted-network evidence |
| --- | --- | --- |
| Constructor validation | Empty market ID/question, malformed JSON, empty sources, duplicate URLs, oversized specs, naive/unordered deadlines | Redeployment pending |
| URL safety | HTTP, localhost, private IPv4, internal suffixes, IPv6 loopback, IPv4-mapped loopback, multicast, malformed hostnames | Redeployment pending |
| Deadline enforcement | Trigger and outcome reject early resolution | Historical deployments exercised ordered stages |
| Stage ordering | Outcome cannot resolve while the trigger is open | Historical deployments exercised trigger then outcome |
| Positive two-stage route | Trigger `TRUE`, outcome `FALSE`, final `SETTLED / NO` | Historical manifests record `SETTLED / YES` |
| False trigger | Stores terminal `VOID` outcome | Not separately exercised live |
| Unavailable evidence | HTTP 503 and request exception both produce retryable `TRIGGER_UNRESOLVED` | Redeployment pending |
| Retry behavior | An unresolved trigger can later become `TRIGGER_CONFIRMED` | Not separately exercised live |
| Replay/idempotency | Repeating terminal trigger resolution preserves state and attempt count | Historical stages finalized once each |
| Malicious leader | Validator rejects altered trigger and outcome decisions | Historical manifests record validator agreement |
| Validator coverage | AST test requires every returned consensus field to be compared with zero tolerance | Historical receipts report no storage warning |
| Storage isolation | AST test rejects `self` capture in leader/validator closures | Historical receipts report no storage warning |

## Current local result — 2026-09-03

- `genvm-lint check`: passed against `GENVM_VERSION=v0.3.0-rc7` with three AST
  checks and SDK schema validation.
- Standalone direct suite: 26 passed.
- Runner: pinned `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.

## Evidence status

The existing StudioNet and Bradbury receipts were produced by source commit
`8efa41d419ca5422c174a37d65efc2a15b1aaf47`, before the 2026-09-03 URL and
request-failure hardening. New deployments and ordered consensus transactions
are required before those manifests can be presented as evidence for the
current source.
