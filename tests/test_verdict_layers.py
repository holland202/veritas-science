from __future__ import annotations

from veritas.evidence import EvidenceRecord, EvidenceState
from veritas.protocol import validate_protocol
from veritas.verdict import PredictionStatus, Verdict, VerifierStatus, claim_verdict, fail_closed


def record(state=EvidenceState.MEASURED):
    return EvidenceRecord(
        evidence_id="e-1", observation_id="o-1", evidence_state=state,
        source_type="test", source_identifier="fixture", timestamp="2026-01-01T00:00:00Z",
        content_hash="hash", integrity={"valid": True},
    )


def test_measured_evidence_is_not_claim_support():
    assert fail_closed([record()]).verdict is Verdict.INSUFFICIENT_EVIDENCE


def test_supported_prediction_and_passing_verifier_support_claim():
    assert claim_verdict([record()], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.PASS).verdict is Verdict.SUPPORTED


def test_unsupported_prediction_without_refutation_criterion_is_insufficient():
    assert claim_verdict([record()], prediction=PredictionStatus.NOT_SUPPORTED, verifier=VerifierStatus.PASS).verdict is Verdict.INSUFFICIENT_EVIDENCE


def test_unsupported_refutation_criterion_refutes_claim():
    assert claim_verdict([record()], prediction=PredictionStatus.NOT_SUPPORTED, verifier=VerifierStatus.PASS, refutation_criterion=True).verdict is Verdict.REFUTED


def test_failed_verifier_blocks_positive_or_refuted_claim():
    assert claim_verdict([record()], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.FAIL).verdict is Verdict.INSUFFICIENT_EVIDENCE
    assert claim_verdict([record()], prediction=PredictionStatus.NOT_SUPPORTED, verifier=VerifierStatus.FAIL, refutation_criterion=True).verdict is Verdict.INSUFFICIENT_EVIDENCE


def test_invalid_evidence_is_invalid():
    bad = record()
    bad = EvidenceRecord(**{**bad.__dict__, "content_hash": ""})
    assert claim_verdict([bad], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.PASS).verdict is Verdict.INVALID_EVIDENCE


def test_invalid_protocol_voids_claim():
    assert claim_verdict([record()], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.PASS, protocol_valid=False).verdict is Verdict.VOID


def test_protocol_requires_explicit_boolean_refutation_authority():
    protocol = {
        "title": "demo", "claim": "x", "epistemic_status": "measured",
        "assumptions": ["a"], "prior_art": ["b"], "hypothesis": "h", "null": "n",
        "predictions": [{"id": "P1", "metric": "effect", "null": "effect < 0.1", "direction": "greater", "threshold": 0.1, "alpha": 0.05, "n_min": 20, "anti_vacuity": {"reject_degenerate": True}}],
        "implementation": {"threshold": 0.5}, "data_contract": {"fields": {"x": "number"}}, "analysis": {"order_invariant": True},
    }
    assert "prediction missing:refutes_claim" in validate_protocol(protocol)
    protocol["predictions"][0]["refutes_claim"] = "no"
    assert "refutes_claim must be boolean" in validate_protocol(protocol)
