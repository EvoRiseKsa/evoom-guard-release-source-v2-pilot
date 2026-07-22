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
