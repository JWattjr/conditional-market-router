# Conditional Market Router

A two-stage GenLayer primitive for “if X happens, will Y happen?” prediction
markets.

The contract freezes separate trigger and outcome questions, evidence sets, and
deadlines. Consensus first routes the market to `TRIGGER_CONFIRMED`, `VOID`, or
`TRIGGER_UNRESOLVED`. Only a confirmed trigger can later resolve to `YES`, `NO`,
or `OUTCOME_UNRESOLVED`. This prevents a centralized backend from deciding
whether a conditional market should exist or settle.

## GenLayer-native decision

Each stage uses independent public-evidence evaluation and a custom validator
that compares the stage and canonical decision. Lifecycle routing is then
deterministic and idempotent.

## Lifecycle and API

- Deploy in `OPEN` with ordered trigger/outcome deadlines.
- Call `resolve_trigger()` after the first deadline. `FALSE` terminates as
  `VOID`; `TRUE` advances to `TRIGGER_CONFIRMED`.
- Only then call `resolve_outcome()` after the second deadline to settle
  `YES`, `NO`, or `OUTCOME_UNRESOLVED`.
- Read both stage records with `get_state()` and wait for finality at each
  consequential transition.

## Live evidence

- [StudioNet contract](https://explorer-studio.genlayer.com/address/0x45bb419FE205cA5B3C08417De013158F2F59a6e8)
- [Bradbury contract](https://explorer-bradbury.genlayer.com/address/0xac98350a1E304f9B80f7d3b272e222978a8665a2)
- Exact stage receipts and current finality are recorded in `deployments/`.

## Verify

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/ConditionalMarketRouter.py
pytest tests -v
```

See `docs/SECURITY_AUDIT.md`, `docs/TEST_MATRIX.md`, and
`PORTAL_SUBMISSION.md` for reviewer evidence.
