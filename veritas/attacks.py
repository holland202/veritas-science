from .experiment import check_prediction
from .protocol import validate_protocol


def attack(protocol):
    """Run verifier controls; these test the instrument, not the scientific claim."""
    errors = validate_protocol(protocol)
    predictions = protocol.get("predictions", [])
    reports = [
        {"name": "protocol_schema", "passed": not errors, "details": errors},
        {"name": "explicit_null", "passed": bool(protocol.get("null"))},
        {"name": "anti_vacuity", "passed": all(bool(p.get("anti_vacuity")) for p in predictions)},
        {"name": "order_invariance_declared", "passed": protocol.get("analysis", {}).get("order_invariant") is True},
    ]
    # Known-negative control: the verifier must not silently accept a degenerate
    # perfect result when the protocol's anti-vacuity policy rejects it.
    fake = {"n": max([p.get("n_min", 2) for p in predictions] or [2]),
            "accuracy": 1.0, "effect": 1.0}
    negative = [check_prediction(p, fake) for p in predictions]
    reports.append({"name": "degenerate_control",
                    "passed": all(x["status"] != "SUPPORTED" for x in negative),
                    "details": negative})
    return {"passed": all(r["passed"] for r in reports), "verifier_attacks": reports}
