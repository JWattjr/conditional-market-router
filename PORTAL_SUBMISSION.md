# GenLayer Portal submission draft

**Contribution type:** Builder → Intelligent Contracts  
**Title:** Conditional Market Router  
**Draft updated:** September 3, 2026

## Notes / Description

Conditional Market Router is an MIT-licensed, standalone GenLayer primitive for
“if X happens, will Y happen?” prediction markets. The constructor freezes
separate trigger and outcome questions, unique public evidence sets, and ordered
timezone-aware deadlines. Consensus first routes the lifecycle to
`TRIGGER_CONFIRMED`, `VOID`, or `TRIGGER_UNRESOLVED`; only a confirmed trigger
can later settle `YES`, `NO`, or `OUTCOME_UNRESOLVED`.

For both stages, the leader and validators independently fetch bounded evidence,
derive a canonical decision, and compare every returned field. Non-200 responses
and request exceptions are treated as unavailable evidence, while an all-source
outage fails closed to a retryable `UNRESOLVED` state. The contract rejects
non-public IP literals and malformed source hosts, stores an explicit `VOID`
outcome for false triggers, and makes terminal transitions replay-safe. It holds
no funds and is intended to compose with a finality-aware payout wrapper.

The repository includes a pinned GenVM runner/toolchain, 26 direct tests, a
router-specific security audit and test matrix, and deployment manifests.

## Verification status

- Repository is public and the reviewed source is on `main`.
- Hardened source commit: `cefc42751267706b506afab65e4d6bfadca0eb9e`.
- StudioNet deployment, trigger, and outcome finalized with successful
  execution.
- Both stages reached `MAJORITY_AGREE` with 3 agree / 2 idle.
- Final state: trigger `TRUE`, status `SETTLED`, outcome `YES`, attempts 2.

## Evidence links

1. Repository — https://github.com/JWattjr/conditional-market-router
2. Contract — https://github.com/JWattjr/conditional-market-router/blob/main/contracts/ConditionalMarketRouter.py
3. State-machine tests — https://github.com/JWattjr/conditional-market-router/blob/main/tests/test_router.py
4. Validator-coverage tests — https://github.com/JWattjr/conditional-market-router/blob/main/tests/test_validator_coverage.py
5. Security audit — https://github.com/JWattjr/conditional-market-router/blob/main/docs/SECURITY_AUDIT.md
6. Test matrix — https://github.com/JWattjr/conditional-market-router/blob/main/docs/TEST_MATRIX.md
7. StudioNet manifest — https://github.com/JWattjr/conditional-market-router/blob/main/deployments/studionet.json
8. GenLayer Explorer contract — https://explorer-studio.genlayer.com/address/0xE0731eBA9d51B84782a51F47Bb403a05672325F9

The Bradbury manifest is explicitly marked as historical pre-hardening evidence
and is not presented as a deployment of the current source.
