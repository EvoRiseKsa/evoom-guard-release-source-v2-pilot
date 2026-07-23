# Round 2 durable evidence snapshot

This directory preserves the exact non-secret artifacts downloaded from the
six successful A-through-G workflow runs recorded in
[`docs/ROUND2_EVIDENCE.md`](../../docs/ROUND2_EVIDENCE.md):

| Stage | Run |
| --- | --- |
| A | `29963102103/1` |
| B | `29963137344/1` |
| C and D | `29963160927/1` |
| E | `29963621119/1` |
| F | `29963656590/1` |
| G | `29963877837/1` |

Each numeric directory retains the original Actions artifact directory and file
names. `attestations/` contains the two public Sigstore bundles freshly
downloaded with `gh attestation download` for the B producer receipt and the E
JSON descriptor. `public-keys/` freezes the six public Ed25519 roots required
to verify the nested RSAE and RAAE without depending on mutable repository
variables. `SHA256SUMS` covers every retained file except itself, and the
repository test suite rejects missing, extra, renamed, or changed bytes.

| Public-key domain | Key ID |
| --- | --- |
| `trusted_finalizer` | `sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0` |
| `artifact_admission_v1` | `sha256:cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b` |
| `artifact_digest_admission_v2` | `sha256:de9519f8d6fa6aecd0d92a88f3d4a5cc217af2c48c1e36f739268fb2557cd556` |
| `release_source_finalizer_v1` | `sha256:37ed1d7c935b2f3228f0b43b0890ae16369c9ae81bf020f8261475b87c5f96b6` |
| `release_source_admission_v2` | `sha256:a8dd7df155e63cefb8f40f9444818954642472bfd05d1d35ac9df9d49d1e5bd5` |
| `release_artifact_admission_v1` | `sha256:922b93371335b17b9b37d127227c0125cb9c4f78bfaf1d2694ffb25f3c146b1b` |

The snapshot was downloaded and checked on 2026-07-23. The RSAE and RAAE ZIP
members were inspected for private-key or token material before commit. No
signing key, Actions secret, credential, or customer data is included. The
repository and both protected Environments also had zero Actions secrets after
the round.

## Verification

From the repository root, first verify that the committed inventory and all six
public-key IDs are unchanged:

```bash
python -m pytest -q tests/test_round2_evidence_snapshot.py
```

For a semantic replay on POSIX, download the immutable v4.2.0 runtime, verify
its published digest, then invoke the same detached verifier contract used by G:

```bash
mkdir -p scratch/v4.2.0
gh release download v4.2.0 \
  --repo EvoRiseKsa/EvoOM-Guard-m \
  --pattern evo-guard.pyz \
  --dir scratch/v4.2.0
printf '%s  %s\n' \
  789428de56c42808fadeed654fc3d9377d2456e15dadf53b8eb24e4287028c88 \
  scratch/v4.2.0/evo-guard.pyz | sha256sum --check --strict

EVIDENCE=evidence/round2
F_ADMISSION="$EVIDENCE/29963656590/evoguard-release-artifact-admission-v1-1"
F_CONTROLS="$EVIDENCE/29963656590/evoguard-release-artifact-v1-controls-1"
KEYS="$EVIDENCE/public-keys"

python -I scratch/v4.2.0/evo-guard.pyz \
  verify-github-release-artifact-admission \
  "$F_ADMISSION/release-artifact-allow.raae" \
  "$F_ADMISSION/release-artifact.json" \
  --trusted-pub "$KEYS/release-artifact-admission-v1.pem" \
  --expected-builder "$F_CONTROLS/builder.json" \
  --expected-admitter "$F_CONTROLS/admitter.json" \
  --expected-release-source "$F_CONTROLS/source.json" \
  --expected-release-source-context "$F_CONTROLS/context.json" \
  --expected-release-source-producer "$F_CONTROLS/producer.json" \
  --expected-release-source-admitter "$F_CONTROLS/source-admitter.json" \
  --expected-release-source-bootstrap-guard-sha \
    789428de56c42808fadeed654fc3d9377d2456e15dadf53b8eb24e4287028c88 \
  --expected-release-source-github-policy \
    "$F_CONTROLS/source-github-policy.json" \
  --expected-release-source-git-executable-sha256 \
    f54a87f6253aab09ed7b522bd78ddeab509105b1043076209d89127e55877a48 \
  --expected-release-source-gh-executable-sha256 \
    56b8bbbb27b066ecb33dbef9a256dc9d1314adaeff0908a752feba6c34053b40 \
  --expected-release-source-provider-isolation-uid 60001 \
  --expected-release-source-provider-isolation-gid 60001 \
  --expected-git-executable-sha256 \
    f54a87f6253aab09ed7b522bd78ddeab509105b1043076209d89127e55877a48 \
  --expected-gh-executable-sha256 \
    56b8bbbb27b066ecb33dbef9a256dc9d1314adaeff0908a752feba6c34053b40 \
  --expected-provider-isolation-uid 60002 \
  --expected-provider-isolation-gid 60002 \
  --trusted-finalizer-pub "$KEYS/trusted-finalizer.pem" \
  --artifact-admission-v1-pub "$KEYS/artifact-admission-v1.pem" \
  --artifact-digest-admission-v2-pub \
    "$KEYS/artifact-digest-admission-v2.pem" \
  --release-source-finalizer-v1-pub \
    "$KEYS/release-source-finalizer-v1.pem" \
  --release-source-admission-v2-pub \
    "$KEYS/release-source-admission-v2.pem"
```

The expected result is exit code zero with `status=VERIFIED`,
`decision=ALLOW`, and `live_provider_reverification=false`. This replay checks
the retained evidence; it does not contact the attestation provider again.

This is a durability copy because the original Actions artifacts have retention
deadlines. It does not enlarge the result: the admitted object is one 290-byte
JSON descriptor, not a package, binary, image, published release, or deployed
runtime. The snapshot is same-owner evidence, not independent review,
reproducibility evidence, publication/deployment authorization, or a production
gate.
