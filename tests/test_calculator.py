from calculator import add, main


def test_add() -> None:
    assert add(2, 3) == 5


def test_cli(capsys) -> None:
    assert main(["add", "7", "5"]) == 0
    assert capsys.readouterr().out == "12\n"

