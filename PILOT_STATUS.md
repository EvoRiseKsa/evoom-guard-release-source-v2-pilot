# Pilot status

Status: **local scaffold; no live admission evidence**.

Implemented in the scaffold:

- A: strong Docker black-box source re-verification using a prior byte-pinned runtime;
- B: canonical producer receipt plus GitHub Artifact Attestation;
- C: protected POSIX/root V2 sealer with a dedicated non-root provider identity;
- D: detached verification as a separate, non-Environment job inside C;
- read-only runtime/tool/pack pin probe;
- static workflow-contract and local behavior tests.

Not established until a live round is completed and preserved:

- repository/ruleset/Environment configuration;
- exact workflow IDs and raw-Git blob pins;
- five genuinely distinct public-key domains and protected V2 private key;
- exact Git and GitHub CLI executable pins on `ubuntu-24.04`;
- positive A/B/C/D run evidence;
- negative matrix evidence;
- artifact, release, package, publication, or deployment authorization;
- independent review or production readiness.
