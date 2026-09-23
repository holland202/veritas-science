# Adapter contract pattern

The external repository adapter boundary is intentionally narrow.

An adapter does three things:

1. identifies the upstream repository and exact commit;
2. records the protocol or gate family it is implementing;
3. defines the execution contract and known limitations without importing the upstream implementation.

This design keeps the core domain-neutral and the adapter auditable.

## Example

The Sentinel HAI adapter records:

- repository: https://github.com/holland202/sentinel-hai-validation
- commit: 1faf2e2e6f002f76c92d52e931842b6bd2634eaa
- protocol: sentinel_hai_validation
- gate names: P0a, P0b, P1, P3, P5, P7a
- required manifest fields: experiment commit, manifest-generation commit, freeze digest, dataset hashes, code hashes, environment, seed

The actual external implementation must still be executed separately under that exact commit and protocol.
