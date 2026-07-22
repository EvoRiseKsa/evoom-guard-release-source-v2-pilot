# Pilot status

Status: **Round 1 source-only admission completed; disabled RAAE scaffold
implemented; no live artifact-admission round has started**.

Implemented and exercised:

- A: strong Docker black-box source re-verification using a prior byte-pinned runtime;
- B: canonical producer receipt plus GitHub Artifact Attestation;
- C: protected POSIX/root V2 sealer with a dedicated non-root provider identity;
- D: detached verification as a separate, non-Environment job inside C;
- read-only runtime/tool/pack pin probe;
- static workflow-contract and local behavior tests.

Implemented but not yet exercised live:

- E: no-secret manual builder that verifies a fresh RSAE, creates one bounded
  canonical data artifact, and requests one exact GitHub Artifact Attestation;
- F: no-secret `workflow_run` preflight followed by a separately protected
  Environment that freshly verifies E and seals one `.raae` with a sixth key;
- G: no-secret detached verification of the RAAE, artifact, nested RSAE, and
  retained provider evidence, including five byte/root/pin negative controls.

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

- a distributable build, release, package, publication, or deployment
  authorization;
- the live matrix cases explicitly listed as unexecuted in the ledger;
- independent external review, production readiness, SLA, or certification.
- any live E/F/G run, RAAE `ALLOW`, artifact-publication authorization, or
  reproducible-build result. The pilot artifact is a deterministic JSON
  descriptor of `calculator.py`, not a compiled or packaged product.

Current safe state: `EVOGUARD_RELEASE_SOURCE_V2_ENABLED=false`, the Environment
private-key secret is absent, and the temporary `main` lock is off while all
normal branch protections and required signatures remain enabled.
The RAAE feature must likewise remain `false`; its Environment and private key
must not be created until the disabled scaffold is merged and exact E/F/G
workflow IDs/blobs and v4.2.0 runtime/tool pins are reviewed.
