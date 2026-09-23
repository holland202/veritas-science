# Claim refutation semantics

`NOT_SUPPORTED` is a prediction-layer result. It is not automatically a
claim-level refutation.

A prediction may carry the explicit frozen-protocol field:

```json
{"id": "P1", "refutes_claim": true}
```

Only a failed prediction with `refutes_claim: true`, admissible evidence, a
valid protocol, and a passing verifier may produce the claim verdict
`REFUTED`. Otherwise a failed prediction produces `INSUFFICIENT_EVIDENCE`.

This preserves the distinction between:

- failing to establish a registered prediction; and
- establishing evidence against the broader claim.
