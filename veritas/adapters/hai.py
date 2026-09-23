"""Pinned external-domain adapter contract for the Sentinel HAI benchmark.

This adapter is intentionally a metadata boundary. The external implementation is
not imported here. It is represented as a pinned repository + commit + contract
reference so the scientific protocol remains domain-neutral while the actual
analysis remains external and versioned.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from veritas.adapters import ExternalAdapter


@dataclass(frozen=True)
class HAIAdapterSpec:
    repository: str = "https://github.com/holland202/sentinel-hai-validation"
    commit: str = "1faf2e2e6f002f76c92d52e931842b6bd2634eaa"
    name: str = "sentinel_hai"
    protocol_name: str = "sentinel_hai_validation"
    gate_names: tuple[str, ...] = (
        "P0a",
        "P0b",
        "P1",
        "P3",
        "P5",
        "P7a",
    )
    required_manifest_fields: tuple[str, ...] = (
        "experiment_commit",
        "manifest_generation_commit",
        "freeze_digest",
        "dataset_hashes",
        "code_hashes",
        "environment",
        "seed",
    )
    limitations: tuple[str, ...] = (
        "No external implementation is executed here.",
        "This adapter only records the external contract and pinned commit.",
        "The domain result is evidence only under the protocol that calls this adapter.",
    )

    def as_adapter(self) -> ExternalAdapter:
        def runner(*args: Any, **kwargs: Any) -> dict[str, Any]:
            return {
                "protocol_name": self.protocol_name,
                "repository": self.repository,
                "commit": self.commit,
                "status": "not_run",
                "note": "placeholder contract only; the actual external implementation must be executed under its pinned repository and commit",
                "args": args,
                "kwargs": kwargs,
            }

        return ExternalAdapter(
            name=self.name,
            repository=self.repository,
            commit=self.commit,
            runner=runner,
            limitations=self.limitations,
        )


def sentinel_hai_adapter() -> ExternalAdapter:
    """Return the pinned Sentinel adapter boundary."""
    return HAIAdapterSpec().as_adapter()


__all__ = ["HAIAdapterSpec", "sentinel_hai_adapter"]
