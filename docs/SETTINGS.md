# External settings contract

Repository and Environment settings are mutable control-plane trust roots, not
Git objects. Keep an out-of-band change record for every value.

## Repository variables

| Variable | Contract |
| --- | --- |
| `EVOGUARD_RELEASE_SOURCE_V2_ENABLED` | Absent/`false` during C0; literal `true` only for an audited live round. |
| `EVOGUARD_BOOTSTRAP_RUNTIME_URL` | HTTPS immutable v4.2.0 asset URL for the new source round. |
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

### Release Artifact Admission V1 variables

These are a separate outer trust domain. Do not alias them to the historical
RSAE tool/provider settings merely because one probe reports equal bytes.

| Variable | Contract |
| --- | --- |
| `EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED` | Absent/`false` through scaffold review; literal `true` only during an audited E/F/G round. |
| `EVOGUARD_RELEASE_ARTIFACT_RUNTIME_URL` | Exact immutable v4.2.0 `evo-guard.pyz` asset URL used by E/F/G. |
| `EVOGUARD_RELEASE_ARTIFACT_RUNTIME_SHA256` | `789428de56c42808fadeed654fc3d9377d2456e15dadf53b8eb24e4287028c88`. |
| `EVOGUARD_RELEASE_ARTIFACT_BUILD_WORKFLOW_ID` | Numeric GitHub workflow ID for E. |
| `EVOGUARD_RELEASE_ARTIFACT_ADMIT_WORKFLOW_ID` | Numeric GitHub workflow ID for F. |
| `EVOGUARD_RELEASE_ARTIFACT_VERIFY_WORKFLOW_ID` | Numeric GitHub workflow ID for G. |
| `EVOGUARD_RELEASE_ARTIFACT_BUILD_WORKFLOW_BLOB_SHA` | Raw-Git E blob in the newly admitted source tree. |
| `EVOGUARD_RELEASE_ARTIFACT_ADMIT_WORKFLOW_BLOB_SHA` | Raw-Git F blob in the newly admitted source tree. |
| `EVOGUARD_RELEASE_ARTIFACT_VERIFY_WORKFLOW_BLOB_SHA` | Raw-Git G blob in the newly admitted source tree. |
| `EVOGUARD_RELEASE_ARTIFACT_GIT_EXECUTABLE_SHA256` | Independently reviewed outer Git executable SHA-256 used by F. |
| `EVOGUARD_RELEASE_ARTIFACT_GH_EXECUTABLE_SHA256` | Independently reviewed outer GitHub CLI SHA-256 used by F. |
| `EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_UID` | Dedicated non-root outer provider UID; not `0` or `65534`. |
| `EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_GID` | Dedicated non-root outer provider GID; not `0` or `65534`. |
| `EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64` | Base64 PEM for the sixth, mutually distinct RAAE public key. |

## Protected Environment secret

Environment: `evoguard-release-source-v2`

| Secret | Contract |
| --- | --- |
| `EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PRIVATE_KEY_B64` | Base64 PEM for the distinct V2 private key. It must match only the V2 public variable and never appear in repository variables, files, artifacts, logs, or D. |

The C job decodes the key into a root-owned `0600` file below a root-owned
`0700` directory. The sealer starts as UID 0, proves the dedicated provider UID
cannot read that path, drops only the GitHub CLI provider process, and reads the
key only after fresh provider verification and cleanup.

Environment: `evoguard-release-artifact-v1`

| Secret | Contract |
| --- | --- |
| `EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PRIVATE_KEY_B64` | Base64 PEM for the sixth RAAE key. It must differ from all five predecessor domains, exist only during the live F window, and never enter repository variables, E/G, artifacts, logs, or Git. |

The F job applies the same root-owned `0600`/provider-unreadable pattern in a
separate Environment. The E and G jobs never request either Environment.

## Values that must never be workflow inputs

Do not expose runtime URL/SHA, workflow IDs/blobs, executable pins, provider
UID/GID, public roots, Environment name, or enable state as
`workflow_dispatch.inputs`. E may accept only the exact protected C run ID and
attempt used to retrieve the RSAE; those values select evidence, not trust
roots. A candidate artifact, checkout, PR field, issue, workflow output, or run
name cannot select its own roots.
