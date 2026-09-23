# Open-source components considered

Veritas does not copy code from unrelated repositories. Components are either
optional dependencies, separately executed tools, or design references pinned by
version and license.

## Candidates

- [python-jsonschema/jsonschema](https://github.com/python-jsonschema/jsonschema) — MIT; mature JSON Schema validation for the `schemas/` contracts. Candidate optional runtime dependency.
- [sixty-north/cosmic-ray](https://github.com/sixty-north/cosmic-ray) — MIT; mature Python mutation-testing engine. Candidate integration for a future mutation adapter, not a replacement for Veritas's scientific verdict semantics.
- [ORNL/flowcept](https://github.com/ORNL/flowcept) — MIT; runtime provenance and workflow lineage. Candidate reference for future execution-event capture; use only after reviewing its dependency and data model surface.

## Policy

Before adding a dependency, record its exact version, license, transitive dependencies, and role. Do not let a third-party tool decide a Veritas claim verdict. External tools may produce observations or attack reports; Veritas retains the final contract and epistemic mapping.

Attribution for dependencies remains governed by each dependency's own license. Veritas's MIT copyright notice remains required for copies of the Veritas core.
