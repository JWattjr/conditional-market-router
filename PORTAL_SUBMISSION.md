# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts  
**Title:** Conditional Market Router  
**Contribution date:** August 12, 2026

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

1. GitHub Repository — https://github.com/JWattjr/conditional-market-router
2. GitHub File — https://github.com/JWattjr/conditional-market-router/blob/main/contracts/ConditionalMarketRouter.py
3. GitHub File — https://github.com/JWattjr/conditional-market-router/blob/main/tests/test_router.py
4. GitHub File — https://github.com/JWattjr/conditional-market-router/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/conditional-market-router/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/conditional-market-router/blob/main/deployments/studionet.json
7. GitHub File — https://github.com/JWattjr/conditional-market-router/blob/main/deployments/bradbury.json
8. GenLayer Explorer Contract — https://explorer-bradbury.genlayer.com/address/0xac98350a1E304f9B80f7d3b272e222978a8665a2
