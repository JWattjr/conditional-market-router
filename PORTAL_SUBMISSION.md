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

## Required before submission

1. Make `https://github.com/JWattjr/conditional-market-router` publicly
   accessible and confirm every file link below works while signed out.
2. Commit and push the hardened source, tests, and documentation.
3. Redeploy the hardened commit and execute both ordered consensus stages on a
   hosted GenLayer network.
4. Replace the deployment placeholders below and update the manifests with the
   new source commit, addresses, transaction hashes, finality, and validator
   results.

## Evidence links

1. Repository — https://github.com/JWattjr/conditional-market-router
2. Contract — https://github.com/JWattjr/conditional-market-router/blob/main/contracts/ConditionalMarketRouter.py
3. State-machine tests — https://github.com/JWattjr/conditional-market-router/blob/main/tests/test_router.py
4. Validator-coverage tests — https://github.com/JWattjr/conditional-market-router/blob/main/tests/test_validator_coverage.py
5. Security audit — https://github.com/JWattjr/conditional-market-router/blob/main/docs/SECURITY_AUDIT.md
6. Test matrix — https://github.com/JWattjr/conditional-market-router/blob/main/docs/TEST_MATRIX.md
7. Hosted-network manifest — REPLACE_WITH_CURRENT_MANIFEST_URL
8. GenLayer Explorer contract — REPLACE_WITH_CURRENT_EXPLORER_URL

The existing `deployments/studionet.json` and `deployments/bradbury.json` files
are explicitly marked as historical pre-hardening evidence and are not evidence
for the current source.
