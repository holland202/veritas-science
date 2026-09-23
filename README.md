# veritas-science

<p align="center">
  <img src="assets/veritas-banner.svg" alt="Veritas Science — evidence-first, fail-closed, adversarial scientific validation" width="100%" />
</p>

<p align="center"><strong>Executable scientific validation for claims that must survive scrutiny.</strong></p>

MIT-licensed scientific validation framework for claims, evidence, protocol execution, verifier qualification, and adversarial probing.

## Core principle

A result is not meaningful because a script printed a number or a model emitted a verdict. A result is meaningful only when:

- the claim is explicit,
- the protocol is fixed,
- the evidence is classified,
- the verifier is fail-closed,
- the result is bound to provenance,
- the verifier has been attacked or probed,
- the result remains conditional on the protocol and environment.

## Design principles

- Evidence state is not research status.
- Missing, inferred, defaulted, or untrusted evidence never becomes measured evidence.
- Positive claims require explicit contracts.
- A verifier must be fail-closed.
- A gate that cannot fail is not evidence.
- Reproduction is not verification.
- A result is only as good as the protocol, implementation, data, and provenance that produced it.
- External implementations are treated as pinned adapters, not implicit evidence.

## Scope

This repository defines the common scientific core:

- evidence states
- provenance manifests
- verdict semantics
- contract-style validation
- anti-vacuity checks
- mutation-style dependence checks
- external adapter boundaries

It does not define a domain-specific detector or claim. Domain-specific logic belongs in external adapters pinned to a repository and commit.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m veritas demo
python -m veritas check
python -m veritas lint .
```

## Open-source policy

This project is MIT-licensed. The core implementation is original to this repository. Upstream research repositories are cited as references and external subjects, not runtime dependencies.

The attribution and integration policy is documented in `ATTRIBUTION.md` and `docs/integration.md`.

## Repository structure

```text
veritas-science/
├── assets/veritas-banner.svg  # README identity banner
├── LICENSE
├── ATTRIBUTION.md
├── pyproject.toml
├── veritas/                   # evidence, verdicts, provenance, attacks
├── schemas/                   # machine-readable contracts
├── tests/                     # core contract tests
└── docs/                      # architecture and adapter policy
```

## Core workflow

```text
Claim
  ↓
Protocol / frozen contract
  ↓
Implementation
  ↓
Measured or recorded evidence
  ↓
Verifier / fail-closed gate
  ↓
Provenance manifest
  ↓
Qualified verdict
```

## First formal adapter

The first adapter is a pinned repository adapter for the Sentinel HAI benchmark flow. It records the source repository, exact commit, adapter name, limitations, and execution contract boundary without importing external code.

## License

MIT. See `LICENSE`.

## Author

Chad Edward Holland

## Citation

If you use this project, cite the repository and preserve the MIT notice.
