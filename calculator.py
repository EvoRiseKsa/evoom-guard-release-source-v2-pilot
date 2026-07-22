"""Tiny candidate used only to exercise the source-admission pilot."""

from __future__ import annotations

import sys


def add(left: int, right: int) -> int:
    return left + right


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 3 or arguments[0] != "add":
        print("usage: python -m calculator add LEFT RIGHT", file=sys.stderr)
        return 2
    print(add(int(arguments[1]), int(arguments[2])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

