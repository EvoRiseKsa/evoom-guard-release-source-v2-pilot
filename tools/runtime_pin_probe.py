"""Produce reviewable runner/runtime pins without changing repository settings."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def executable(name: str) -> dict[str, str]:
    located = shutil.which(name)
    if not located:
        raise SystemExit(f"required executable is absent: {name}")
    resolved = Path(located).resolve(strict=True)
    if not resolved.is_file():
        raise SystemExit(f"resolved executable is not a regular file: {resolved}")
    version = subprocess.run(
        [str(resolved), "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    ).stdout.splitlines()[0]
    return {"path": str(resolved), "sha256": sha256(resolved), "version": version}


def provider_identity(uid: int, gid: int) -> dict[str, object]:
    if not 1 <= uid <= 2_147_483_647 or not 1 <= gid <= 2_147_483_647:
        raise SystemExit("provider UID/GID must be non-root positive POSIX IDs")
    if uid == 65534 or gid == 65534:
        raise SystemExit("provider UID/GID must not reuse nobody/65534")
    getent = shutil.which("getent")
    if not getent:
        raise SystemExit("getent is required to prove provider UID/GID availability")
    passwd = subprocess.run([getent, "passwd", str(uid)], capture_output=True, text=True)
    group = subprocess.run([getent, "group", str(gid)], capture_output=True, text=True)
    if passwd.returncode == 0 or group.returncode == 0:
        raise SystemExit("configured provider UID/GID conflicts with an existing account")
    if passwd.returncode != 2 or group.returncode != 2:
        raise SystemExit("getent did not return the expected not-found status")
    return {
        "uid": uid,
        "gid": gid,
        "non_root": True,
        "not_nobody_65534": True,
        "getent_passwd_conflict": False,
        "getent_group_conflict": False,
    }


def build_report(
    bootstrap: Path,
    expected_bootstrap_sha256: str,
    *,
    provider_uid: int | None = None,
    provider_gid: int | None = None,
) -> dict[str, object]:
    expected = expected_bootstrap_sha256.strip().lower()
    if len(expected) != 64 or any(character not in "0123456789abcdef" for character in expected):
        raise SystemExit("expected bootstrap digest must be one lowercase SHA-256")
    actual = sha256(bootstrap.resolve(strict=True))
    if actual != expected:
        raise SystemExit("downloaded bootstrap digest does not match the external pin")
    report: dict[str, object] = {
        "format": "EVOGUARD_V2_RUNTIME_PIN_PROBE_V1",
        "runner": {
            "environment": os.environ.get("RUNNER_ENVIRONMENT", "local"),
            "image_os": os.environ.get("ImageOS", ""),
            "image_version": os.environ.get("ImageVersion", ""),
            "platform": platform.platform(),
            "python": sys.version.split()[0],
        },
        "bootstrap": {"path": str(bootstrap.resolve()), "sha256": actual},
        "git": executable("git"),
        "github_cli": executable("gh"),
    }
    if (provider_uid is None) != (provider_gid is None):
        raise SystemExit("provider UID and GID must be supplied together")
    if provider_uid is not None and provider_gid is not None:
        report["provider_identity"] = provider_identity(provider_uid, provider_gid)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", required=True, type=Path)
    parser.add_argument("--expected-bootstrap-sha256", required=True)
    parser.add_argument("--provider-uid", required=True, type=int)
    parser.add_argument("--provider-gid", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    report = build_report(
        args.bootstrap,
        args.expected_bootstrap_sha256,
        provider_uid=args.provider_uid,
        provider_gid=args.provider_gid,
    )
    args.output.write_text(
        json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
