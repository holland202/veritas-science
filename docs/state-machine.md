# Veritas reconciliation decision

The repository contains two useful generations that are now intentionally separated:

1. **Prediction layer** — the original executable threshold demonstration produces `SUPPORTED`, `NOT_SUPPORTED`, or `INDETERMINATE` for a preregistered prediction.
2. **Evidence/verifier layer** — evidence admissibility and verifier status are evaluated independently.
3. **Claim layer** — only the combination of valid protocol, admissible evidence, a passing verifier, and a prediction status produces a claim verdict.

The canonical flow is:

```text
CLAIM → PREREGISTERED → FROZEN → EXECUTED
     → EVIDENCE ADMISSIBILITY + VERIFIER ATTACKS
     → PREDICTION TEST → CLAIM VERDICT
```

Measured evidence is a prerequisite, never a conclusion. The compatibility function `fail_closed()` therefore returns `INSUFFICIENT_EVIDENCE` for measured records when no claim comparison is supplied. Use `claim_verdict()` for the final epistemic mapping.

The layers remain separate because `NOT_SUPPORTED` is a prediction outcome, while `REFUTED` is a qualified claim outcome. A low metric, invalid sample, failed gate, and void protocol are not interchangeable.
