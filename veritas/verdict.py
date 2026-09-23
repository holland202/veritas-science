"""Layered verdict semantics for Veritas.

Prediction status, verifier status, and claim verdict are deliberately separate
state machines.  Measured evidence is admissible input, not a claim conclusion.
"""
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
    """Return a blocking result, or ``None`` when evidence is admissible.

    Admissibility is intentionally not support. A later claim evaluator must
    compare an admissible result with the preregistered prediction and null.
    """
    items = list(records)
    ids = [r.evidence_id for r in items]
    if not items:
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, ["no evidence supplied"], ids)
    invalid = [r for r in items if not r.content_hash or r.integrity.get("valid") is False]
    if invalid:
        return VerdictResult(Verdict.INVALID_EVIDENCE, ["evidence integrity is invalid"], ids)
    inadmissible = [r for r in items if r.evidence_state is not EvidenceState.MEASURED]
    if inadmissible:
        states = sorted({r.evidence_state.value for r in inadmissible})
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, [f"inadmissible evidence states: {', '.join(states)}"], ids)
    return None


def fail_closed(records: Iterable[EvidenceRecord]) -> VerdictResult:
    """Compatibility wrapper: validate admissibility, never infer support.

    A collection of measured records alone is not a supported claim. It is
    returned as ``INSUFFICIENT_EVIDENCE`` until a prediction evaluator supplies
    the claim comparison and verifier result.
    """
    items = list(records)
    blocked = admissibility(items)
    if blocked is not None:
        return blocked
    return VerdictResult(
        Verdict.INSUFFICIENT_EVIDENCE,
        ["measured evidence is admissible but no claim comparison was supplied"],
        [r.evidence_id for r in items],
    )


def claim_verdict(
    records: Iterable[EvidenceRecord],
    *,
    prediction: PredictionStatus | str,
    verifier: VerifierStatus | str,
    protocol_valid: bool = True,
    void_reason: str | None = None,
) -> VerdictResult:
    """Translate the independent layers into a qualified claim verdict."""
    items = list(records)
    ids = [r.evidence_id for r in items]
    if not protocol_valid:
        return VerdictResult(Verdict.VOID, [void_reason or "protocol is invalid or not frozen"], ids)
    blocked = admissibility(items)
    if blocked is not None:
        return blocked
    v = VerifierStatus(verifier)
    p = PredictionStatus(prediction)
    if v is not VerifierStatus.PASS:
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, [f"verifier status: {v.value}"], ids)
    if p is PredictionStatus.SUPPORTED:
        return VerdictResult(Verdict.SUPPORTED, ["prediction supported under the valid protocol and verifier"], ids)
    if p is PredictionStatus.NOT_SUPPORTED:
        return VerdictResult(Verdict.REFUTED, ["prediction was not supported under the valid protocol"], ids)
    if p is PredictionStatus.INVALID:
        return VerdictResult(Verdict.INVALID_EVIDENCE, ["prediction result is invalid"], ids)
    return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, ["prediction result is indeterminate"], ids)
