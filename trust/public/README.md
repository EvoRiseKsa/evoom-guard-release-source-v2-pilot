# Public trust roots

No placeholder PEM is committed. A syntactically valid placeholder could be
mistaken for a trusted key, while an invalid placeholder would make bootstrap
automation ambiguous.

The six public PEM values are stored as separately audited base64 repository
variables listed in `docs/SETTINGS.md`. C decodes the five source-chain roots
into a root-owned trust directory; D decodes those roots independently. F and
G decode the same five predecessor roots plus the separate sixth RAAE root.
The source V2 and RAAE private keys may exist only during their respective live
windows as protected `evoguard-release-source-v2` and
`evoguard-release-artifact-v1` Environment secrets.

Before enabling either round, record the Ed25519 public-key IDs and prove all
six domains are distinct:

1. `trusted_finalizer`
2. `artifact_admission_v1`
3. `artifact_digest_admission_v2`
4. `release_source_finalizer_v1`
5. `release_source_admission_v2`
6. `release_artifact_admission_v1`

Do not commit private keys, generated key pairs, provider tokens, or live
evidence under this directory.
