from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "evidence" / "round2"
CHECKSUMS = EVIDENCE_ROOT / "SHA256SUMS"
LINE_RE = re.compile(r"([0-9a-f]{64})  ([0-9A-Za-z._/-]+)")
KEY_IDS = {
    "trusted-finalizer.pem": (
        "e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0"
    ),
    "artifact-admission-v1.pem": (
        "cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b"
    ),
    "artifact-digest-admission-v2.pem": (
        "de9519f8d6fa6aecd0d92a88f3d4a5cc217af2c48c1e36f739268fb2557cd556"
    ),
    "release-source-finalizer-v1.pem": (
        "37ed1d7c935b2f3228f0b43b0890ae16369c9ae81bf020f8261475b87c5f96b6"
    ),
    "release-source-admission-v2.pem": (
        "a8dd7df155e63cefb8f40f9444818954642472bfd05d1d35ac9df9d49d1e5bd5"
    ),
    "release-artifact-admission-v1.pem": (
        "922b93371335b17b9b37d127227c0125cb9c4f78bfaf1d2694ffb25f3c146b1b"
    ),
}


def test_round2_evidence_snapshot_is_complete_and_unchanged() -> None:
    entries: dict[str, str] = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        match = LINE_RE.fullmatch(line)
        assert match is not None, f"invalid SHA256SUMS line: {line!r}"
        digest, relative = match.groups()
        assert relative not in entries, f"duplicate SHA256SUMS path: {relative}"
        assert relative != "SHA256SUMS"
        entries[relative] = digest

    observed = {
        path.relative_to(EVIDENCE_ROOT).as_posix()
        for path in EVIDENCE_ROOT.rglob("*")
        if path.is_file() and path != CHECKSUMS
    }
    assert set(entries) == observed

    for relative, expected in entries.items():
        actual = hashlib.sha256((EVIDENCE_ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected, relative


def test_round2_evidence_snapshot_retains_the_bounded_chain() -> None:
    required = {
        "29963160927/evoguard-release-source-admission-v2-1/source-allow.rsae",
        "29963621119/evoguard-release-artifact-builder-1/release-artifact.json",
        "29963656590/evoguard-release-artifact-admission-v1-1/"
        "release-artifact-allow.raae",
        "29963877837/evoguard-release-artifact-admission-v1-verified-1/"
        "raae-detached-verification.json",
        "29963877837/evoguard-release-artifact-admission-v1-verified-1/"
        "raae-negative-results.txt",
        "attestations/"
        "sha256-5c4d7677d5aea8022c9e7c48789f4c7060fa4fef0daa77f93ec31b2f6a2db629.jsonl",
        "attestations/"
        "sha256-c2e573ad7556ec15db102e6e92c4197d2b413970e37f8d12f823ac4b7aefe64e.jsonl",
    }
    observed = {
        path.relative_to(EVIDENCE_ROOT).as_posix()
        for path in EVIDENCE_ROOT.rglob("*")
        if path.is_file()
    }
    assert required <= observed


def test_round2_public_roots_match_the_six_recorded_key_ids() -> None:
    observed: set[str] = set()
    for name, expected in KEY_IDS.items():
        lines = (EVIDENCE_ROOT / "public-keys" / name).read_text(
            encoding="ascii"
        ).splitlines()
        assert lines[0] == "-----BEGIN PUBLIC KEY-----"
        assert lines[-1] == "-----END PUBLIC KEY-----"
        der = base64.b64decode("".join(lines[1:-1]), validate=True)
        actual = hashlib.sha256(der).hexdigest()
        assert actual == expected
        observed.add(actual)
    assert len(observed) == 6
