import trailing


def test_init() -> None:
    assert trailing

    assert isinstance(trailing.__version_info__, tuple)
    assert trailing.__version_info__
    assert isinstance(trailing.__version__, str)
    assert len(trailing.__version__)
