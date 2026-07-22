# Round 1 evidence ledger

This ledger records the first live, source-only
`EVOGUARD_RELEASE_SOURCE_ADMISSION_V2` pilot round. It separates observed
evidence from tests that were not performed. All times are UTC on 2026-07-22.

## Scope and target

The admitted target was the one-parent, source-only merge from PR
[#2](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/pull/2).
Only `calculator.py` changed.

| Binding | Value |
| --- | --- |
| Target commit | `af8e4592ef5572acfe2ea295c435eed6a8e122fc` |
| Target tree | `4172083ab3b38c8d5793b69da422485294d1e9ae` |
| Reviewed C1 parent | `20f387e03aaed7c501ca837c2a8cc933ace838ef` |
| Parent tree | `e42eeeeabac2642dd0fd253cb437f60bdcab186a` |
| Bootstrap runtime | EvoOM Guard `v4.1.0` |
| Runtime SHA-256 | `d5ce7dbefa870307d6fe49ddec1e9847cad89d15f6afe2b74f4e7b8953fc62b2` |
| Verifier-pack SHA-256 | `1069166cacc8e885bfe128b4767888f5fbdba66d53d881bd30fe2b55ff789e5b` |

Both `main` commits were created by GitHub and have a valid GitHub signature.
Required-signature enforcement was temporarily disabled during the two merges
because the reviewed feature-branch commits were unsigned, then restored after
GitHub created each signed squash commit. This ledger does not claim that the
setting remained continuously enabled during bootstrap.
The C2 post-merge `Pilot CI` run
[`29896878968`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29896878968)
completed successfully on the exact target SHA.

## Frozen live inputs

The three active workflow IDs and raw-Git blobs were:

| Stage | Workflow ID | Blob SHA |
| --- | --- | --- |
| A: reverify | `317944578` | `d75fd929d96c4a6dc69655ee8de672a534236d7a` |
| B: receipt | `317944577` | `82f312f8bb773f9c8e34f3255955095cf5d27556` |
| C with D: admit | `317944575` | `0a1e8cb07c9782cf53df53dec9bfb00069f5eab3` |

Two runtime-probe runs,
[`29896329971`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29896329971)
and
[`29896366700`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29896366700),
reported the same GitHub-hosted `ubuntu24` image inputs: Python `3.12.13`,
Git `2.54.0` at `/usr/bin/git`, GitHub CLI `2.96.0` at `/usr/bin/gh`,
provider UID/GID `60001:60001`, and these executable hashes:

- Git: `f54a87f6253aab09ed7b522bd78ddeab509105b1043076209d89127e55877a48`
- GitHub CLI: `56b8bbbb27b066ecb33dbef9a256dc9d1314adaeff0908a752feba6c34053b40`

The five configured DER-SPKI key identities were distinct:

| Domain | Key identity |
| --- | --- |
| Artifact admission V1 | `sha256:cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b` |
| Artifact-digest admission V2 | `sha256:de9519f8d6fa6aecd0d92a88f3d4a5cc217af2c48c1e36f739268fb2557cd556` |
| Release-source admission V2 | `sha256:a8dd7df155e63cefb8f40f9444818954642472bfd05d1d35ac9df9d49d1e5bd5` |
| Release-source finalizer V1 | `sha256:37ed1d7c935b2f3228f0b43b0890ae16369c9ae81bf020f8261475b87c5f96b6` |
| Trusted finalizer | `sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0` |

## Positive chain

| Stage | Run and attempt | Observed result |
| --- | --- | --- |
| A | [`29896945747/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29896945747/attempts/1) | `success`; Guard `PASS`; 2/2 judge-owned black-box tests; Docker candidate isolation; network `none`; external-process-isolated report integrity. |
| B | [`29896982146/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29896982146/attempts/1) | `success`; canonical producer receipt created and attested. |
| C and D | [`29897001564/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897001564/attempts/1) | `success`; protected C returned `SEALED/ALLOW`; detached D returned `VERIFIED/ALLOW`. |

GitHub Artifact Attestation verification independently matched the B subject
`producer-receipt.json`, its exact SHA-256, workflow B, GitHub-hosted runner,
target source SHA, and run `29896982146/1`. The protected Environment deployment
was `5550877736`. It required approval by `MANA-awam`; that account and
`EvoRiseKsa` have the same owner, so this is procedural separation, not an
independent external review.

The final retained envelope was 35,222 bytes with SHA-256
`99b1fb6252321466a14507903f6ec39eaa59ae0e9500a57e669a81a447983c6a`.
It was also verified locally with the published, byte-pinned EvoOM Guard
`v4.1.0` runtime and the five audited public roots, producing
`VERIFIED/ALLOW`.

### Evidence digests

| Evidence | SHA-256 |
| --- | --- |
| Guard verdict | `1ac6826b1a9f1efd8f96322ea4c8a3e1e3722bc6340d4b335f3c53a2d741664c` |
| Source document | `ae4c1552269008b5a39f59a39068b3612f7e85454afc7df7d61fb62d76e7e0f0` |
| Handoff | `5fab04aa7a20243f60054c007394696c6e6dbd2619558678c7c5794e2f167584` |
| Context | `539208cdfbc07361074a62350a43ac8e2ebfcb1ce1a274ea81cad98e45fee24b` |
| Producer input | `00259917da31ffd2e5c346fb81f0a4a345d114900354c50410ccc5e2dc308acd` |
| Producer receipt | `5b5f769bdc3484e4f9524fb1af82b62e9ff9716cfa7beb2dad6af9c6f114f567` |
| Admitter input | `d6684d445e3e9cb92044a9bab90154e5cc113db40180ddb20c8c153742bc6f31` |
| GitHub policy | `3e73512a5eed356c983a80f1fbee9b814eb9edd026b8898dbcc6aa7c40ee64c8` |
| Signing requirements | `583b7e20db33f932684c9e9fe8e94ec796a04decfc66884a6463cc73c35bef11` |
| Controls manifest | `b23430e325f6076b80d4d36a0c60238761b6118ad46f8711a6e9cc0fdf5177cb` |
| Seal result | `95312b77d7791c812e223f5d5f5bb6f7afca22e95940eccbc8594fa5337daa12` |
| Detached verification | `691a612a594fbd69aec7c792187e5f43f1c71cbf549c7209e627ad44ff3dd574` |
| Detached-negative results | `df2c9edb06a1017474d91b7cc8db8eef4ea31db22b3c31c2879b757a7e676ba0` |

## Live fail-closed exercises

Each settings mutation was restored before the next case. No case below
produced a usable V2 `ALLOW`.

| Case | Decisive observed run | Result |
| --- | --- | --- |
| Feature disabled | A [`29897350842`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897350842), B [`29897354697`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897354697), C [`29897365549`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897365549) | All skipped; no new Environment deployment. |
| Wrong A workflow ID | B [`29897492077`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897492077) | Failed in B preflight before attestation. |
| Wrong B workflow ID | C [`29897613851`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897613851) | Failed before Environment. |
| Wrong A blob | B [`29897700526`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897700526) | Failed raw-Git binding. |
| Wrong B blob | B [`29897799614`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897799614) | Failed B self/raw-Git binding. |
| Wrong C blob | C [`29897919864`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897919864) | Failed before Environment. |
| Wrong runtime digest | A [`29897959241`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29897959241) | Failed download/pin before Guard execution. |
| Wrong verifier-pack digest | A [`29898045803`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29898045803) | Failed strong black-box re-verification. |
| Reused public-key domain | C [`29898196694`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29898196694) | Failed before signing. |
| Wrong V2 public/private pair | C [`29898529995`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29898529995) | Failed in protected C; no self-verifying envelope. |
| Wrong Git executable digest | C [`29898737014`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29898737014) | Failed canonical external-controls preflight before Environment. |
| Provider UID `65534` | C [`29898871508`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29898871508) | Failed canonical external-controls preflight before Environment. |
| Partial A rerun | A [`29896945747/2`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29896945747/attempts/2), B [`29899000636`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29899000636), C [`29899009097`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29899009097) | A attempt 2 failed its exact source-control input; downstream B failed and C skipped. The positive chain remains explicitly bound to A attempt 1. |

One earlier wrong-key-pair setup run was cancelled and is intentionally excluded
from the evidence claim; the clean repeated case above is the recorded result.

## Detached D mutation exercises

Within the successful C run, D independently rejected all eleven automated
mutations: a changed envelope byte, wrong V2 root, wrong Git digest, wrong
GitHub CLI digest, wrong provider UID, wrong provider GID, mutated source,
mutated context, wrong bootstrap digest, mutated signer policy, and mutated
producer input.

## Not live-executed

The following matrix entries are not claimed as live evidence:

- an A path/name-collision workflow;
- moving protected `main` between A and B or between B and C;
- replacing an already uploaded immutable A or B GitHub artifact;
- removing the provider attestation permission/token;
- wrong GitHub CLI digest in protected C (the equivalent Git preflight was
  exercised live, and D exercised the GitHub CLI mutation);
- provider GID `65534` in protected C (UID was exercised live, and D exercised
  both UID and GID).

The first four require a separate, deliberately destructive or protected-
workflow/settings exercise. Static contracts and fail-closed checks exist for
them, but that is not live proof.

## Post-round safe state

After the matrix, all pinned variables were restored and independently read
back. At `2026-07-22T07:16:12Z`,
`EVOGUARD_RELEASE_SOURCE_V2_ENABLED=false`; there were no active runs;
the protected Environment secret was deleted; the local private key remains
outside the repository; and the temporary `main` operational lock was removed.
The required `contracts` check, one approving review, Code Owner review, stale
review dismissal, last-push approval, conversation resolution, linear history,
administrator enforcement, required signatures, and force-push/deletion bans
remain enabled.

## Exact limit of the result

Round 1 establishes one successful live execution of the narrow source-
admission claim in [`THREAT_MODEL.md`](THREAT_MODEL.md), plus the recorded
fail-closed observations above. It does **not** authorize or establish the
provenance, reproducibility, safety, or publication of an artifact, package,
image, release, deployment, or production service. It is not an independent
security audit or a production-readiness certification.
