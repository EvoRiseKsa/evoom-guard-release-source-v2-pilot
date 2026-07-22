# C0, C1, and live-round bootstrap procedure

Follow the order exactly. A value observed from a workflow artifact becomes a
trust root only after an administrator reviews and records it outside the
candidate run.

## C0 — publish only the inert fixture and CI baseline

1. Create the repository with default branch `main`. Stage only the inert
   calculator baseline: repository metadata, `.evoguard.json`, `LICENSE`,
   `CODEOWNERS`, `Pilot CI`, `calculator.py`, the two judge-pack source files,
   the judge/development locks, and `tests/test_calculator.py`. Do **not** stage
   A/B/C, the runtime-pin-probe workflow/tool, `tests/test_runtime_pin_probe.py`,
   or `tests/test_workflow_contracts.py` in the first push.
2. Keep `EVOGUARD_RELEASE_SOURCE_V2_ENABLED` absent or set to `false`.
3. Add a ruleset that protects `main`, requires pull requests and `Pilot CI`,
   prevents force pushes/deletion, and uses squash or rebase so the target
   admitted commit has exactly one parent.
4. Confirm no private key, PEM private material, token, or generated evidence is
   committed. The `.gitignore` rejects the common local forms but is not a
   secret scanner.
5. Confirm `Pilot CI` passes on the exact C0 commit.

## C1 — add the disabled trust workflows through review

1. Open a PR that adds A, B, C/D, the runtime-pin-probe workflow/tool, its test,
   the workflow contract tests, the signing lock, trust docs, and operations
   docs. Keep the enable variable false.
2. Review and merge that PR. Confirm `Pilot CI` passes on the exact C1 commit.
3. Create the Environment `evoguard-release-source-v2`, restrict it to `main`,
   and configure required reviewers if the plan supports them. Do not add the
   private key secret yet.
4. Set only the reviewed bootstrap URL/SHA and the proposed dedicated provider
   UID/GID variables. The currently planned UID/GID is `60001`/`60001`.

The intended prior runtime is the immutable v4.1.0 release asset:

```text
URL:    https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v4.1.0/evo-guard.pyz
SHA256: d5ce7dbefa870307d6fe49ddec1e9847cad89d15f6afe2b74f4e7b8953fc62b2
```

Verify its GitHub release/build attestations separately. A URL and SHA alone do
not establish provenance.

## C1 — observe immutable runner inputs

1. Set only `EVOGUARD_BOOTSTRAP_RUNTIME_URL` and
   `EVOGUARD_BOOTSTRAP_RUNTIME_SHA256` to the reviewed values above.
2. Manually dispatch `EvoGuard Runtime Pin Probe` on the exact protected C1
   commit.
3. Download `runtime-pin-probe.json` and `pack-doctor.json`.
4. Confirm `runner.environment == "github-hosted"`, inspect the runner image,
   and independently compare the reported executable paths and hashes.
5. Record the reviewed Git SHA-256 as `EVOGUARD_GIT_EXECUTABLE_SHA256`, the
   GitHub CLI SHA-256 as `EVOGUARD_GH_EXECUTABLE_SHA256`, and the pack digest as
   `EVOGUARD_RELEASE_SOURCE_PACK_SHA256`.

Runner binaries can change. A mismatch must stop C until a new probe is
reviewed; never auto-update these variables from probe output.

The probe must run on a clean checkout. Do not compute the
`EVOGUARD_PACK_V2` digest from a working directory containing `__pycache__`,
coverage output, or other generated files. The probe never updates a variable.
The probe fails unless the pack directory contains exactly `pack.json` and
`test_calculator_protocol.py`. With those reviewed LF-normalized bytes, the
published v4.1.0 runtime reports
`1069166cacc8e885bfe128b4767888f5fbdba66d53d881bd30fe2b55ff789e5b`;
any other digest is a stop condition, not a value to copy into settings.

## C1 — bind workflows and keys

1. Read A/B/C numeric workflow IDs from GitHub's Actions API after all three
   workflow files exist on the C1 `main` commit.
2. Resolve the three exact blobs from the protected C1 Git tree, for example:

   ```bash
   git rev-parse main:.github/workflows/evoguard-release-source-reverify.yml
   git rev-parse main:.github/workflows/evoguard-produce-release-source-receipt.yml
   git rev-parse main:.github/workflows/evoguard-admit-release-source.yml
   ```

3. Set the corresponding ID/blob variables listed in `SETTINGS.md`.
4. Generate five separate Ed25519 key pairs for the five named domains. Never
   derive one key from another and never reuse an older domain's key.
5. Store the five base64-encoded public keys as repository variables. Compare
   their key IDs out of band and prove all five are distinct.
6. Set a dedicated unused non-root UID/GID in
   `EVOGUARD_PROVIDER_ISOLATION_UID`/`EVOGUARD_PROVIDER_ISOLATION_GID`,
   currently planned as `60001`/`60001`. Do not
   use `nobody`/`65534` or a UID reused by another service.
7. Audit all values while the enable variable remains false.
8. Only after the probe, workflow ID/blob anchors, public-key IDs, Environment
   restrictions, and required reviewer are audited, store the V2 private key as
   the Environment secret
   `EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PRIVATE_KEY_B64`.

## Live round — one source-only target after C1

1. Set `EVOGUARD_RELEASE_SOURCE_V2_ENABLED=true` only after the complete C0
   audit.
2. Create and merge one benign **source-only** change to `calculator.py`. Do not
   change workflows, the pack, locks, trust docs, or settings in that commit.
3. Confirm the new main commit has exactly one parent and that its parent is the
   reviewed C1 workflow baseline.
4. Dispatch A on protected `main`.
5. Observe B and C starting automatically. C's no-secret `preflight` publishes
   `evoguard-release-source-v2-controls-<attempt>`. Before approving the
   Environment, the required reviewer must compare the exact C target SHA,
   workflow ID/blob, B run ID/attempt, tool pins, provider UID/GID, and five
   public-key IDs in `control-manifest.json` to the out-of-band audit record.
   A reviewer account controlled by the same owner is procedural separation,
   not independent security review.
6. Require all four results:
   - A strong `PASS` with `candidate_isolation=docker`, `network=none`,
     `report_integrity=external_process_isolated`, and
     `overall_profile=black_box_external_judge`;
   - B successful GitHub Artifact Attestation for the exact producer receipt;
   - C `SEALED` / `ALLOW`;
   - D `VERIFIED` / `ALLOW` without Environment, private key, or a fresh
     Artifact Attestation provider call. D is detached, not offline.
7. Preserve run IDs/attempts, commit/tree, workflow IDs/blobs, tool/runtime/pack
   hashes, public key IDs, artifacts, attestation, and negative-test results.

Do not connect the result to a release, package, deployment, or customer gate.
That requires a separate artifact/publication boundary.
