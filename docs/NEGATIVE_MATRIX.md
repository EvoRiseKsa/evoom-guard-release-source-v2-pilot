# Required negative matrix

Run each case in a disposable branch/settings window. Preserve exact run IDs,
attempts, logs, and artifacts. Restore and re-audit settings after each test.

| Case | Mutation | Required result |
| --- | --- | --- |
| Disabled | Enable variable absent/false | A/B/C preflight does not run; no Environment or key use. |
| Wrong A ID | Change configured A workflow ID | B preflight fails before attestation. |
| Wrong A path/name collision | Trigger another same-name workflow | B rejects exact `run.path`/ID. |
| Wrong B ID/path | Change configured B workflow ID or use a same-name workflow | C preflight fails before Environment. |
| Moved main after A | Merge another commit before B | B rejects `context.sha`/current-main mismatch. |
| Moved main after B | Merge another commit before C | C preflight rejects before Environment. |
| Partial rerun | Re-run only a downstream job/attempt | artifact/run-attempt binding fails closed. |
| Altered A artifact | Replace/remove/add a downloaded evidence file | B's exact file-set, regular-file, size, byte, or raw-Git checks fail. |
| Altered B artifact | Replace/remove/add a receipt input | C snapshot or receipt/raw-Git/provider binding fails. |
| Wrong A/B/C blob | Change any configured blob SHA | B or C raw-Git binding fails. |
| Wrong runtime/pack | Change bootstrap or pack digest | A/B/C download or pack identity fails. |
| Wrong Git/`gh` pin | Change either executable SHA-256 | C fails before provider/key read. |
| Provider UID/GID `65534` | Set either to `65534` | C account/key step rejects. |
| Reused domain key | Reuse any public key in two domains | V2 sealer/verifier rejects key separation. |
| Wrong V2 public/private pair | Replace one side | C cannot seal a self-verifying envelope. |
| Failed provider attestation | Remove permission/token or use wrong policy | C rejects before signing. |
| Tampered `.rsae` | Change one retained bundle byte | D detached signature/canonical verification rejects. |
| Wrong detached V2 root | Give D a different Ed25519 public key | D rejects the envelope signature. |
| Wrong detached Git/`gh` pin | Change either expected executable digest | D rejects the signed runtime binding. |
| Wrong detached UID/GID | Change either expected provider identity | D rejects the signed isolation binding. |
| Wrong detached source/context | Mutate the expected target SHA in either document | D rejects the external binding. |
| Wrong detached bootstrap | Change the expected bootstrap digest | D rejects the signed runtime binding. |
| Wrong detached policy | Change the expected signer digest | D rejects the signed provider policy. |

A negative test is successful only when it fails at the expected boundary and
does not expose a private key, publish bytes, or produce a usable `ALLOW`.

## Release Artifact Admission V1 additions

These cases apply only after the disabled E/F/G scaffold is merged and the
separate roots in `RELEASE_ARTIFACT_BOOTSTRAP.md` are reviewed.

| Case | Mutation | Required result |
| --- | --- | --- |
| Artifact feature disabled | Keep the artifact enable variable absent/false | E/F/G protected work does not run; no artifact Environment or key use. |
| Wrong C run/attempt | Dispatch E with a different run or attempt | E rejects before checkout, build, or attestation. |
| Moved main before E | Advance `main` after C | E rejects the C/current-main binding. |
| Wrong E ID/path | Change E ID or trigger a name-collision workflow | F rejects before Environment access. |
| Moved main between E/F | Advance `main` after E | F rejects before Environment access. |
| Wrong E/F/G blob | Change any configured raw-Git blob | F or G rejects before a usable detached `ALLOW`. |
| Open E inventory | Add, remove, rename, symlink, or oversize an E output | F preflight rejects the closed snapshot. |
| Altered builder controls | Change the artifact/RSAE digest or source-run binding | F rejects before Environment access. |
| Wrong outer Git/`gh` pin | Change either outer executable SHA-256 | F rejects before the provider/key operation. |
| Outer UID/GID root or `65534` | Configure a forbidden identity | F rejects before signing. |
| Reused sixth key | Reuse any predecessor public key | F rejects the six-domain separation check. |
| Wrong sixth public/private pair | Replace one side | F cannot produce a self-verifying RAAE. |
| Failed E attestation verification | Remove permission/token or mismatch the E provenance | F rejects before RAAE signing. |
| Tampered artifact | Append or alter one artifact byte | G rejects. |
| Tampered `.raae` | Alter one retained envelope byte | G rejects. |
| Wrong sixth public root | Give G a different Ed25519 public key | G rejects the signature. |
| Wrong detached outer pin | Change the expected outer Git or `gh` digest | G rejects the signed runtime binding. |
| Wrong detached nested pin | Change a required RSAE runtime/tool/provider root | G rejects the nested source binding. |
| Moved main before G | Advance `main` after F | G rejects the F/current-main binding. |

The five built-in G controls cover tampered artifact, tampered envelope, wrong
sixth root, wrong outer Git pin, and wrong nested source `gh` pin. All other
rows remain live-round obligations and must not be described as executed until
their run evidence is preserved.
