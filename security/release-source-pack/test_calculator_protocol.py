"""External judge pack: never imports candidate code."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

LAUNCHER = os.environ.get("EVOGUARD_EXEC")
if not LAUNCHER:
    pytest.skip("runs only under the EvoOM Guard external judge", allow_module_level=True)


def _run(left: int, right: int) -> str:
    python = os.environ.get("EVOGUARD_PYTHON") or sys.executable
    completed = subprocess.run(
        [LAUNCHER, python, "-m", "calculator", "add", str(left), str(right)],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return completed.stdout.strip()


def test_known_sum() -> None:
    assert _run(2, 3) == "5"


def test_commutativity() -> None:
    assert _run(7, 5) == _run(5, 7) == "12"

