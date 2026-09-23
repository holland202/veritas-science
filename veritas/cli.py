from __future__ import annotations

import argparse
import json
from pathlib import Path

from .attacks.vacuity import scan
from .evidence import EvidenceRecord, EvidenceState
from .provenance import manifest
from .verdict import Verdict, fail_closed


def _example_records() -> list[EvidenceRecord]:
    return [
        EvidenceRecord(
            evidence_id="e-1",
            observation_id="o-1",
            evidence_state=EvidenceState.MEASURED,
            source_type="simulation",
            source_identifier="demo",
            timestamp="2026-01-01T00:00:00Z",
            content_hash="abcd1234",
            provenance={"status": "ASSERTED"},
            integrity={"valid": True},
            metadata={"value": 42.0},
        )
    ]


def _lint_command(path: str) -> int:
    result = scan(path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"CLEAN", "NOT_APPLICABLE"} else 1


def _manifest_command(path: str) -> int:
    root = Path(path)
    selected = [p.name for p in root.rglob("*.py")] if root.is_dir() else [root.name]
    data = manifest(root, files=selected, seed=2026)
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def _check_command() -> int:
    result = fail_closed(_example_records())
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.verdict is not Verdict.INVALID_EVIDENCE else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="veritas")
    sub = parser.add_subparsers(dest="command", required=True)

    lint = sub.add_parser("lint", help="scan a file or tree for vacuity-related fail-path issues")
    lint.add_argument("path")

    manifest = sub.add_parser("manifest", help="build a provenance manifest for a repository or directory")
    manifest.add_argument("path", nargs="?", default=".")

    check = sub.add_parser("check", help="evaluate a strict measured-only evidence contract")

    demo = sub.add_parser("demo", help="print a minimal example verdict and evidence bundle")

    args = parser.parse_args(argv)

    if args.command == "lint":
        return _lint_command(args.path)
    if args.command == "manifest":
        return _manifest_command(args.path)
    if args.command == "check":
        return _check_command()
    if args.command == "demo":
        result = fail_closed(_example_records())
        payload = {
            "evidence": [r.to_dict() for r in _example_records()],
            "verdict": result.to_dict(),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
