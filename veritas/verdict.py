"""Layered verdict semantics for Veritas."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable

from .evidence import EvidenceRecord, EvidenceState


class PredictionStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class VerifierStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_TESTED = "NOT_TESTED"


class Verdict(str, Enum):
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    INVALID_EVIDENCE = "INVALID_EVIDENCE"
    VOID = "VOID"


@dataclass(frozen=True)
class VerdictResult:
    verdict: Verdict
    reasons: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "reasons": list(self.reasons),
            "evidence_ids": list(self.evidence_ids),
            "metadata": self.metadata,
        }


def admissibility(records: Iterable[EvidenceRecord]) -> VerdictResult | None:
    items = list(records)
    ids = [record.evidence_id for record in items]
    if not items:
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, ["no evidence supplied"], ids)
    if any(not record.content_hash or record.integrity.get("valid") is False for record in items):
        return VerdictResult(Verdict.INVALID_EVIDENCE, ["evidence integrity is invalid"], ids)
    inadmissible = [record for record in items if record.evidence_state is not EvidenceState.MEASURED]
    if inadmissible:
        states = sorted({record.evidence_state.value for record in inadmissible})
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, [f"inadmissible evidence states: {', '.join(states)}"], ids)
    return None


def fail_closed(records: Iterable[EvidenceRecord]) -> VerdictResult:
    items = list(records)
    blocked = admissibility(items)
    if blocked is not None:
        return blocked
    return VerdictResult(
        Verdict.INSUFFICIENT_EVIDENCE,
        ["measured evidence is admissible but no claim comparison was supplied"],
        [record.evidence_id for record in items],
    )


def claim_verdict(
    records: Iterable[EvidenceRecord],
    *,
    prediction: PredictionStatus | str,
    verifier: VerifierStatus | str,
    protocol_valid: bool = True,
    refutation_criterion: bool = False,
    void_reason: str | None = None,
) -> VerdictResult:
    """Combine layers without equating prediction failure with refutation."""
    items = list(records)
    ids = [record.evidence_id for record in items]
    if not protocol_valid:
        return VerdictResult(Verdict.VOID, [void_reason or "protocol is invalid or not frozen"], ids)
    blocked = admissibility(items)
    if blocked is not None:
        return blocked
    verifier_status = VerifierStatus(verifier)
    prediction_status = PredictionStatus(prediction)
    if verifier_status is not VerifierStatus.PASS:
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, [f"verifier status: {verifier_status.value}"], ids)
    if prediction_status is PredictionStatus.SUPPORTED:
        return VerdictResult(Verdict.SUPPORTED, ["prediction supported under the valid protocol and verifier"], ids)
    if prediction_status is PredictionStatus.NOT_SUPPORTED and refutation_criterion:
        return VerdictResult(Verdict.REFUTED, ["explicit refutation criterion was not supported"], ids)
    if prediction_status is PredictionStatus.NOT_SUPPORTED:
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, ["prediction failed without explicit refutation authority"], ids)
    if prediction_status is PredictionStatus.INVALID:
        return VerdictResult(Verdict.INVALID_EVIDENCE, ["prediction result is invalid"], ids)
    return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, ["prediction result is indeterminate"], ids)
