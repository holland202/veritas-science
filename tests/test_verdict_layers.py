from __future__ import annotations

from veritas.evidence import EvidenceRecord, EvidenceState
from veritas.verdict import PredictionStatus, Verdict, VerifierStatus, claim_verdict, fail_closed


def record(state=EvidenceState.MEASURED):
    return EvidenceRecord(
        evidence_id="e-1", observation_id="o-1", evidence_state=state,
        source_type="test", source_identifier="fixture", timestamp="2026-01-01T00:00:00Z",
        content_hash="hash", integrity={"valid": True},
    )


def test_measured_evidence_is_not_claim_support():
    assert fail_closed([record()]).verdict is Verdict.INSUFFICIENT_EVIDENCE


def test_claim_verdict_requires_all_layers():
    result = claim_verdict([record()], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.PASS)
    assert result.verdict is Verdict.SUPPORTED


def test_failed_verifier_blocks_positive_prediction():
    result = claim_verdict([record()], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.FAIL)
    assert result.verdict is Verdict.INSUFFICIENT_EVIDENCE


def test_invalid_protocol_voids_claim():
    result = claim_verdict([record()], prediction=PredictionStatus.SUPPORTED, verifier=VerifierStatus.PASS, protocol_valid=False)
    assert result.verdict is Verdict.VOID
