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

## Verify

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/ConditionalMarketRouter.py
pytest tests -v
```

See `docs/SECURITY_AUDIT.md`, `docs/TEST_MATRIX.md`, and
`PORTAL_SUBMISSION.md` for reviewer evidence.
