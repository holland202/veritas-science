# Veritas state machine

The repository has one canonical layered interpretation:

```text
CLAIM
  ↓
PREREGISTERED → FROZEN
  ↓
EXECUTED
  ├── evidence admissibility
  ├── verifier attacks
  └── prediction test
          ↓
     CLAIM VERDICT
```

## Separate state machines

### Prediction layer

The original experiment runner returns:

- `SUPPORTED` — the registered prediction threshold was met;
- `NOT_SUPPORTED` — the threshold was not met or an anti-vacuity rule rejected it;
- `INDETERMINATE` — the metric was missing or non-finite;
- `INVALID` — the result cannot be interpreted under the prediction contract.

### Verifier layer

The verifier reports:

- `PASS` — registered attack controls passed;
- `FAIL` — a control detected a verifier weakness;
- `NOT_TESTED` — no attack qualification was performed.

### Claim layer

Only the combination of a valid protocol, admissible evidence, a passing verifier, and a prediction result produces a claim verdict:

- `SUPPORTED`
- `REFUTED`
- `INSUFFICIENT_EVIDENCE`
- `INVALID_EVIDENCE`
- `VOID`

Measured evidence is a prerequisite for evaluating support. It is never support by itself. `fail_closed()` therefore returns `INSUFFICIENT_EVIDENCE` for measured records when no claim comparison is supplied.
