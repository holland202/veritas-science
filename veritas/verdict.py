"""Strict, contract-oriented verdict evaluation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

from .evidence import EvidenceRecord, EvidenceState


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
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict.value,
            "reasons": list(self.reasons),
            "evidence_ids": list(self.evidence_ids),
            "metadata": self.metadata,
        }


def fail_closed(records: Iterable[EvidenceRecord]) -> VerdictResult:
    """Apply the default measured-only contract.

    This function does not decide whether a measured value satisfies a domain
    claim; it only prevents an absent, inferred, defaulted, or unverified value
    from becoming a positive result by accident.
    """
    items = list(records)
    ids = [r.evidence_id for r in items]
    if not items:
        return VerdictResult(Verdict.INSUFFICIENT_EVIDENCE, ["no evidence supplied"], ids)
    invalid = [r for r in items if not r.content_hash or r.integrity.get("valid") is False]
    if invalid:
        return VerdictResult(
            Verdict.INVALID_EVIDENCE,
            ["evidence hash or declared integrity is invalid"],
            ids,
        )
    inadmissible = [r for r in items if not r.is_measured]
    if inadmissible:
        states = sorted({r.evidence_state.value for r in inadmissible})
        return VerdictResult(
            Verdict.INSUFFICIENT_EVIDENCE,
            [f"evidence states are not admissible: {', '.join(states)}"],
            ids,
        )
    return VerdictResult(Verdict.SUPPORTED, ["all supplied evidence is measured"], ids)
