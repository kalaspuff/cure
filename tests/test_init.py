import pytest

import cure
from cure import decorator


def test_init():
    assert cure
    assert cure.decorator
    assert decorator

    assert isinstance(cure.__version_info__, tuple)
    assert cure.__version_info__
    assert isinstance(cure.__version__, str)
    assert len(cure.__version__)

    with pytest.raises(TypeError):
        "__version__" in cure

    with pytest.raises(AttributeError):
        cure.decorator.__version__

    with pytest.raises(AttributeError):
        decorator.__version__


def test_available_functions():
    assert cure.trail_name is not None
    assert cure.respected_keywords is not None
    assert isinstance(cure.respected_keywords, set)
    assert len(cure.respected_keywords) > 10
