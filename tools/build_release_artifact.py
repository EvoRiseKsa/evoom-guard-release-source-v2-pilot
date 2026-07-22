"""Build one deterministic, data-only artifact for the public RAAE pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat

FORMAT = "EVOGUARD_RAAE_PILOT_ARTIFACT_V1"
MAX_INPUT_BYTES = 1024 * 1024
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
GIT_SHA = re.compile(r"[0-9a-f]{40}\Z")


def _stable_regular_file(path: Path) -> bytes:
    before = path.lstat()
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISREG(before.st_mode):
        raise ValueError("artifact input must be a regular non-symlink file")
    if before.st_size > MAX_INPUT_BYTES:
        raise ValueError("artifact input exceeds the one MiB pilot limit")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise ValueError("artifact input changed away from a regular file")
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise ValueError("artifact input identity changed before read")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_INPUT_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_INPUT_BYTES:
                raise ValueError("artifact input exceeds the one MiB pilot limit")
        after_open = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after_path = path.lstat()
    identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    if identity != (
        after_open.st_dev,
        after_open.st_ino,
        after_open.st_size,
        after_open.st_mtime_ns,
    ) or identity != (
        after_path.st_dev,
        after_path.st_ino,
        after_path.st_size,
        after_path.st_mtime_ns,
    ):
        raise ValueError("artifact input changed while being read")
    return b"".join(chunks)


def build_artifact(
    source: Path,
    source_root: Path,
    output: Path,
    *,
    repository: str,
    source_commit_sha: str,
) -> dict[str, object]:
    if REPOSITORY.fullmatch(repository) is None:
        raise ValueError("repository must be canonical owner/repository text")
    if GIT_SHA.fullmatch(source_commit_sha) is None:
        raise ValueError("source commit must be one lowercase 40-hex Git SHA")
    if output.exists() or output.is_symlink():
        raise ValueError("artifact output already exists")
    root = source_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("artifact source root must be a directory")
    try:
        logical_path = Path(os.path.abspath(source)).relative_to(root)
    except ValueError as exc:
        raise ValueError("artifact input must be inside its declared source root") from exc
    if logical_path.as_posix() != "calculator.py":
        raise ValueError("pilot artifact input must be root calculator.py")
    if source.resolve(strict=True) == output.resolve(strict=False):
        raise ValueError("artifact input and output paths must differ")
    source_bytes = _stable_regular_file(source)
    payload: dict[str, object] = {
        "format": FORMAT,
        "input": {
            "path": logical_path.as_posix(),
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
            "size": len(source_bytes),
        },
        "repository": repository,
        "source_commit_sha": source_commit_sha,
    }
    encoded = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_BINARY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(output, flags, 0o600)
    try:
        view = memoryview(encoded)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("short write while creating pilot artifact")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit-sha", required=True)
    args = parser.parse_args(argv)
    build_artifact(
        args.input,
        args.source_root,
        args.output,
        repository=args.repository,
        source_commit_sha=args.source_commit_sha,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
