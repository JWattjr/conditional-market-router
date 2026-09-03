# Security and consensus audit: ConditionalMarketRouter

Audit updated: 2026-09-03

Scope: `contracts/ConditionalMarketRouter.py`

Method: manual review, GenVM AST lint, SDK schema validation, direct-mode
state-machine tests, and review of historical hosted-network receipts.

## Result

No unresolved critical or high-severity issue was found in the reviewed source.
The router records a two-stage judgment and contains no funds or payout code.
The current source still requires fresh hosted-network deployment evidence
before portal submission.

## Remediated findings

| ID | Severity | Finding | Remediation |
| --- | --- | --- | --- |
| CR-01 | Medium | An unavailable evidence set could reach the LLM. | Return stage `UNRESOLVED` before prompting when every source is unavailable. |
| CR-02 | Medium | URL checks allowed non-public targets, including IPv4-mapped IPv6 and multicast literals. | Require public unicast IP literals and syntactically valid public hostnames; retain DNS rebinding as a documented residual risk. |
| CR-03 | Medium | A thrown web request could abort the claimed fail-closed outage path. | Convert request exceptions and non-200 responses to unavailable evidence. |
| CR-04 | Medium | Consensus closures could capture storage-backed inputs. | Snapshot the selected spec and URL list before nondeterministic execution; closures contain no `self`. |
| CR-05 | Medium | Submission documents claimed tests and APIs belonging to other contracts. | Replace the copied matrix, threat model, and example manifest with router-specific evidence. |
| CR-06 | Medium | The default linter selected a GenVM bundle that did not contain the pinned runner. | Pin Python dependencies and document `GENVM_VERSION=v0.3.0-rc7`, which validates the exact runner. |
| CR-07 | Low | A false trigger did not expose an explicit terminal market outcome. | Store terminal `VOID` when the trigger is `FALSE`. |
| CR-08 | Low | Specs, duplicate sources, naive deadlines, malformed bytes, and loose LLM return wrappers needed hardening. | Bound canonical specs, require unique sources and timezone-aware deadlines, safely decode bounded bytes, normalize decisions, and require `gl.vm.Return`. |

## Verification evidence

- Pinned GenVM runner.
- GenVM lint: 3 AST checks passed.
- SDK validation: passed against the matching `v0.3.0-rc7` GenVM bundle.
- Standalone direct suite: 26 passed.
- Validator tests bind every returned consensus field and reject altered
  decisions.
- Outage tests cover both HTTP failure responses and thrown request failures.
- Historical StudioNet and Bradbury receipts finalized both stages with
  validator agreement and no storage-capture warning.

## Historical deployment limitation

The checked-in hosted-network manifests reference source commit
`8efa41d419ca5422c174a37d65efc2a15b1aaf47`. They predate the current hardening
changes and must not be represented as deployments of the reviewed source.

This is an engineering assessment, not formal verification or a financial or
legal guarantee.
