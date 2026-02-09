"""Tests unitarios del módulo calculator."""

import pytest

from pyapp.calculator import add, greet, is_even


@pytest.mark.unit
class TestAdd:
    def test_add_integers(self) -> None:
        assert add(1, 2) == 3

    def test_add_floats(self) -> None:
        assert add(1.5, 2.5) == 4.0

    def test_add_zero(self) -> None:
        assert add(0, 0) == 0


@pytest.mark.unit
class TestGreet:
    def test_greet_returns_message(self) -> None:
        assert greet("World") == "Hello, World!"

    def test_greet_strips_whitespace(self) -> None:
        assert greet("  Alice  ") == "Hello, Alice!"

    def test_greet_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            greet("")

    def test_greet_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            greet("   ")


@pytest.mark.unit
class TestIsEven:
    def test_even(self) -> None:
        assert is_even(0) is True
        assert is_even(2) is True

    def test_odd(self) -> None:
        assert is_even(1) is False
        assert is_even(-1) is False
