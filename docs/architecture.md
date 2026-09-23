# Veritas architecture

```mermaid
flowchart TD
    C[Claim] --> P[Preregistered protocol]
    P --> F[Freeze + SHA-256 digest]
    F --> I[Reference implementation]
    I --> A[Adversarial verifier]
    A --> S[Sealed experiment]
    S --> V[Qualified verdict]
    V --> R[Replication / transfer]
    V --> L[(Append-only evidence ledger)]
    A --> L
    S --> L
    R --> L
    A -. failure retained .-> X[Refutation / amendment branch]
    X --> P
```

## Runtime boundaries

| Boundary | Input | Output | Safety property |
|---|---|---|---|
| Protocol | Claim, assumptions, null, predictions | Frozen protocol | No silent post-hoc changes |
| Instrument | Frozen protocol + data | Deterministic result | Implementation is not evidence |
| Attacker | Protocol + verifier | Attack report | Verifier must be falsifiable |
| Verdict | Attack report + result | Qualified status | No unconditional truth claim |
| Ledger | All artifacts | Hash chain | Tampering is detectable |

The supplied threshold implementation is a reference instrument only. Production adapters should preserve these boundaries and add domain-specific statistics, missingness, dependence, uncertainty, and multiple-comparison controls.
