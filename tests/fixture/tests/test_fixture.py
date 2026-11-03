import fixture_pkg


def test_double() -> None:
    assert fixture_pkg.double(21) == 42


def test_version() -> None:
    assert fixture_pkg.__version__ == "0.0.1"
