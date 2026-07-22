# Threat model and exact claim

## Exact positive claim

A valid V2 `ALLOW` says that, under the externally configured repository,
source, A/B/C workflow, run-attempt, bootstrap, provider-policy, Git/`gh`,
UID/GID, and five public-key roots, protected C admitted the exact source and
exact B receipt after a fresh constrained GitHub Artifact Attestation
verification. D confirms the retained signed envelope against the same external
roots without making a fresh Artifact Attestation provider call. D still uses
GitHub Actions artifact transport and downloads its pinned verifier runtime and
hash-locked dependencies; it is detached from the key/provider boundary, not
offline.

## Candidate boundary

- A is the only stage that executes candidate source.
- A has no secret, OIDC, attestation write, Environment, or write-capable token.
- The judge pack and judge dependency lock come from the exact parent checkout,
  not the candidate checkout.
- The pack never imports candidate code. It invokes the candidate only through
  `$EVOGUARD_EXEC`.
- The candidate runs inside an exact Docker image digest with network `none`.
- A fails closed unless the final verdict is a Docker-isolated external-judge
  `PASS`.

## Producer and signer boundaries

- B never checks out or executes candidate source. It re-derives raw-Git
  bindings, creates one canonical receipt, and requests an attestation only for
  that file.
- C's first job has no Environment or secret. It rejects the wrong workflow,
  path, ID, repository, branch, run, attempt, conclusion, or moved main before
  the protected job can start.
- C binds the exact A/B/C raw-Git blobs and executable hashes.
- The protected job starts the sealer as root, while the provider runs as a
  dedicated non-root UID/GID with cleared supplementary groups.
- Only the V2 private key exists in C; D receives neither the Environment nor
  the key.

## Trust roots that remain

- GitHub's control plane, runner service, Artifact Attestation service, OIDC
  issuer, Actions artifact service, and Environment enforcement;
- repository administrators and the mutable settings listed in `SETTINGS.md`;
- the reviewed A/B/C workflow definitions and parent-owned judge pack/lock;
- the immutable prior EvoOM Guard runtime and its release provenance;
- exact Git, GitHub CLI, Python, Docker daemon, and pinned container image;
- correctness of EvoOM Guard's V2 implementation and Ed25519/cryptographic
  dependencies;
- custody and separation of all five key domains.

## Explicit non-claims

The pilot does not prove:

- independent review when both GitHub accounts share one owner;
- source correctness, absence of vulnerabilities, complete test coverage, or
  freedom from malicious behavior outside the narrow calculator protocol;
- provenance, reproducibility, safety, or authorization of an artifact,
  package, image, release, publication, or deployment;
- immutability of GitHub settings outside the recorded audit;
- resistance to a compromised GitHub-hosted runner/control plane;
- production readiness, SLA, compliance certification, or commercial fitness.
