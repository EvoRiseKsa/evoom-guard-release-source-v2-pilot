"""Tiny candidate used only to exercise the source-admission pilot."""

from __future__ import annotations

import sys


def add(left: int, right: int) -> int:
    """Return the integer sum exposed by the pilot CLI."""
    total = left + right
    return total


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 3 or arguments[0] != "add":
        print("usage: python -m calculator add LEFT RIGHT", file=sys.stderr)
        return 2
    _, left_text, right_text = arguments
    print(add(int(left_text), int(right_text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
