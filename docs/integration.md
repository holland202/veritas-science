# Integration policy

Veritas uses a small MIT-licensed core and treats other repositories as pinned experimental subjects or adapters.

## Rules

- The core does not import unrelated repositories at runtime.
- An adapter records repository, exact commit, implementation digest, environment, and limitations.
- A result from an adapter is evidence only under an explicit Veritas protocol.
- A dashboard, model output, hash, or self-attested manifest is not sufficient semantic evidence by itself.
- External code is not copied into the core unless its license and provenance are clear.
- Reproduction and verification remain separate statuses.

## First adapters

The planned order is:

1. `sentinel-hai-validation` for preregistered anomaly-detection gates.
2. `evidence-ledger` concepts for the evidence schema, reimplemented cleanly in Veritas.
3. `vacuity_lint.py` and `veritas-eval-harness` concepts for static and dynamic verifier attacks.
4. `coverage-preserving-synthesis`, `qolas-synthesis`, and `quasar` as pinned domain experiments.

The adapter boundary is deliberately narrow. Veritas supplies protocol, provenance, attacks, and verdict semantics; the external repository supplies the domain implementation.
