"""Reproducibility metadata for external implementations and runs."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(root: str | Path, *args: str) -> str | None:
    try:
        return subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def manifest(root: str | Path = ".", files: list[str] | None = None, seed: int | None = None) -> dict[str, Any]:
    """Build an observation manifest without pretending it proves authenticity."""
    root = Path(root)
    selected = files or []
    return {
        "repository": git_value(root, "config", "--get", "remote.origin.url"),
        "commit": git_value(root, "rev-parse", "HEAD"),
        "working_tree": git_value(root, "status", "--porcelain"),
        "files": {name: file_sha256(root / name) for name in selected if (root / name).is_file()},
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
            "veritas": "0.1.0",
        },
        "seed": seed,
    }


def digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=list).encode()
    return hashlib.sha256(encoded).hexdigest()
