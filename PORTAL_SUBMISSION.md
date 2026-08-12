# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts  
**Title:** Conditional Market Router  
**Contribution date:** Use the actual date of the submitted release.

## Notes / Description

Built and deployed an MIT-licensed Conditional Market Router, a standalone
GenLayer primitive for “if X happens, will Y happen?” prediction markets. The
constructor freezes separate trigger/outcome questions, public evidence sets,
and ordered deadlines. Consensus first routes the lifecycle to
TRIGGER_CONFIRMED, VOID, or TRIGGER_UNRESOLVED; only a confirmed trigger can
later settle YES, NO, or OUTCOME_UNRESOLVED. For both stages, the leader and
validators independently fetch evidence and compare the stage plus canonical
decision through a custom equivalence function. All-source outages fail closed,
false triggers store an explicit VOID outcome, and terminal transitions are
replay-safe. Includes pinned GenVM source, validator tests, security audit, test
matrix, and StudioNet/Bradbury deployment records. It is composable with a
finality-aware payout wrapper but holds no funds itself.

## Evidence to add

1. GitHub Repository — replace with the private repository URL.
2. GitHub File — `contracts/ConditionalMarketRouter.py`.
3. GitHub File — `tests/test_router.py`.
4. GitHub File — `docs/SECURITY_AUDIT.md`.
5. GitHub File — `docs/TEST_MATRIX.md`.
6. GitHub File — `deployments/studionet.json`.
7. GitHub File — `deployments/bradbury.json`.
8. GenLayer Explorer Contract — replace with the finalized Bradbury address URL.
