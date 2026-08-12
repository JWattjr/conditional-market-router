import json


def _deploy(direct_deploy):
    return direct_deploy(
        "contracts/ConditionalMarketRouter.py",
        "route-1",
        {"question": "Does trigger happen?"},
        {"question": "Does outcome happen?"},
        ["https://trigger.example.org/record"],
        ["https://outcome.example.org/record"],
        "2030-01-01T00:00:00Z",
        "2030-02-01T00:00:00Z",
    )


def test_routes_trigger_then_outcome(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2030-01-02T00:00:00Z")
    direct_vm.mock_web(r".*", {"status": 200, "body": "evidence"})
    direct_vm.mock_llm(r".*", json.dumps({"decision": "TRUE"}))
    contract.resolve_trigger()
    direct_vm.clear_mocks()
    direct_vm.warp("2030-02-02T00:00:00Z")
    direct_vm.mock_web(r".*", {"status": 200, "body": "evidence"})
    direct_vm.mock_llm(r".*", json.dumps({"decision": "FALSE"}))
    assert contract.resolve_outcome()["decision"] == "FALSE"
    assert contract.get_state()["outcome"] == "NO"
    assert direct_vm.run_validator()


def test_false_trigger_voids_market(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2030-01-02T00:00:00Z")
    direct_vm.mock_web(r".*", {"status": 200, "body": "evidence"})
    direct_vm.mock_llm(r".*", json.dumps({"decision": "FALSE"}))
    contract.resolve_trigger()
    assert contract.get_state()["outcome"] == "VOID"
