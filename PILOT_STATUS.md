# Pilot status

Status: **Round 1 live source-only admission completed; pilot remains disabled**.

Implemented and exercised:

- A: strong Docker black-box source re-verification using a prior byte-pinned runtime;
- B: canonical producer receipt plus GitHub Artifact Attestation;
- C: protected POSIX/root V2 sealer with a dedicated non-root provider identity;
- D: detached verification as a separate, non-Environment job inside C;
- read-only runtime/tool/pack pin probe;
- static workflow-contract and local behavior tests.

Round 1 is preserved in [`docs/ROUND1_EVIDENCE.md`](docs/ROUND1_EVIDENCE.md).
It binds the exact source commit, parent, trees, workflow IDs/blobs, runtime,
pack, tools, identities, public roots, A/B/C/D runs, evidence digests, live
negative cases, unexecuted cases, and post-round cleanup state.

Established for this one source-only round:

- protected repository and Environment configuration;
- exact workflow IDs, raw-Git blobs, executable hashes, pack, and runtime pins;
- five distinct public-key domains and a protected V2 key during C;
- a Docker/network-none external-judge `PASS` in A;
- an attested canonical producer receipt in B;
- `SEALED/ALLOW` in protected C and `VERIFIED/ALLOW` in detached D;
- the live and detached fail-closed cases recorded in the evidence ledger.

Not established:

- artifact, release, package, publication, or deployment authorization;
- the live matrix cases explicitly listed as unexecuted in the ledger;
- independent external review, production readiness, SLA, or certification.

Current safe state: `EVOGUARD_RELEASE_SOURCE_V2_ENABLED=false`, the Environment
private-key secret is absent, and the temporary `main` lock is off while all
normal branch protections and required signatures remain enabled.
