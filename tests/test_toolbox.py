import pytest

from manven.toolbox import has_binary


@pytest.mark.parametrize("binary_name, expected", [
    ("which", True),
    ("sdjfaklhas", False),
])
def test_has_binary(binary_name, expected):
    output = has_binary(binary_name)
    assert output == expected
