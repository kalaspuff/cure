import pytest

import cure


def test_default_options():
    assert cure.get_options() == cure.DEFAULT_OPTIONS
    assert cure.get_options() == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(cure.DEFAULT_OPTIONS) == cure.DEFAULT_OPTIONS


def test_options():
    assert cure.get_options(1) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(1, 0, 0, 1) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(KEYWORD_TRAILING_UNDERSCORES=True) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(keyword_trailing_underscores=True) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(["KEYWORD_TRAILING_UNDERSCORES"]) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(["keyword_trailing_underscores"]) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options([1]) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options([cure.KEYWORD_TRAILING_UNDERSCORES]) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options((cure.KEYWORD_TRAILING_UNDERSCORES)) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(cure.KEYWORD_TRAILING_UNDERSCORES) == [cure.KEYWORD_TRAILING_UNDERSCORES]
    assert cure.get_options(cure.KEYWORD_TRAILING_UNDERSCORES, cure.KEYWORD_TRAILING_UNDERSCORES) == [
        cure.KEYWORD_TRAILING_UNDERSCORES
    ]
    assert cure.get_options("KEYWORD_TRAILING_UNDERSCORES", cure.KEYWORD_TRAILING_UNDERSCORES) == [
        cure.KEYWORD_TRAILING_UNDERSCORES
    ]

    with pytest.raises(TypeError):
        cure.get_options(0)

    with pytest.raises(TypeError):
        cure.get_options(KEYWORD_TRAILING_UNDERSCORES=False)

    with pytest.raises(TypeError):
        cure.get_options(1, 2)

    with pytest.raises(TypeError):
        cure.get_options(2)

    with pytest.raises(TypeError):
        cure.get_options([2])

    with pytest.raises(TypeError):
        cure.get_options([3])

    with pytest.raises(TypeError):
        cure.get_options(["unknown_option"])

    with pytest.raises(TypeError):
        cure.get_options(unknown_option=True)

    with pytest.raises(TypeError):
        cure.get_options("string_options")
