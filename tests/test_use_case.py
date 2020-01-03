from cure import DEFAULT_OPTIONS, KEYWORD_TRAILING_UNDERSCORES, cure


@cure
def values(id_: str = "", type_: str = "") -> None:
    return id_, type_


class X:
    @cure(1)
    def values(self, id_: str = "", type_: str = "") -> None:
        return self, id_, type_

    @cure(DEFAULT_OPTIONS)
    @classmethod
    def clsvalues(cls, id_: str = "", type_: str = "") -> None:
        return cls, id_, type_

    @cure(KEYWORD_TRAILING_UNDERSCORES)
    @staticmethod
    def staticvalues(id_: str = "", type_: str = "") -> None:
        return None, id_, type_


def test_trailing_underscores_decorated_functions():
    x = X()

    assert values(**{"id": 4711, "type": "YES"}) == (4711, "YES")

    assert x.values(**{"id": 4711, "type": "YES"}) == (x, 4711, "YES")

    assert X.clsvalues(**{"id": 4711, "type": "YES"}) == (X, 4711, "YES")
    assert x.clsvalues(**{"id": 4711, "type": "YES"}) == (X, 4711, "YES")

    assert X.staticvalues(**{"id": 4711, "type": "YES"}) == (None, 4711, "YES")
    assert x.staticvalues(**{"id": 4711, "type": "YES"}) == (None, 4711, "YES")
