from __future__ import annotations

import json
from pathlib import Path

from veritas.evidence import EvidenceRecord, EvidenceState
from veritas.verdict import Verdict, fail_closed
from veritas.attacks.vacuity import scan


def test_fail_closed_measurement_only():
    rec = EvidenceRecord(
        evidence_id="e-1",
        observation_id="o-1",
        evidence_state=EvidenceState.MEASURED,
        source_type="simulation",
        source_identifier="sim-1",
        timestamp="2026-01-01T00:00:00Z",
        content_hash="abcd1234",
        provenance={"status": "ASSERTED"},
        integrity={"valid": True},
    )
    result = fail_closed([rec])
    assert result.verdict is Verdict.SUPPORTED


def test_inferred_evidence_is_rejected():
    rec = EvidenceRecord(
        evidence_id="e-2",
        observation_id="o-2",
        evidence_state=EvidenceState.INFERRED,
        source_type="model",
        source_identifier="infer-1",
        timestamp="2026-01-01T00:00:00Z",
        content_hash="efgh5678",
        provenance={"status": "ASSERTED"},
        integrity={"valid": True},
    )
    result = fail_closed([rec])
    assert result.verdict is Verdict.INSUFFICIENT_EVIDENCE


def test_static_scan_detects_vacuity_shape(tmp_path):
    py = tmp_path / "verify_example.py"
    py.write_text("print('[FAIL] check failed')\nprint('done')\n")
    result = scan(tmp_path)
    assert any(report["status"] == "NO_FAIL_PATH" for report in result["reports"])


def test_schema_files_are_valid_json():
    for name in ["protocol.json", "evidence.json", "result.json", "verdict.json"]:
        path = Path(__file__).resolve().parents[1] / "schemas" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert "$schema" in data


def test_manifest_records_environment():
    from veritas.provenance import manifest
    data = manifest(Path(__file__).resolve().parents[1], files=["README.md"], seed=7)
    assert "environment" in data
    assert "seed" in data
