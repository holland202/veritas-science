"""Veritas scientific validation framework."""
__version__ = "0.1.1"

from .evidence import EvidenceRecord, EvidenceState, ResearchStatus
from .verdict import (
    PredictionStatus,
    VerifierStatus,
    Verdict,
    VerdictResult,
    admissibility,
    claim_verdict,
    fail_closed,
)

__all__ = [
    "__version__", "EvidenceRecord", "EvidenceState", "ResearchStatus",
    "PredictionStatus", "VerifierStatus", "Verdict", "VerdictResult",
    "admissibility", "claim_verdict", "fail_closed",
]
