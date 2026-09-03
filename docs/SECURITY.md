# Threat model and security notes

## Trust boundary

The contract is the authoritative router for two consensus decisions. It does
not custody funds or execute payouts. Anyone may call the resolution methods
after their respective deadlines; the frozen evidence and validator agreement,
not caller identity, determine the result.

## Threats addressed

- **Malicious leader:** validators independently fetch the same frozen evidence,
  rerun the evaluation, and compare both `stage` and `decision` exactly.
- **Source outage:** non-200 responses and request exceptions are marked
  unavailable. An all-source outage returns `UNRESOLVED` without invoking an
  LLM, leaving the stage retryable.
- **Direct private-address input:** URLs require public HTTPS hosts. Non-public
  IPv4 and IPv6 literals, IPv4-mapped private addresses, multicast addresses,
  local/internal suffixes, userinfo, malformed hostnames, and non-default ports
  are rejected.
- **Prompt injection:** source text is labeled as evidence, bounded before it
  enters the prompt, and accompanied by an instruction to ignore embedded
  commands. Validators independently repeat the task.
- **Premature or out-of-order resolution:** explicit UTC-normalized deadlines
  and lifecycle gates control each transition.
- **Replay:** terminal calls return current state without another consensus run
  or attempt increment.
- **Unbounded inputs:** market IDs, questions, canonical specs, source counts,
  URL lengths, and per-source response bodies are capped.

## Residual risks

- DNS names can resolve differently or rebind after constructor validation.
  Production deployments should use an explicit reviewed-domain allowlist.
- HTTPS proves transport security, not that a source is authoritative or true.
- Public evidence and LLM judgments can drift between validators, causing
  disagreement or a retryable unresolved state.
- `UNRESOLVED` stages have no expiry and may be retried indefinitely. A payout
  adapter should define its own maximum-wait and refund policy.
- Prompt-injection resistance is defense in depth, not a formal guarantee.
- Trigger and outcome are separate consensus transactions. Integrators must
  wait for finality after both consequential transitions.

## Operational requirements

Use stable, source-specific URLs from reviewed domains. Prefer immutable
reports, official records, or signed attestations. A payout wrapper must consume
only finalized terminal state and make its claims idempotent.
