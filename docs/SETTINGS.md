# External settings contract

Repository and Environment settings are mutable control-plane trust roots, not
Git objects. Keep an out-of-band change record for every value.

## Repository variables

| Variable | Contract |
| --- | --- |
| `EVOGUARD_RELEASE_SOURCE_V2_ENABLED` | Absent/`false` during C0; literal `true` only for an audited live round. |
| `EVOGUARD_BOOTSTRAP_RUNTIME_URL` | HTTPS immutable v4.1.0 asset URL. |
| `EVOGUARD_BOOTSTRAP_RUNTIME_SHA256` | Exact lowercase SHA-256 of the bootstrap bytes. |
| `EVOGUARD_RELEASE_SOURCE_PACK_SHA256` | `EVOGUARD_PACK_V2` digest reported by reviewed `pack-doctor`. |
| `EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_ID` | Numeric GitHub workflow ID for A. |
| `EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_ID` | Numeric GitHub workflow ID for B. |
| `EVOGUARD_RELEASE_SOURCE_ADMIT_WORKFLOW_ID` | Numeric GitHub workflow ID for C. |
| `EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_BLOB_SHA` | Raw-Git blob of A in the admitted source tree. |
| `EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_BLOB_SHA` | Raw-Git blob of B in the admitted source tree. |
| `EVOGUARD_RELEASE_SOURCE_ADMIT_WORKFLOW_BLOB_SHA` | Raw-Git blob of C in the admitted source tree. |
| `EVOGUARD_GIT_EXECUTABLE_SHA256` | Reviewed SHA-256 of the canonical Git executable on `ubuntu-24.04`. |
| `EVOGUARD_GH_EXECUTABLE_SHA256` | Reviewed SHA-256 of the canonical GitHub CLI executable on `ubuntu-24.04`. |
| `EVOGUARD_PROVIDER_ISOLATION_UID` | Dedicated non-root decimal UID; not `65534`. |
| `EVOGUARD_PROVIDER_ISOLATION_GID` | Dedicated non-root decimal GID; not `65534`. |
| `EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PUBLIC_KEY_B64` | Base64 PEM for the V2 source-admission public key. |
| `EVOGUARD_TRUSTED_FINALIZER_PUBLIC_KEY_B64` | Base64 PEM for the Trusted Finalizer public key. |
| `EVOGUARD_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64` | Base64 PEM for the Artifact Admission V1 public key. |
| `EVOGUARD_ARTIFACT_DIGEST_ADMISSION_V2_PUBLIC_KEY_B64` | Base64 PEM for the Artifact Digest Admission V2 public key. |
| `EVOGUARD_RELEASE_SOURCE_FINALIZER_V1_PUBLIC_KEY_B64` | Base64 PEM for the DENY-only Release Source Finalizer V1 public key. |

## Protected Environment secret

Environment: `evoguard-release-source-v2`

| Secret | Contract |
| --- | --- |
| `EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PRIVATE_KEY_B64` | Base64 PEM for the distinct V2 private key. It must match only the V2 public variable and never appear in repository variables, files, artifacts, logs, or D. |

The C job decodes the key into a root-owned `0600` file below a root-owned
`0700` directory. The sealer starts as UID 0, proves the dedicated provider UID
cannot read that path, drops only the GitHub CLI provider process, and reads the
key only after fresh provider verification and cleanup.

## Values that must never be workflow inputs

Do not expose runtime URL/SHA, workflow IDs/blobs, executable pins, provider
UID/GID, public roots, Environment name, or enable state as
`workflow_dispatch.inputs`. A candidate artifact, checkout, PR field, issue,
workflow output, or run name cannot select its own trust roots.
