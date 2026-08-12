# Security and consensus audit: ConditionalMarketRouter

Audit date: 2026-08-12
Scope: `contracts/ConditionalMarketRouter.py`
Method: manual review, GenVM AST lint, SDK schema validation, direct-mode
state-machine tests, and hosted-network receipt inspection.

## Result

No unresolved critical or high-severity issue was found after remediation.
The router records a two-stage judgment and contains no funds or payout code.

## Remediated findings

| ID | Severity | Finding | Remediation |
| --- | --- | --- | --- |
| CR-01 | Medium | An unavailable evidence set could reach the LLM. | Derive stage `UNRESOLVED` before prompting when every source is unavailable. |
| CR-02 | Medium | Public URL checks allowed private/internal targets. | Enforce bounded public HTTPS hosts and reject private literals, internal suffixes, userinfo, and non-default ports. |
| CR-03 | Medium | Consensus closures could capture storage-backed stage inputs. | Snapshot the selected spec and URL list before nondeterministic execution; closures contain no `self`. |
| CR-04 | Medium | Stage validation needed a narrowly consequential equivalence rule. | Validators independently recompute and compare only the frozen stage and normalized decision. |
| CR-05 | Low | A false trigger did not expose an explicit terminal market outcome. | Store terminal `VOID` when the trigger is `FALSE`. |
| CR-06 | Low | Decoded JSON, malformed bytes, and loose return wrappers needed hardening. | Canonicalize inputs, safely decode bounded bytes, and require `gl.vm.Return`. |

## Residual risks

- A confirmed trigger and outcome are separate consensus transactions; callers
  must respect both deadlines and finality states.
- Source drift can produce validator disagreement and leave a stage unresolved.
- Evidence authority is a deployment-policy decision, not established by HTTPS.
- DNS rebinding requires reviewed domains or an explicit allowlist.

## Verification evidence

- Pinned GenVM runner; GenVM lint and SDK validation pass.
- Standalone direct suite: 3 passed, covering the positive two-stage route,
  false-trigger `VOID`, and storage isolation.
- Both StudioNet stage transactions finalized with `SUCCESS`, 3 agree / 2 idle,
  and no storage warning.
- Live final state: trigger `TRUE`, status `SETTLED`, outcome `YES`, attempts 2.
- Bradbury status is tracked independently in its deployment manifest.

This is an engineering assessment, not formal verification or a financial or
legal guarantee.
