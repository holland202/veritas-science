"""Static anti-vacuity checks for verification-shaped Python files."""
from __future__ import annotations

import ast
from pathlib import Path

VERIFY_HINTS = ("verify", "check", "validate", "audit", "gate", "harness", "test")
FAIL_WORDS = ("fail", "error", "wrong", "mismatch")


def _gather_python_files(root: str | Path):
    root = Path(root)
    if root.is_file():
        return [root] if root.suffix == ".py" else []
    return sorted(p for p in root.rglob("*.py") if p.is_file())


def _scan_single(path: Path) -> dict:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(path))
    except Exception as exc:  # pragma: no cover - parsing failure handled as output
        return {"path": str(path), "status": "UNPARSEABLE", "reason": str(exc)}

    has_assert = any(isinstance(node, ast.Assert) for node in ast.walk(tree))
    has_raise = any(isinstance(node, ast.Raise) for node in ast.walk(tree))
    has_test = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    has_main = "__main__" in source
    verification_shaped = has_test or any(token in path.name.lower() for token in VERIFY_HINTS)

    if not verification_shaped:
        status = "NOT_APPLICABLE"
    elif has_assert or has_raise or has_test or has_main:
        status = "HAS_FAIL_MECHANISM"
    else:
        status = "NO_FAIL_PATH"

    return {
        "path": str(path),
        "status": status,
        "assert": has_assert,
        "raise": has_raise,
        "test_functions": has_test,
        "main_guard": has_main,
    }


def scan(root: str | Path) -> dict:
    files = _gather_python_files(root)
    if not files:
        return {"files_scanned": 0, "status": "NOT_INSPECTED", "reports": []}

    reports = [_scan_single(path) for path in files]
    findings = [r for r in reports if r["status"] in {"NO_FAIL_PATH", "UNPARSEABLE"}]
    return {
        "files_scanned": len(files),
        "status": "FINDINGS" if findings else "CLEAN",
        "reports": reports,
    }


__all__ = ["scan"]
