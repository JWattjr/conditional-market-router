import json

import pytest


TRIGGER_DEADLINE = "2030-01-01T00:00:00Z"
OUTCOME_DEADLINE = "2030-02-01T00:00:00Z"


def _deploy(
    direct_deploy,
    *,
    market_id="route-1",
    trigger_spec=None,
    outcome_spec=None,
    trigger_sources=None,
    outcome_sources=None,
    trigger_deadline=TRIGGER_DEADLINE,
    outcome_deadline=OUTCOME_DEADLINE,
):
    return direct_deploy(
        "contracts/ConditionalMarketRouter.py",
        market_id,
        trigger_spec if trigger_spec is not None else {"question": "Does trigger happen?"},
        outcome_spec if outcome_spec is not None else {"question": "Does outcome happen?"},
        trigger_sources if trigger_sources is not None else ["https://trigger.example.org/record"],
        outcome_sources if outcome_sources is not None else ["https://outcome.example.org/record"],
        trigger_deadline,
        outcome_deadline,
    )


def _mock_decision(direct_vm, decision):
    direct_vm.mock_web(r".*", {"status": 200, "body": "official evidence"})
    direct_vm.mock_llm(r".*", json.dumps({"decision": decision}))


def test_routes_trigger_then_outcome_and_rejects_false_leader(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2030-01-02T00:00:00Z")
    _mock_decision(direct_vm, "TRUE")
    assert contract.resolve_trigger() == {"stage": "trigger", "decision": "TRUE"}
    assert contract.get_state()["status"] == "TRIGGER_CONFIRMED"
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result={"stage": "trigger", "decision": "FALSE"})

    direct_vm.clear_mocks()
    direct_vm.warp("2030-02-02T00:00:00Z")
    _mock_decision(direct_vm, "FALSE")
    assert contract.resolve_outcome() == {"stage": "outcome", "decision": "FALSE"}
    state = contract.get_state()
    assert state["status"] == "SETTLED"
    assert state["outcome"] == "NO"
    assert state["attempts"] == 2
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result={"stage": "outcome", "decision": "TRUE"})


def test_false_trigger_voids_market_and_terminal_replay_is_safe(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2030-01-02T00:00:00Z")
    _mock_decision(direct_vm, "FALSE")
    contract.resolve_trigger()
    state = contract.get_state()
    assert state["status"] == "VOID"
    assert state["outcome"] == "VOID"
    assert state["attempts"] == 1

    direct_vm.clear_mocks()
    replay = contract.resolve_trigger()
    assert replay["status"] == "VOID"
    assert contract.get_state()["attempts"] == 1


def test_all_sources_down_is_unresolved_and_retryable(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2030-01-02T00:00:00Z")
    direct_vm.mock_web(r".*", {"status": 503, "body": "offline"})
    assert contract.resolve_trigger() == {"stage": "trigger", "decision": "UNRESOLVED"}
    assert contract.get_state()["status"] == "TRIGGER_UNRESOLVED"
    assert contract.get_state()["attempts"] == 1

    direct_vm.clear_mocks()
    _mock_decision(direct_vm, "TRUE")
    assert contract.resolve_trigger()["decision"] == "TRUE"
    assert contract.get_state()["status"] == "TRIGGER_CONFIRMED"
    assert contract.get_state()["attempts"] == 2


def test_web_request_exception_is_treated_as_unavailable(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2030-01-02T00:00:00Z")
    direct_vm._live_web_handler = lambda _request: {"error": "simulated timeout"}
    assert contract.resolve_trigger() == {"stage": "trigger", "decision": "UNRESOLVED"}
    assert contract.get_state()["status"] == "TRIGGER_UNRESOLVED"


def test_deadlines_and_stage_order_are_enforced(direct_vm, direct_deploy):
    contract = _deploy(direct_deploy)
    direct_vm.warp("2029-12-31T00:00:00Z")
    with direct_vm.expect_revert("trigger deadline has not passed"):
        contract.resolve_trigger()

    assert contract.resolve_outcome()["status"] == "OPEN"
    direct_vm.warp("2030-01-02T00:00:00Z")
    _mock_decision(direct_vm, "TRUE")
    contract.resolve_trigger()
    direct_vm.clear_mocks()
    with direct_vm.expect_revert("outcome deadline has not passed"):
        contract.resolve_outcome()


@pytest.mark.parametrize(
    "url",
    [
        "http://example.org/record",
        "https://localhost/record",
        "https://127.0.0.1/record",
        "https://10.0.0.1/record",
        "https://service.internal/record",
        "https://[::1]/record",
        "https://[::ffff:127.0.0.1]/record",
        "https://[ff02::1]/record",
        "https://bad_host.example/record",
    ],
)
def test_rejects_non_public_or_malformed_sources(direct_vm, direct_deploy, url):
    with direct_vm.expect_revert():
        _deploy(direct_deploy, trigger_sources=[url])


def test_rejects_duplicate_sources(direct_vm, direct_deploy):
    url = "https://example.org/record"
    with direct_vm.expect_revert("must be unique"):
        _deploy(direct_deploy, trigger_sources=[url, url])


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"market_id": ""}, "market_id"),
        ({"trigger_spec": {}}, "question"),
        ({"trigger_spec": "not-json"}, "Invalid trigger spec JSON"),
        ({"trigger_sources": []}, "1-8 URLs"),
        ({"trigger_deadline": "2030-01-01T00:00:00"}, "timezone offset is required"),
        ({"outcome_deadline": TRIGGER_DEADLINE}, "future and ordered"),
    ],
)
def test_rejects_invalid_constructor_inputs(direct_vm, direct_deploy, overrides, message):
    with direct_vm.expect_revert(message):
        _deploy(direct_deploy, **overrides)


def test_rejects_oversized_specs(direct_vm, direct_deploy):
    with direct_vm.expect_revert("must not exceed 4000 characters"):
        _deploy(
            direct_deploy,
            trigger_spec={"question": "Does trigger happen?", "metadata": "x" * 4000},
        )
