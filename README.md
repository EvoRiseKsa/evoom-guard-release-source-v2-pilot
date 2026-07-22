# EvoOM Guard Release Source + Artifact Admission Pilot

This repository is a deliberately narrow live-integration pilot for EvoOM
Guard's source-to-artifact trust boundary. Round 1 exercised the
`EVOGUARD_RELEASE_SOURCE_ADMISSION_V2` envelope across A/B/C and detached D.
The disabled second topology adds E/F/G for the published v4.2.0
`EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1` contract.

It is **not** a release publisher, artifact gate, deployment gate, production
service, or independent security audit. A source `ALLOW` authorizes source only;
a later artifact `ALLOW` binds one exact data file to that source authorization.
Neither result authorizes a package, image, release, publication, or deployment.

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
   no Environment/protected signing key/fresh attestation-provider call;
   verifies the signed envelope
   against externally supplied source, workflow, tool, UID/GID, and key roots

E  EvoGuard Build Release Artifact
   workflow_dispatch; no secret; verifies a fresh RSAE, builds one bounded
   canonical data file, and requests one GitHub Artifact Attestation
              |
              v
F  EvoGuard Admit Release Artifact
   workflow_run(E); no-secret preflight then a separate protected Environment;
   freshly verifies E and signs one RAAE with a sixth distinct key
              |
              v
G  EvoGuard Verify Release Artifact
   workflow_run(F); no Environment, trusted signing key, OIDC, or live provider call;
   verifies RAAE + artifact + nested RSAE and retained provider evidence
```

D is intentionally a second job inside C. E is a separate manual root, so E/F/G
forms another three-level chain rather than extending A/B/C past GitHub's chain
limit. D and G are detached from their key-bearing/provider operations; their
core verification is offline over retained bytes, although the jobs still use
Actions artifact transport and download a pinned verifier runtime and locked
dependencies.

## Safe initial state

All A/B/C and E/F/G entry jobs are fail-closed behind separate administrative
repository variables. Keep both `EVOGUARD_RELEASE_SOURCE_V2_ENABLED` and
`EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED` absent or `false` until their
external roots and protected Environments are audited.

The first admitted target must be a later **source-only, one-parent** main
commit. The baseline commit must already contain the judge pack, hash-locked
judge dependencies, and reviewed A/B/C workflow blobs. Do not attempt to admit
the bootstrap commit itself.

See:

- [`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md) for the ordered C0/C1 procedure.
- [`docs/SETTINGS.md`](docs/SETTINGS.md) for the complete external root set.
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) for guarantees and non-claims.
- [`docs/NEGATIVE_MATRIX.md`](docs/NEGATIVE_MATRIX.md) for required fail-closed exercises.
- [`docs/ROUND1_EVIDENCE.md`](docs/ROUND1_EVIDENCE.md) for the first live round, exact evidence, and unexecuted cases.
- [`docs/RELEASE_ARTIFACT_BOOTSTRAP.md`](docs/RELEASE_ARTIFACT_BOOTSTRAP.md) for the disabled E/F/G bootstrap and live-round order.
- [`trust/public/README.md`](trust/public/README.md) for key handling.

## Local validation

```bash
python -m pip install pytest PyYAML
actionlint -color
python -m pytest -q
```

CI pins actionlint v1.7.12 by its release-archive SHA-256. The local tests
validate YAML syntax, the deterministic pilot artifact builder, and static
workflow contracts. They do not claim that GitHub executed E/F/G or
that its second Environment, sixth key, fresh artifact attestation, or RAAE
result exists.
