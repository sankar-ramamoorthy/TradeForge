import sys


def test_runtime_uses_python_312() -> None:
    assert sys.version_info[:2] == (3, 12)
