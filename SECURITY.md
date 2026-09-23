# Operational safety and scientific limitations

Veritas is an evidence and validation instrument, not a proof engine or safety certification.

Before a consequential experiment:

1. Have domain experts approve the claim, assumptions, null, sampling plan, stopping rule, and analysis.
2. Freeze the protocol and record its digest outside the execution environment.
3. Seal or independently hash the evaluation data before running the implementation.
4. Add domain-specific treatment for dependence, missingness, censoring, calibration, uncertainty, and multiple comparisons.
5. Run known-positive, known-negative, null, malformed, metamorphic, and sabotage controls against the verifier.
6. Retain all failed attacks, refutations, amendments, and rejected branches.
7. Never interpret `SUPPORTED` as universal truth, production authorization, or evidence of safety.
8. Do not deploy the included threshold demo to control people, machines, infrastructure, or medical decisions.

The included runner is deterministic and dependency-free to make the methodology inspectable. It intentionally does not pretend to solve every statistical or operational problem. Production adapters must preserve the protocol/result/attack/verdict boundaries and document every additional assumption.
