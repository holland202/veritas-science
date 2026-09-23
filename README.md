# Veritas Science

**An executable scientific validation pipeline that treats the verifier as a falsifiable object.**

Veritas turns a claim into a versioned, hashed protocol; runs deterministic reference implementations; attacks the analysis with nulls, sabotage, metamorphic tests, dependence checks, ties, numerical edge cases, and vacuity checks; then emits a verdict whose failures remain in the record.

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
veritas demo --out run
veritas attack run/protocol.json --out run/attacks.json
veritas experiment run/protocol.json --out run/result.json
veritas verdict run/protocol.json run/attacks.json run/result.json --out run/verdict.json
python -m unittest discover -s tests -v
```

The demo is a fully executable synthetic experiment. It demonstrates the machinery, including a deliberately explicit null and verifier attack controls. It is not evidence for a real-world scientific claim.

## Pipeline

`claim → assumptions → prior art → preregistration → implementation → attack → freeze → sealed run → verdict → replication → admission/refutation`

Artifacts are canonical JSON with SHA-256 digests. Amendments create a new protocol with `parent_digest`; history is not overwritten. Results include protocol, data, implementation, and environment metadata.

The default runner is intentionally dependency-free and conservative. Before using real data, add domain-appropriate handling for dependence, missingness, confidence intervals, multiple comparisons, and data sealing. See `SECURITY.md`.
