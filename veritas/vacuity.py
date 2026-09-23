"""Static checks for verification-shaped Python programs.

This is intentionally conservative: it reports whether a program has an
observable failure mechanism, not whether that mechanism is logically correct.
Dynamic mutation and sabotage tests are needed for the latter.
"""
from __future__ import annotations

import ast
import os
from pathlib import Path


_HINTS = ("test", "verify", "check", "validate", "audit", "gate", "harness")


def scan_file(path: str | Path) -> dict:
    path = Path(path)
    source = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return {"path": str(path), "status": "UNPARSEABLE", "reason": str(exc)}
    has_assert = any(isinstance(node, ast.Assert) for node in ast.walk(tree))
    has_raise = any(isinstance(node, ast.Raise) for node in ast.walk(tree))
    has_test = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    has_main = "__main__" in source
    verification_shaped = has_test or any(token in path.name.lower() for token in _HINTS)
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
    root = Path(root)
    files = [root] if root.is_file() else sorted(root.rglob("*.py"))
    reports = [scan_file(path) for path in files]
    return {
        "files_scanned": len(reports),
        "status": "NOT_INSPECTED" if not reports else (
            "FINDINGS" if any(r["status"] in {"NO_FAIL_PATH", "UNPARSEABLE"} for r in reports)
            else "CLEAN"
        ),
        "reports": reports,
    }
