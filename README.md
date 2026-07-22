# EvoOM Guard Release Source Admission V2 Pilot

This repository is a deliberately narrow live-integration pilot for EvoOM
Guard's `EVOGUARD_RELEASE_SOURCE_ADMISSION_V2` envelope. It tests whether one
exact, single-parent protected-main source commit can travel through a
three-workflow A/B/C trust topology and then pass a detached D verification.

It is **not** a release publisher, artifact gate, deployment gate, production
service, or independent security audit. An `ALLOW` from this pilot authorizes
source only. It does not authorize any package, image, executable, release, or
deployment.

## Topology

```text
A  EvoGuard Release Source Reverify
   workflow_dispatch; no secret/OIDC/write; strong Docker black-box PASS
              |
              v
B  EvoGuard Produce Release Source Receipt
   workflow_run(A); no checkout/candidate execution; GitHub attests receipt
              |
              v
C  EvoGuard Admit Release Source
   workflow_run(B); protected Environment; root sealer drops only gh to a
   dedicated non-root UID/GID; signs one V2 source ALLOW after fresh verification
              |
              v
D  detached-verify job in C
   no Environment/private key/fresh attestation-provider call; verifies the signed envelope
   against externally supplied source, workflow, tool, UID/GID, and key roots
```

D is intentionally a second job inside C. GitHub limits chained
`workflow_run` workflows; it is not a fourth workflow. D is detached from the
key-bearing/provider operation, but it is not an offline job: it downloads the
retained controls and envelope plus a hash-pinned verifier runtime and
hash-locked dependencies.

## Safe initial state

All A/B/C entry jobs are fail-closed behind the administrative repository
variable `EVOGUARD_RELEASE_SOURCE_V2_ENABLED == "true"`. Publish C0 with the
variable absent or `false`. Configure and audit every external root before
setting it to `true`.

The first admitted target must be a later **source-only, one-parent** main
commit. The baseline commit must already contain the judge pack, hash-locked
judge dependencies, and reviewed A/B/C workflow blobs. Do not attempt to admit
the bootstrap commit itself.

See:

- [`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md) for the ordered C0/C1 procedure.
- [`docs/SETTINGS.md`](docs/SETTINGS.md) for the complete external root set.
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) for guarantees and non-claims.
- [`docs/NEGATIVE_MATRIX.md`](docs/NEGATIVE_MATRIX.md) for required fail-closed exercises.
- [`trust/public/README.md`](trust/public/README.md) for key handling.

## Local validation

```bash
python -m pip install pytest PyYAML
python -m pytest -q
```

The local tests validate YAML syntax and static workflow contracts. They do not
claim that GitHub executed A/B/C/D or that an Environment, ruleset, variable,
secret, artifact attestation, runner image, or provider result exists.
