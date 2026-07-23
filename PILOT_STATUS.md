# Pilot status

Status: **Round 1 source-only admission and Round 2 Release Artifact
Admission V1 E/F/G completed; both chains are disabled and both Environment
signing secrets have been removed**.

Implemented and exercised:

- A: strong Docker black-box source re-verification using a prior byte-pinned runtime;
- B: canonical producer receipt plus GitHub Artifact Attestation;
- C: protected POSIX/root V2 sealer with a dedicated non-root provider identity;
- D: detached verification as a separate, non-Environment job inside C;
- E: no-secret manual builder that verified the retained RSAE, created one
  bounded canonical JSON descriptor, and requested one exact GitHub Artifact
  Attestation;
- F: no-secret `workflow_run` preflight followed by a separately protected
  Environment that freshly verified E and sealed one `.raae` with a sixth key;
- G: no-secret detached verification of the RAAE, artifact, nested RSAE, and
  retained provider evidence, including five byte/root/pin negative controls;
- read-only runtime/tool/pack pin probe;
- static workflow-contract and local behavior tests.

Round 1 is preserved in [`docs/ROUND1_EVIDENCE.md`](docs/ROUND1_EVIDENCE.md).
It binds the exact source commit, parent, trees, workflow IDs/blobs, runtime,
pack, tools, identities, public roots, A/B/C/D runs, evidence digests, live
negative cases, unexecuted cases, and post-round cleanup state.

Round 2 is preserved in
[`docs/ROUND2_EVIDENCE.md`](docs/ROUND2_EVIDENCE.md). Its observed positive
chain was E
[`29963621119/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963621119/attempts/1),
protected F
[`29963656590/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963656590/attempts/1),
and detached G
[`29963877837/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963877837/attempts/1).
F returned `SEALED/ALLOW`; G returned `VERIFIED/ALLOW` without live provider
re-verification; and all five retained-evidence mutations exercised by G returned
`REJECTED`.

Established for these two bounded rounds:

- protected repository and Environment configuration;
- exact workflow IDs, raw-Git blobs, executable hashes, pack, and runtime pins;
- five distinct predecessor public-key domains, the protected V2 key used by C,
  and a separate sixth artifact-admission key used by F;
- a Docker/network-none external-judge `PASS` in A;
- an attested canonical producer receipt in B;
- `SEALED/ALLOW` in protected C and `VERIFIED/ALLOW` in detached D;
- one attested 290-byte canonical JSON descriptor in E;
- `SEALED/ALLOW` in protected F and `VERIFIED/ALLOW` in detached G;
- the live and detached fail-closed cases recorded in the two evidence ledgers.

Not established:

- a distributable build, release, package, publication, or deployment
  authorization;
- the live matrix cases explicitly listed as unexecuted in the ledger;
- independent external review, production readiness, SLA, or certification.
- artifact-publication authorization or a reproducible-build result. The
  admitted artifact is a deterministic JSON descriptor of `calculator.py`,
  not a compiled or packaged product.

Current safe state:
`EVOGUARD_RELEASE_SOURCE_V2_ENABLED=false` and
`EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED=false`; the repository has no
Actions secrets; neither protected Environment retains its signing secret; and
all normal branch protections and required signatures remain enabled.
