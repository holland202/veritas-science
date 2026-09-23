from __future__ import annotations

import json
from typing import Any

from veritas.adapters import ExternalAdapter


def sentinel_hai_adapter() -> ExternalAdapter:
    """Reference adapter skeleton for sentinel-hai-validation.

    This does not import the external repository. It records the repository and a
    pinned commit as metadata for a future domain-specific analyzer.
    """

    def runner(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return {
            "adapter": "sentinel-hai-validation",
            "kind": "provisioned_adapter_skeleton",
            "status": "not_run",
            "message": "placeholder; external implementation should be bound to a pinned commit and protocol",
            "args": args,
            "kwargs": kwargs,
        }

    return ExternalAdapter(
        name="sentinel_hai",
        repository="https://github.com/holland202/sentinel-hai-validation",
        commit="1faf2e2e6f002f76c92d52e931842b6bd2634eaa",
        runner=runner,
        limitations=(
            "No domain logic is executed in this skeleton adapter; it is a metadata boundary only.",
            "The connected external implementation must be run under its own pinned version and protocol.",
        ),
    )


__all__ = ["sentinel_hai_adapter"]
