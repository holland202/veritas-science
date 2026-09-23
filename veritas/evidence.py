"""Evidence states and provenance-aware records.

This module defines the clean-room Veritas evidence vocabulary.  Evidence state
and research status are deliberately separate: a measured observation may still
be unverified, and a verified test may intentionally use absent evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EvidenceState(str, Enum):
    MEASURED = "MEASURED"
    DERIVED = "DERIVED"
    INFERRED = "INFERRED"
    OPERATOR = "OPERATOR"
    ABSENT = "ABSENT"
    DEFAULTED = "DEFAULTED"
    UNVERIFIED = "UNVERIFIED"
    NEVER_WIRED = "NEVER_WIRED"


class ResearchStatus(str, Enum):
    NOT_TESTED = "NOT_TESTED"
    IMPLEMENTED = "IMPLEMENTED"
    EXPERIMENTAL = "EXPERIMENTAL"
    VERIFIED = "VERIFIED"
    REPRODUCED = "REPRODUCED"
    REFUTED = "REFUTED"
    VOID = "VOID"
    UNVERIFIED = "UNVERIFIED"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    observation_id: str
    evidence_state: EvidenceState
    source_type: str
    source_identifier: str
    timestamp: str
    content_hash: str
    provenance: dict[str, Any] = field(default_factory=dict)
    integrity: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "observation_id": self.observation_id,
            "evidence_state": self.evidence_state.value,
            "source_type": self.source_type,
            "source_identifier": self.source_identifier,
            "timestamp": self.timestamp,
            "content_hash": self.content_hash,
            "provenance": self.provenance,
            "integrity": self.integrity,
            "metadata": self.metadata,
        }

    @property
    def is_measured(self) -> bool:
        return self.evidence_state is EvidenceState.MEASURED
