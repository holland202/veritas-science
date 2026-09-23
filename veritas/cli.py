from __future__ import annotations

import argparse
from pathlib import Path

from .attacks import attack
from .core import read_json, write_json
from .experiment import check_prediction, run
from .protocol import freeze


def demo_protocol() -> dict:
    """Return the original executable threshold protocol."""
    return {
        "title": "Deterministic threshold demonstration",
        "claim": "The fixed threshold classifier improves on majority baseline by at least 0.10.",
        "epistemic_status": "measured",
        "assumptions": ["rows are independent", "y is binary", "threshold is fixed before evaluation"],
        "prior_art": ["Majority-class accuracy is a baseline."],
        "hypothesis": "accuracy_minus_majority >= 0.10",
        "null": "accuracy_minus_majority < 0.10",
        "predictions": [{
            "id": "P1", "metric": "effect", "null": "effect < 0.10", "direction": "greater",
            "threshold": 0.10, "alpha": 0.05, "n_min": 20,
            "anti_vacuity": {"require_finite": True, "reject_degenerate": True},
        }],
        "implementation": {"name": "threshold", "version": "1", "threshold": 0.5},
        "data_contract": {"fields": {"x": "finite number", "y": "0 or 1"}},
        "analysis": {"order_invariant": True, "seed": 7, "sealed_data": False},
    }


def _demo(out: str) -> int:
    path = Path(out)
    path.mkdir(parents=True, exist_ok=True)
    protocol = freeze(demo_protocol())
    data = [{"x": i / 100, "y": int(i >= 50)} for i in range(100)]
    write_json(path / "protocol.json", protocol)
    write_json(path / "data.json", data)
    write_json(path / "attacks.json", attack(protocol["payload"]))
    write_json(path / "result.json", run(protocol["payload"], data, 7))
    print(f"wrote {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="veritas")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo")
    demo.add_argument("--out", default="run")
    attack_cmd = sub.add_parser("attack")
    attack_cmd.add_argument("protocol")
    attack_cmd.add_argument("--out", required=True)
    experiment = sub.add_parser("experiment")
    experiment.add_argument("protocol")
    experiment.add_argument("--data", required=True)
    experiment.add_argument("--out", required=True)
    verdict = sub.add_parser("verdict")
    verdict.add_argument("protocol")
    verdict.add_argument("attacks")
    verdict.add_argument("result")
    verdict.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.command == "demo":
        return _demo(args.out)

    protocol_obj = read_json(args.protocol)
    protocol = protocol_obj.get("payload", protocol_obj)
    if args.command == "attack":
        write_json(args.out, attack(protocol))
    elif args.command == "experiment":
        write_json(args.out, run(protocol, read_json(args.data), protocol["analysis"].get("seed")))
    else:
        attacks, result = read_json(args.attacks), read_json(args.result)
        checks = [check_prediction(p, result) for p in protocol["predictions"]]
        prediction_status = "SUPPORTED" if all(x["status"] == "SUPPORTED" for x in checks) else (
            "INDETERMINATE" if any(x["status"] == "INDETERMINATE" for x in checks) else "NOT_SUPPORTED"
        )
        verifier_status = "PASS" if attacks.get("passed") else "FAIL"
        claim_status = "SUPPORTED" if attacks.get("passed") and prediction_status == "SUPPORTED" else (
            "REFUTED" if attacks.get("passed") and prediction_status == "NOT_SUPPORTED" else "INSUFFICIENT_EVIDENCE"
        )
        write_json(args.out, {
            "claim_verdict": claim_status,
            "prediction_status": prediction_status,
            "verifier_status": verifier_status,
            "qualification": "conditional on this protocol, implementation, data, and verifier",
            "predictions": checks,
            "attacks": attacks,
            "result": result,
        })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
