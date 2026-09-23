"""Adapters are external implementations, never implicit evidence."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class AdapterResult:
    adapter: str
    source_repository: str
    source_commit: str
    result: dict[str, Any]
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter": self.adapter,
            "source_repository": self.source_repository,
            "source_commit": self.source_commit,
            "result": self.result,
            "limitations": self.limitations,
        }


@dataclass(frozen=True)
class ExternalAdapter:
    name: str
    repository: str
    commit: str
    runner: Callable[..., dict[str, Any]]
    limitations: tuple[str, ...] = ()

    def run(self, *args: Any, **kwargs: Any) -> AdapterResult:
        return AdapterResult(
            self.name,
            self.repository,
            self.commit,
            self.runner(*args, **kwargs),
            list(self.limitations),
        )
