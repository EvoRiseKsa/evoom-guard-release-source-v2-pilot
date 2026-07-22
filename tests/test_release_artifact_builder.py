from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.build_release_artifact import FORMAT, build_artifact


def test_builder_creates_canonical_data_only_artifact(tmp_path: Path) -> None:
    source = tmp_path / "calculator.py"
    source.write_bytes(b"def add(a, b):\n    return a + b\n")
    output = tmp_path / "release-artifact.json"
    payload = build_artifact(
        source,
        tmp_path,
        output,
        repository="EvoRiseKsa/evoom-guard-release-source-v2-pilot",
        source_commit_sha="a" * 40,
    )
    assert payload == {
        "format": FORMAT,
        "input": {
            "path": "calculator.py",
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "size": source.stat().st_size,
        },
        "repository": "EvoRiseKsa/evoom-guard-release-source-v2-pilot",
        "source_commit_sha": "a" * 40,
    }
    assert output.read_bytes() == (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def test_builder_refuses_existing_output(tmp_path: Path) -> None:
    source = tmp_path / "calculator.py"
    source.write_text("pass\n", encoding="utf-8")
    output = tmp_path / "artifact.json"
    output.write_text("existing\n", encoding="utf-8")
    with pytest.raises(ValueError, match="already exists"):
        build_artifact(
            source,
            tmp_path,
            output,
            repository="owner/repo",
            source_commit_sha="b" * 40,
        )


def test_builder_refuses_symlink_input(tmp_path: Path) -> None:
    real_root = tmp_path / "real"
    real_root.mkdir()
    source = real_root / "calculator.py"
    source.write_text("pass\n", encoding="utf-8")
    source_root = tmp_path / "source"
    source_root.mkdir()
    link = source_root / "calculator.py"
    try:
        link.symlink_to(source)
    except OSError:
        pytest.skip("symlinks are unavailable")
    with pytest.raises(ValueError, match="non-symlink"):
        build_artifact(
            link,
            source_root,
            tmp_path / "artifact.json",
            repository="owner/repo",
            source_commit_sha="c" * 40,
        )


@pytest.mark.parametrize(
    ("repository", "commit"),
    [("not-a-repository", "a" * 40), ("owner/repo", "A" * 40)],
)
def test_builder_rejects_noncanonical_identity(
    tmp_path: Path, repository: str, commit: str
) -> None:
    source = tmp_path / "calculator.py"
    source.write_text("pass\n", encoding="utf-8")
    with pytest.raises(ValueError):
        build_artifact(
            source,
            tmp_path,
            tmp_path / "artifact.json",
            repository=repository,
            source_commit_sha=commit,
        )


def test_builder_rejects_a_different_logical_input_path(tmp_path: Path) -> None:
    source = tmp_path / "other.py"
    source.write_text("pass\n", encoding="utf-8")
    with pytest.raises(ValueError, match="root calculator.py"):
        build_artifact(
            source,
            tmp_path,
            tmp_path / "artifact.json",
            repository="owner/repo",
            source_commit_sha="d" * 40,
        )
