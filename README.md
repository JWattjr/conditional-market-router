# Conditional Market Router

A two-stage GenLayer primitive for “if X happens, will Y happen?” prediction
markets.

The contract freezes separate trigger and outcome questions, public evidence
sets, and ordered deadlines. After the trigger deadline, consensus routes the
market to `TRIGGER_CONFIRMED`, `VOID`, or `TRIGGER_UNRESOLVED`. Only a confirmed
trigger can later settle to `YES`, `NO`, or `OUTCOME_UNRESOLVED` after the
outcome deadline.

## Consensus boundary

The frontend or market operator owns market creation, display, indexing, and
any payout adapter. The contract owns the immutable resolution inputs, deadline
checks, independent validator evaluation, and the final routing state. External
sources provide evidence but are not trusted merely because they use HTTPS.

For each stage, the leader and validators independently fetch the frozen source
set, ask for one canonical `TRUE`, `FALSE`, or `UNRESOLVED` decision, and compare
both returned fields (`stage` and `decision`). Storage is updated only after
consensus.

## Safety properties

- All inputs are bounded; source URLs must be unique public HTTPS endpoints.
- Non-public IPv4/IPv6 literals, malformed hostnames, userinfo, and non-default
  ports are rejected.
- HTTP failures and request exceptions are represented as unavailable evidence.
  If every source is unavailable, the stage returns `UNRESOLVED` without an LLM
  call and remains retryable.
- Deadlines require explicit timezone offsets and are normalized to UTC.
- Terminal transitions are replay-safe and do not increment `attempts` again.
- The contract holds no funds. Payout integrations must wait for finality and
  make claims idempotent.

## Verify

The pinned runner is contained in the GenVM `v0.3.0-rc7` bundle. From a virtual
environment:

```powershell
python -m pip install -r requirements.txt
$env:GENVM_VERSION = "v0.3.0-rc7"
genvm-lint check contracts/ConditionalMarketRouter.py --json
python -m pytest tests -v
```

The current direct suite contains 26 tests. See `docs/TEST_MATRIX.md` and
`docs/SECURITY_AUDIT.md` for the exact coverage and residual risks.

## Deployment evidence

- [Current StudioNet deployment](https://explorer-studio.genlayer.com/address/0xE0731eBA9d51B84782a51F47Bb403a05672325F9)
  executes public source commit `cefc42751267706b506afab65e4d6bfadca0eb9e`.
  Deployment, trigger, and outcome all finalized with successful execution;
  the final state is `SETTLED / YES` with two attempts.
- `deployments/studionet.json` records the current transaction hashes, exact
  constructor arguments, validator results, and final state.
- `deployments/bradbury.json` remains explicitly marked as historical
  pre-hardening evidence and is not presented as a deployment of current code.

After committing the exact source to deploy, an operator can reproduce this with
`python scripts/studionet_smoke.py` with `GENLAYER_PRIVATE_KEY` set. The script
waits for finalized execution and writes a source-linked StudioNet manifest.
