"""Every field the leader returns must be bound by the validator.

The router's consequence is a settle-or-void routing decision, and both fields
the leader returns reach state: ``decision`` is stored directly and ``stage``
travels into ``trigger_result_json`` / ``outcome_result_json``, which
``get_state()`` exposes. Leaving either unbound would let validators agree on
the routing while persisting different accounts of how it was reached. This
test pins the invariant so a field added to the consensus result later cannot
silently arrive in state unverified.
"""

import ast
from pathlib import Path

CANDIDATES = (
    Path("contracts/ConditionalMarketRouter.py"),
    Path("contracts/conditional_market_router.py"),
)


def _contract_path() -> Path:
    for candidate in CANDIDATES:
        if candidate.exists():
            return candidate
    raise AssertionError("conditional market router contract source not found")


def _named_function(name: str) -> ast.FunctionDef:
    tree = ast.parse(_contract_path().read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"{name} not found")


def _returned_keys() -> set:
    keys = set()
    for node in ast.walk(_named_function("leader_fn")):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict):
            for key in node.value.keys:
                assert isinstance(key, ast.Constant), "leader keys must be literals"
                keys.add(key.value)
    return keys


def _bound_keys() -> set:
    keys = set()
    for node in ast.walk(_named_function("validator_fn")):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            keys.add(node.args[0].value)
    return keys


def test_validator_binds_every_returned_field():
    returned = _returned_keys()
    assert returned, "expected the leader to return a result dict"
    unbound = returned - _bound_keys()
    assert unbound == set(), f"consensus fields reach state unbound: {sorted(unbound)}"


def test_both_routing_fields_are_bound():
    bound = _bound_keys()
    assert {"stage", "decision"} <= bound


def test_validator_carries_no_comparison_tolerance():
    """Guard against a tolerant comparison being introduced, as in RB-05."""
    for node in ast.walk(_named_function("validator_fn")):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id != "abs"
