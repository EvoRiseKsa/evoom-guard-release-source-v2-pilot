# Public trust roots

No placeholder PEM is committed. A syntactically valid placeholder could be
mistaken for a trusted key, while an invalid placeholder would make bootstrap
automation ambiguous.

The five public PEM values are stored as separately audited base64 repository
variables listed in `docs/SETTINGS.md`. C decodes them into a root-owned trust
directory; D decodes the same external roots independently. The V2 private key
exists only as a protected `evoguard-release-source-v2` Environment secret.

Before enabling the pilot, record the Ed25519 public-key IDs and prove all five
domains are distinct:

1. `trusted_finalizer`
2. `artifact_admission_v1`
3. `artifact_digest_admission_v2`
4. `release_source_finalizer_v1`
5. `release_source_admission_v2`

Do not commit private keys, generated key pairs, provider tokens, or live
evidence under this directory.
