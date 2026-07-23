# Round 2 source-to-artifact evidence ledger

This ledger records the first completed live
`EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1` pilot round. It distinguishes observed
evidence from claims that were not tested. All workflow times are UTC on
2026-07-22.

## Scope and target

The admitted target was the signed, one-parent, source-only merge from PR
[#10](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/pull/10).
Only `calculator.py` changed relative to its reviewed parent.

| Binding | Value |
| --- | --- |
| Target commit | `382a24774e2da7d1117f8969455816bd7b941af2` |
| Target tree | `5caede847e2cde175b3583d1b6bc3bef267a5d26` |
| Reviewed parent | `83500ec73ee309584c12c28d29fa754dba0ff7e1` |
| Parent tree | `6f3382b180881b444a96607f6e9348df9a39e9f8` |
| Bootstrap runtime | EvoOM Guard `v4.2.0` |
| Runtime SHA-256 | `789428de56c42808fadeed654fc3d9377d2456e15dadf53b8eb24e4287028c88` |
| Verifier-pack SHA-256 | `1069166cacc8e885bfe128b4767888f5fbdba66d53d881bd30fe2b55ff789e5b` |

The target and parent are GitHub-signed. The exact-target post-merge `Pilot CI`
run
[`29963055962`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963055962)
completed successfully.

## Frozen workflows

| Stage | Workflow ID | Raw-Git blob SHA |
| --- | --- | --- |
| A: source reverify | `317944578` | `d75fd929d96c4a6dc69655ee8de672a534236d7a` |
| B: source receipt | `317944577` | `82f312f8bb773f9c8e34f3255955095cf5d27556` |
| C with D: source admit | `317944575` | `0a1e8cb07c9782cf53df53dec9bfb00069f5eab3` |
| E: artifact build | `318448421` | `8827c2b67634964e87a5f2c38d04e32c13aced5f` |
| F: artifact admit | `318448420` | `0cb6964eac644a314cecff4ddf634eb363089b9b` |
| G: detached artifact verify | `318448423` | `d3f5635378af1fd421cece29b6c28d82096952ae` |

The Git and GitHub CLI executable hashes were respectively
`f54a87f6253aab09ed7b522bd78ddeab509105b1043076209d89127e55877a48`
and
`56b8bbbb27b066ecb33dbef9a256dc9d1314adaeff0908a752feba6c34053b40`.
The source provider used UID/GID `60001:60001`; the artifact provider used
`60002:60002`.

All six configured DER-SPKI key identities were distinct. The sixth,
release-artifact-admission identity was
`sha256:922b93371335b17b9b37d127227c0125cb9c4f78bfaf1d2694ffb25f3c146b1b`.
The five predecessor identities remain recorded in
[`ROUND1_EVIDENCE.md`](ROUND1_EVIDENCE.md).

## Observed positive chain

| Stage | Run and attempt | Observed result |
| --- | --- | --- |
| A | [`29963102103/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963102103/attempts/1) | `success`; Guard `PASS`; 2/2 judge-owned black-box tests; Docker isolation; network `none`; only `calculator.py` changed. |
| B | [`29963137344/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963137344/attempts/1) | `success`; one canonical producer receipt and one GitHub-hosted Artifact Attestation subject. |
| C and D | [`29963160927/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963160927/attempts/1) | `success`; protected C returned `SEALED/ALLOW`; detached D returned `VERIFIED/ALLOW`; 11/11 source mutations were rejected. |
| E | [`29963621119/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963621119/attempts/1) | `success`; verified the exact RSAE, built one canonical JSON data descriptor, and produced one GitHub-hosted attestation subject. |
| F | [`29963656590/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963656590/attempts/1) | `success`; protected F freshly verified E and returned `SEALED/ALLOW`. |
| G | [`29963877837/1`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29963877837/attempts/1) | `success`; returned `VERIFIED/ALLOW` with `live_provider_reverification=false`; 5/5 retained-evidence mutations were rejected. |

Both protected Environment approvals were performed by `MANA-awam`. That
account and `EvoRiseKsa` have the same owner, so the approvals demonstrate
procedural separation and GitHub enforcement, not independent external review.

## Exact retained objects

The source envelope was 35,410 bytes with SHA-256
`89df65f0d7cdb4fe477d8607957f5cc5985cf21e453640384a4284ba9d94ee24`.
Its Ed25519 signature was independently checked over its canonical manifest,
and its embedded verdict, handoff, and producer receipt matched the reviewed
controls byte for byte.

The E output is a 290-byte JSON descriptor, not a binary, package, container,
or published release. Its SHA-256 is
`c2e573ad7556ec15db102e6e92c4197d2b413970e37f8d12f823ac4b7aefe64e`.
It binds `calculator.py` at the target commit: 713 bytes and SHA-256
`5165e387688a25586918ce7689b2dec3950c96b3e939399160d2e756703ef1b0`.

The artifact envelope was 56,452 bytes with SHA-256
`b8891a032d6deb182dcd899798f60c06238ecba787bc542ef267d4f44598b3be`.
It contained exactly five deterministic, stored ZIP entries with the canonical
1980 timestamp. Its Ed25519 signature was independently checked over its
canonical manifest, and its embedded source envelope matched the source result
byte for byte.

| Evidence | SHA-256 |
| --- | --- |
| Source Guard verdict | `507ab966c2845b413a74c201decea8d6200c9d60e8b6e9cc597a3460acbc9e8e` |
| Source producer receipt | `5c4d7677d5aea8022c9e7c48789f4c7060fa4fef0daa77f93ec31b2f6a2db629` |
| Source controls manifest | `5601b0b638df01a16e0ce2572e742e0813545cf3c7ea740ee41b3659221d4c81` |
| Source seal result | `b88d17ce5f280e4e3c03747ac1f8a917e57b47389c40073ecfcbba5a1f238125` |
| Source detached verification | `92604b0f6e16340e5fab9cb7a0f35e0653224969d89d78978e1c00775721b547` |
| F controls manifest | `76f0d71006555a74e8baa47fb1677cf3351a2bc5a718c5973bef723234c7c696` |
| Artifact seal result | `7375d7f859c59b3f8c12aeee42dfae15a1d02c11d389a98abfb5d85401373012` |
| Artifact detached verification | `b27b02b08799a0ffe515b663a36d4b00627f5e254d7546afe1b41f2a1bb8b819` |
| Artifact negative results | `252e4168ee6aeb3901bbb520c0f3d4415b9ddb8a2931d63281c8b36d865aaa00` |

## Fail-closed observations during completion

The first G attempt,
[`29962322219`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29962322219),
failed before executing its mutation assertions because read-only retained files
were copied with read-only modes. PR
[#9](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/pull/9)
changed only the disposable negative fixtures to mode `0600` and added a
workflow-contract regression test. The later G run above passed all five
negative controls. The failed run is not counted as positive evidence.

After that harness fix, source run
[`29962871162`](https://github.com/EvoRiseKsa/evoom-guard-release-source-v2-pilot/actions/runs/29962871162)
correctly rejected the workflow-and-test change at the pre-execution reward-hack
gate. PR #10 then supplied a separate source-only child, which became the
admitted target. This is an observed fail-closed result, not a bypass of the
source policy.

G rejected these five retained-evidence mutations: changed artifact bytes,
changed RAAE bytes, a wrong sixth public root, a wrong outer Git digest, and a
wrong nested source GitHub CLI digest. D separately rejected all eleven source
mutations listed in the Round 1 matrix.

The remaining artifact rows in [`NEGATIVE_MATRIX.md`](NEGATIVE_MATRIX.md) were
not live-executed in this round and must not be described as observed.

## Post-round safe state

After G completed, both enable variables were set to `false`; the source and
artifact Environment secrets were deleted; the repository secret count was
zero; and the active GitHub CLI account was restored to `EvoRiseKsa`. The local
private keys remain outside the repository.

Protected `main` remained locked on the admitted target throughout A through G.
The required `contracts` check, one approval, Code Owner review, stale-review
dismissal, last-push approval, conversation resolution, linear history,
administrator enforcement, required signatures, and force-push/deletion bans
were enabled after the round. This evidence-only documentation commit occurs
after the admitted target and is not itself covered by that target's ALLOW.

## Durable public snapshot

The exact non-secret artifacts downloaded from A through G and the two public
GitHub/Sigstore attestation bundles are preserved under
[`evidence/round2/`](../evidence/round2/). Its `SHA256SUMS` covers every retained
file except itself and is enforced by the local/CI test suite. This avoids
depending on the finite retention window of the original Actions artifacts.

The durability copy does not add a new security claim or a new verification
event. It contains no private signing key, Actions secret, credential, or
customer data, and it remains subject to the exact limits below.

## Exact limit of the result

Round 2 establishes one live binding from one exact source RSAE to one exact
E-built JSON descriptor, one exact pair of E/F workflow identities, one fresh
GitHub Artifact Attestation, one sixth-key RAAE, and one later detached
verification over retained provider evidence without a fresh provider call.

It does **not** establish independent review, vulnerability absence, repeated
reproducibility, a general build system, package or image provenance, release
publication authority, deployment safety, production readiness, or permission
to use the result as a production admission gate.
