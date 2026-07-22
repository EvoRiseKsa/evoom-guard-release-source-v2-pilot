from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tools.runtime_pin_probe import build_report, provider_identity, sha256


def test_sha256(tmp_path: Path) -> None:
    sample = tmp_path / "sample"
    sample.write_bytes(b"pinned\n")
    assert sha256(sample) == hashlib.sha256(b"pinned\n").hexdigest()


def test_probe_rejects_wrong_bootstrap_digest(tmp_path: Path) -> None:
    sample = tmp_path / "runtime.pyz"
    sample.write_bytes(b"runtime")
    with pytest.raises(SystemExit, match="does not match"):
        build_report(sample, "0" * 64)


def test_probe_keeps_release_artifact_runtime_as_a_separate_pin(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.pyz"
    artifact = tmp_path / "artifact.pyz"
    source.write_bytes(b"source-runtime")
    artifact.write_bytes(b"artifact-runtime")
    report = build_report(
        source,
        sha256(source),
        release_artifact_bootstrap=artifact,
        expected_release_artifact_bootstrap_sha256=sha256(artifact),
    )
    assert report["format"] == "EVOGUARD_RUNTIME_PIN_PROBE_V2"
    assert report["bootstrap"] == {
        "path": str(source.resolve()),
        "sha256": sha256(source),
    }
    assert report["release_artifact_bootstrap"] == {
        "path": str(artifact.resolve()),
        "sha256": sha256(artifact),
    }


@pytest.mark.parametrize(("uid", "gid"), [(0, 60001), (60001, 0), (65534, 60001), (60001, 65534)])
def test_provider_identity_rejects_root_and_nobody(uid: int, gid: int) -> None:
    with pytest.raises(SystemExit):
        provider_identity(uid, gid)
