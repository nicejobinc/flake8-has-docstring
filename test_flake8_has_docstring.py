import ast
import inspect

from flake8_has_docstring import Plugin


def test_eligible_function_has_docstring() -> None:
    source = inspect.cleandoc(
        """
        def f() -> None:
            '''This is a docstring'''
            return 0
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []


def test_eligible_function_has_no_docstring() -> None:
    source = inspect.cleandoc(
        """
        def f() -> None:
            return 0
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    expected = [(1, 0, "DOC001 Missing docstring for function 'f'", "")]
    assert result == expected


def test_eligible_method_has_docstring() -> None:
    source = inspect.cleandoc(
        """
        class C:
            def f(self) -> None:
                '''This is a docstring'''
                return 0
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []


def test_eligible_method_has_no_docstring() -> None:
    source = inspect.cleandoc(
        """
        class C:
            def f(self) -> None:
                return 0
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    expected = [(2, 4, "DOC001 Missing docstring for function 'f'", "")]
    assert result == expected


def test_pytest_fixture_has_no_docstring() -> None:
    source = inspect.cleandoc(
        """
        import pytest

        @pytest.fixture
        def f() -> Table:
            return Table()
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []


def test_scoped_pytest_fixture_has_no_docstring() -> None:
    source = inspect.cleandoc(
        """
        import pytest

        @pytest.fixture(scope="session")
        def f() -> Table:
            return Table()
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []


def test_dunder_method_has_no_docstring() -> None:
    source = inspect.cleandoc(
        """
        class C:
            def __init__(self) -> None:
                pass
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []


def test_overload_has_no_docstring() -> None:
    source = inspect.cleandoc(
        """
        from typing import overload

        @overload
        def f() -> int:
            ...

        @overload
        def f() -> str:
            ...
    """
    )
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []
