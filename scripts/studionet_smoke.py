"""Deploy and exercise the current router source on hosted StudioNet.

Set GENLAYER_PRIVATE_KEY to an unlocked StudioNet account key. The script waits
for finalized execution at every step and replaces deployments/studionet.json
only after it has a readable final state.
"""

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import time

from eth_account import Account
from genlayer_py import create_client
from genlayer_py.chains import studionet
from genlayer_py.provider import provider as provider_module
from genlayer_py.types import TransactionStatus


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "ConditionalMarketRouter.py"
MANIFEST = ROOT / "deployments" / "studionet.json"
RUNNER = "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"


provider_module.requests.post = (
    lambda original: lambda *args, **kwargs: original(*args, timeout=(10, 45), **kwargs)
)(provider_module.requests.post)


def _wait_finalized(client, transaction_hash: str, label: str) -> dict:
    for attempt in range(12):
        try:
            return client.wait_for_transaction_receipt(
                transaction_hash=transaction_hash,
                status=TransactionStatus.FINALIZED,
                interval=5000,
                retries=60,
            )
        except Exception as exc:
            print(f"{label}: receipt retry {attempt + 1}: {type(exc).__name__}", flush=True)
            time.sleep(4)
    raise RuntimeError(f"{label}: finality unavailable")


def _execution(receipt: dict) -> str:
    leader_receipts = receipt.get("consensus_data", {}).get("leader_receipt") or []
    if not leader_receipts:
        return "MISSING_LEADER_RECEIPT"
    return str(leader_receipts[0].get("execution_result", "UNKNOWN"))


def _assert_success(receipt: dict, label: str) -> None:
    execution = _execution(receipt)
    if execution not in ("SUCCESS", "FINISHED_WITH_RETURN"):
        raise RuntimeError(f"{label} execution failed: {execution}")


def _wait_until(deadline: datetime) -> None:
    while True:
        remaining = (deadline - datetime.now(timezone.utc)).total_seconds()
        if remaining <= 0:
            return
        time.sleep(min(5, remaining))


def _git_commit() -> str:
    return subprocess.run(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    private_key = os.environ.get("GENLAYER_PRIVATE_KEY", "").strip()
    if not private_key:
        raise RuntimeError("GENLAYER_PRIVATE_KEY is required")

    account = Account.from_key(private_key)
    client = create_client(
        chain=studionet,
        account=account,
        endpoint=studionet.rpc_urls["default"]["http"][0],
    )

    now = datetime.now(timezone.utc)
    trigger_deadline = now + timedelta(seconds=45)
    outcome_deadline = now + timedelta(seconds=90)
    source_url = "https://www.iana.org/help/example-domains"
    constructor_args = [
        "iana-example-domains-conditional-smoke",
        json.dumps({"question": "Does IANA state that example domains are reserved for documentation?"}),
        json.dumps({"question": "Does IANA identify example.com as an example domain?"}),
        json.dumps([source_url]),
        json.dumps([source_url]),
        trigger_deadline.isoformat(),
        outcome_deadline.isoformat(),
    ]

    source_commit = _git_commit()
    code = CONTRACT.read_text(encoding="utf-8")
    deploy_hash = client.deploy_contract(code=code, args=constructor_args, leader_only=False)
    print(f"deployment submitted: {deploy_hash}", flush=True)
    deploy_receipt = _wait_finalized(client, deploy_hash, "deployment")
    _assert_success(deploy_receipt, "deployment")
    address = deploy_receipt.get("data", {}).get("contract_address")
    if not address:
        raise RuntimeError("deployment finalized without a contract address")
    print(f"deployment finalized: {address}", flush=True)

    _wait_until(trigger_deadline)
    trigger_hash = client.write_contract(
        address=address,
        function_name="resolve_trigger",
        args=[],
        leader_only=False,
    )
    print(f"trigger submitted: {trigger_hash}", flush=True)
    trigger_receipt = _wait_finalized(client, trigger_hash, "trigger")
    _assert_success(trigger_receipt, "trigger")
    state = client.read_contract(address=address, function_name="get_state", args=[])

    outcome_hash = None
    outcome_receipt = None
    if state.get("status") == "TRIGGER_CONFIRMED":
        _wait_until(outcome_deadline)
        outcome_hash = client.write_contract(
            address=address,
            function_name="resolve_outcome",
            args=[],
            leader_only=False,
        )
        print(f"outcome submitted: {outcome_hash}", flush=True)
        outcome_receipt = _wait_finalized(client, outcome_hash, "outcome")
        _assert_success(outcome_receipt, "outcome")
        state = client.read_contract(address=address, function_name="get_state", args=[])

    manifest = {
        "contract": "ConditionalMarketRouter",
        "source_commit": source_commit,
        "historical_pre_hardening_deployment": False,
        "network": "studionet",
        "chain_id": studionet.id,
        "deployer": account.address,
        "contract_address": address,
        "deployment_transaction": deploy_hash,
        "explorer_url": f"https://explorer-studio.genlayer.com/address/{address}",
        "runner": RUNNER,
        "constructor_args": constructor_args,
        "deployment_status": str(deploy_receipt.get("status_name", deploy_receipt.get("status"))),
        "deployment_execution": _execution(deploy_receipt),
        "trigger_transaction": trigger_hash,
        "trigger_status": str(trigger_receipt.get("status_name", trigger_receipt.get("status"))),
        "trigger_execution": _execution(trigger_receipt),
        "outcome_transaction": outcome_hash,
        "outcome_status": None if outcome_receipt is None else str(outcome_receipt.get("status_name", outcome_receipt.get("status"))),
        "outcome_execution": None if outcome_receipt is None else _execution(outcome_receipt),
        "state": state,
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str), flush=True)


if __name__ == "__main__":
    main()
