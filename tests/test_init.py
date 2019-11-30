import pytest

import convention
from convention import decorator


def test_init():
    assert convention
    assert convention.decorator
    assert decorator

    assert isinstance(convention.__version_info__, tuple)
    assert convention.__version_info__
    assert isinstance(convention.__version__, str)
    assert len(convention.__version__)

    with pytest.raises(TypeError):
        "__version__" in convention

    with pytest.raises(AttributeError):
        convention.decorator.__version__

    with pytest.raises(AttributeError):
        decorator.__version__


def test_available_functions():
    assert convention.trail is not None
    assert convention.respected_keywords is not None
    assert isinstance(convention.respected_keywords, set)
    assert len(convention.respected_keywords) > 10
