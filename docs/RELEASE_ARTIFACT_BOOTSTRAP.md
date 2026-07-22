# Release Artifact Admission V1 pilot procedure

This procedure adds one live E/F/G round after the published immutable v4.2.0
bootstrap. It must not create a tag, release, Marketplace update, package,
deployment, or production gate.

## Why the previous RSAE cannot be reused

The preserved Round 1 RSAE admits source commit
`af8e4592ef5572acfe2ea295c435eed6a8e122fc`. That tree predates E and F.
Release Artifact Admission V1 resolves both workflow paths to raw Git blobs in
the admitted source tree, so the old RSAE must fail. The correct order is to
merge the disabled E/F/G scaffold, then admit a later source-only child that
already inherits those workflows.

## R0 — merge only an inert scaffold

1. Keep both enable variables `false` and keep both Environment secrets absent.
2. Merge E/F/G, the deterministic builder, contract tests, and this documentation
   through protected `main`.
3. Require `Pilot CI` on the exact merge commit.
4. Manually dispatch E once while the artifact feature remains disabled and
   confirm E is skipped. Confirm no F/G protected work, Environment approval,
   or key access occurs.
5. Read the numeric workflow IDs from GitHub and resolve exact blobs from the
   protected merge tree:

   ```bash
   git rev-parse main:.github/workflows/evoguard-build-release-artifact.yml
   git rev-parse main:.github/workflows/evoguard-admit-release-artifact.yml
   git rev-parse main:.github/workflows/evoguard-verify-release-artifact.yml
   ```

6. Record the six ID/blob values outside any candidate run, then set the
   corresponding repository variables while the feature remains disabled.

## R1 — establish v4.2 and outer tool roots

Set both source and artifact runtime URLs to:

```text
https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v4.2.0/evo-guard.pyz
```

Set their independently named SHA-256 variables to:

```text
789428de56c42808fadeed654fc3d9377d2456e15dadf53b8eb24e4287028c88
```

Then:

1. dispatch `EvoGuard Runtime Pin Probe` from protected `main`;
2. inspect both runtime descriptors, runner image, canonical Git/`gh` paths,
   hashes, and both proposed UID/GID identities;
3. set the historical RSAE Git/`gh`/UID/GID variables and the separately named
   outer RAAE variables only after review; and
4. never auto-copy a probe artifact into repository variables.

Values may be equal on one runner image, but the RSAE and RAAE names remain
separate because they represent different verification events.

## R2 — create the protected RAAE domain while disabled

1. Create Environment `evoguard-release-artifact-v1` restricted to protected
   branches, with `MANA-awam` as required reviewer, prevent self-review enabled,
   and no admin bypass. This is same-owner procedural separation, not
   independent review.
2. Generate a new Ed25519 key pair for
   `release-artifact-admission-v1`; do not reuse any predecessor key.
3. Compute the DER-SPKI SHA-256 IDs of the sixth public key and all five
   predecessor public keys. Require six distinct values.
4. Store only the sixth public PEM as the repository variable listed in
   `SETTINGS.md`. Keep the private PEM out of Git and out of the Environment
   until immediately before F is allowed to run.

## R3 — obtain a new RSAE over a tree containing E/F/G

The source Environment currently has no private secret. Restore the private key
matching the configured Release Source Admission V2 public root, or rotate that
public/private pair together and re-audit it. Never combine a new private key
with the old public variable.

1. Merge one benign **source-only** change to `calculator.py`. Do not modify
   workflows, tests, policies, packs, locks, or documentation in that commit.
2. Confirm it is a one-parent child of the reviewed scaffold and that its tree
   contains the pinned A/B/C/E/F/G blobs.
3. Temporarily lock `main` against additional changes.
4. Set `EVOGUARD_RELEASE_SOURCE_V2_ENABLED=true`, dispatch A, observe B, and
   inspect C's no-secret control artifact before Environment approval.
5. Approve C only when target/run/workflow/tool/provider/key values match the
   external record. Require `SEALED/ALLOW` and detached D `VERIFIED/ALLOW`.
6. Set the source flag back to `false` and delete the source private secret.

## R4 — execute E/F/G

1. Add the sixth private key only to `evoguard-release-artifact-v1`.
2. Set `EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED=true`.
3. Dispatch E on the still-locked protected `main`, supplying only the new C run
   ID and attempt.
4. Require E to verify the RSAE, build one deterministic JSON data file without
   importing `calculator.py`, and produce one GitHub Artifact Attestation subject.
5. Inspect F's no-secret controls: E/F IDs, paths, raw-Git blobs, run/attempt,
   target SHA, artifact/RSAE digests, outer tool pins, provider UID/GID, and six
   distinct public-key IDs.
6. Approve F. Require fresh provider verification and `SEALED/ALLOW`.
7. Require G `VERIFIED/ALLOW`, `live_provider_reverification=false`, and all five
   built-in detached negative controls to report `REJECTED`.

## R5 — additional live negatives and cleanup

Exercise the remaining cases in `NEGATIVE_MATRIX.md` one mutation at a time.
After each, restore and re-audit the external setting. A negative case succeeds
only when it stops before a usable `ALLOW` and does not expose a key.

Finally:

1. set both feature flags to `false`;
2. delete both Environment private secrets;
3. verify that repository secret count is zero and both Environments contain no
   retained secret;
4. preserve public, non-secret evidence bytes and exact run/attempt/digest facts
   in a separate protected PR; and
5. unlock `main` without weakening normal branch protection.

## Exact claim if the round succeeds

The round would establish only that protected F verified the exact source RSAE,
one exact E-built file, exact E/F protected workflow identities, and one fresh
GitHub Artifact Attestation before a sixth key signed the retained evidence, and
that G later verified those retained bytes without a live provider call. It
would not prove reproducibility, vulnerability absence, publication authority,
deployment safety, production readiness, or independent external review.
