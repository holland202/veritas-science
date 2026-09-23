from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from .attacks import attack
from .core import read_json, sha256, write_json
from .evidence import EvidenceRecord, EvidenceState
from .experiment import check_prediction, run
from .protocol import freeze, validate_protocol
from .verdict import PredictionStatus, VerifierStatus, claim_verdict


def demo_protocol() -> dict:
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
            "refutes_claim": False,
        }],
        "implementation": {"name": "threshold", "version": "1", "threshold": 0.5},
        "data_contract": {"fields": {"x": "finite number", "y": "0 or 1"}},
        "analysis": {"order_invariant": True, "seed": 7, "sealed_data": False},
    }


def _result_evidence(result: dict) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=f"result:{result.get('data_digest', sha256(result))}",
        observation_id="experiment-result",
        evidence_state=EvidenceState.MEASURED,
        source_type="veritas.experiment",
        source_identifier="threshold-reference",
        timestamp=datetime.now(timezone.utc).isoformat(),
        content_hash=sha256(result),
        provenance={"status": "EXECUTED", "semantic_role": "admissible_observation"},
        integrity={"valid": True},
        metadata={"result": result},
    )


def _prediction_status(checks: list[dict]) -> PredictionStatus:
    statuses = {check.get("status") for check in checks}
    if "INVALID" in statuses:
        return PredictionStatus.INVALID
    if "INDETERMINATE" in statuses:
        return PredictionStatus.INDETERMINATE
    if statuses == {"SUPPORTED"}:
        return PredictionStatus.SUPPORTED
    return PredictionStatus.NOT_SUPPORTED


def _refutation_criterion(protocol: dict, checks: list[dict]) -> bool:
    return any(
        prediction.get("refutes_claim") is True and check.get("status") == "NOT_SUPPORTED"
        for prediction, check in zip(protocol.get("predictions", []), checks)
    )


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
    demo = sub.add_parser("demo"); demo.add_argument("--out", default="run")
    attack_cmd = sub.add_parser("attack"); attack_cmd.add_argument("protocol"); attack_cmd.add_argument("--out", required=True)
    experiment = sub.add_parser("experiment"); experiment.add_argument("protocol"); experiment.add_argument("--data", required=True); experiment.add_argument("--out", required=True)
    verdict = sub.add_parser("verdict"); verdict.add_argument("protocol"); verdict.add_argument("attacks"); verdict.add_argument("result"); verdict.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.command == "demo":
        return _demo(args.out)
    protocol_object = read_json(args.protocol)
    protocol = protocol_object.get("payload", protocol_object)
    if args.command == "attack":
        write_json(args.out, attack(protocol))
    elif args.command == "experiment":
        write_json(args.out, run(protocol, read_json(args.data), protocol["analysis"].get("seed")))
    else:
        attacks, result = read_json(args.attacks), read_json(args.result)
        checks = [check_prediction(prediction, result) for prediction in protocol["predictions"]]
        prediction = _prediction_status(checks)
        verifier = VerifierStatus.PASS if attacks.get("passed") else VerifierStatus.FAIL
        protocol_errors = validate_protocol(protocol)
        refutation = _refutation_criterion(protocol, checks)
        claim = claim_verdict(
            [_result_evidence(result)], prediction=prediction, verifier=verifier,
            protocol_valid=not protocol_errors, refutation_criterion=refutation,
            void_reason="; ".join(protocol_errors) if protocol_errors else None,
        )
        write_json(args.out, {
            "claim_verdict": claim.verdict.value,
            "prediction_status": prediction.value,
            "verifier_status": verifier.value,
            "refutation_criterion": refutation,
            "claim_reasons": claim.reasons,
            "evidence_ids": claim.evidence_ids,
            "qualification": "conditional on this protocol, implementation, data, and verifier",
            "predictions": checks, "attacks": attacks, "result": result,
        })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
