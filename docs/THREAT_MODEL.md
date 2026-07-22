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

If a later E/F/G round succeeds, its separate positive claim is narrower:
protected F freshly verifies the GitHub Artifact Attestation for one exact,
bounded JSON artifact created by exact E from an already admitted source tree,
then signs an RAAE that binds the artifact bytes, nested RSAE, E/F workflow
identities, tool/provider pins, and six distinct public roots. G verifies those
retained bytes and bindings without an Environment, protected signing key, or
fresh provider call. The JSON artifact records the digest and size of
`calculator.py`; it is not a compiled binary, package, release, or proof of a
reproducible build.

## Candidate boundary

- A is the only stage that executes the candidate application.
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

## Release-artifact pilot boundaries

- E is a manual, no-secret root. It accepts only an exact successful C run on
  the still-current protected `main`, verifies the nested RSAE, checks out that
  exact commit, executes the reviewed `tools/build_release_artifact.py` helper,
  reads but never imports or executes `calculator.py`, creates one canonical
  JSON descriptor, and requests one-subject GitHub provenance.
- F's preflight has no Environment or secret. It authenticates exact E/current
  `main`, closes and snapshots the artifact inventory, binds E/F raw-Git blobs,
  and records the outer runtime/tool/provider settings plus six public-key IDs
  in reviewable controls before the protected job can start.
- Before any protected step references the private key, F requires the reviewed
  settings snapshot to equal the live repository variables, preserves those
  exact decoded Ed25519 public roots, freezes the controls and roots root-owned
  beneath `/run` behind a checked hash inventory, and uses snapshot values for
  the rest of the job.
- F's protected job rechecks the controls, raw-Git blobs, runtime and tool
  hashes, provider identity, and six-key separation. The live provider runs as
  a dedicated non-root identity that cannot read the root-owned sixth private
  key.
- G has no Environment, secret, trusted signing key, or attestation permission.
  Its read-only job token is used only for run metadata and artifact transport,
  never passed to the detached verifier or an attestation provider. Its
  negative test creates only an ephemeral unrelated key. It
  authenticates exact F/current `main`, externally binds E/F/G identities, and
  verifies the retained RAAE, artifact, nested RSAE, and provider receipt.
- A valid RAAE is evidence about one exact file and one exact verification
  event. It is not permission to publish or deploy that file.

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
- for E/F/G, the separately reviewed E/F/G workflow IDs/blobs, v4.2 runtime,
  outer Git/`gh` hashes, dedicated outer UID/GID, and custody of the sixth key.

## Explicit non-claims

The pilot does not prove:

- independent review when both GitHub accounts share one owner;
- source correctness, absence of vulnerabilities, complete test coverage, or
  freedom from malicious behavior outside the narrow calculator protocol;
- before a live E/F/G round, any artifact provenance at all; after a successful
  round, anything beyond GitHub workflow provenance for the one exact JSON
  descriptor—specifically not semantic correctness, reproducibility, safety,
  or authorization of a package, image, release, publication, or deployment;
- equivalence between the pilot JSON descriptor and a shippable product, or
  proof that two independent builders reproduce identical distributable bytes;
- immutability of GitHub settings outside the recorded audit;
- resistance to a compromised GitHub-hosted runner/control plane;
- production readiness, SLA, compliance certification, or commercial fitness.
