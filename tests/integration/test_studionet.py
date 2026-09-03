import json
import os
from pathlib import Path

import pytest


MANIFEST = Path("deployments/studionet.json")
EXPECTED_COMMIT = "cefc42751267706b506afab65e4d6bfadca0eb9e"
EXPECTED_STATE = {
    "status": "SETTLED",
    "trigger_decision": "TRUE",
    "outcome": "YES",
    "attempts": 2,
}


def test_studionet_manifest_records_current_successful_execution():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["network"] == "studionet"
    assert data["source_commit"] == EXPECTED_COMMIT
    assert data["historical_pre_hardening_deployment"] is False
    assert data["deployment_status"] == "FINALIZED"
    assert data["deployment_execution"] == "SUCCESS"
    assert data["trigger_status"] == "FINALIZED"
    assert data["trigger_execution"] == "SUCCESS"
    assert data["trigger_consensus_result"] == "MAJORITY_AGREE"
    assert data["outcome_status"] == "FINALIZED"
    assert data["outcome_execution"] == "SUCCESS"
    assert data["outcome_consensus_result"] == "MAJORITY_AGREE"
    assert data["contract_address"].startswith("0x")
    assert data["deployment_transaction"].startswith("0x")
    assert data["trigger_transaction"].startswith("0x")
    assert data["outcome_transaction"].startswith("0x")
    for field, value in EXPECTED_STATE.items():
        assert data["state"][field] == value


@pytest.mark.slow
@pytest.mark.skipif(
    os.environ.get("GENLAYER_INTEGRATION") != "1",
    reason="set GENLAYER_INTEGRATION=1 for a live StudioNet read",
)
def test_live_studionet_state_matches_manifest():
    from eth_account import Account
    from genlayer_py import create_client
    from genlayer_py.chains import studionet

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    client = create_client(
        chain=studionet,
        account=Account.create(),
        endpoint=studionet.rpc_urls["default"]["http"][0],
    )
    state = client.read_contract(
        address=data["contract_address"],
        function_name="get_state",
        args=[],
    )
    for field, value in EXPECTED_STATE.items():
        assert state[field] == value
