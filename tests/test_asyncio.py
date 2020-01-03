import asyncio

import cure


@cure.decorator
async def values(id_: str = "", type_: str = "") -> None:
    await asyncio.sleep(0.05)
    return id_, type_


class X:
    @cure.decorator
    async def values(self, id_: str = "", type_: str = "") -> None:
        await asyncio.sleep(0.05)
        return self, id_, type_

    @cure.decorator(cure.DEFAULT_OPTIONS)
    @classmethod
    async def clsvalues(cls, id_: str = "", type_: str = "") -> None:
        await asyncio.sleep(0.05)
        return cls, id_, type_

    @cure.decorator(cure.KEYWORD_TRAILING_UNDERSCORES)
    @staticmethod
    async def staticvalues(id_: str = "", type_: str = "") -> None:
        await asyncio.sleep(0.05)
        return None, id_, type_


def test_trailing_underscores_decorated_functions():
    completed = []

    async def _async():
        x = X()

        assert await values(**{"id": 4711, "type": "YES"}) == (4711, "YES")

        assert await x.values(**{"id": 4711, "type": "YES"}) == (x, 4711, "YES")

        assert await X.clsvalues(**{"id": 4711, "type": "YES"}) == (X, 4711, "YES")
        assert await x.clsvalues(**{"id": 4711, "type": "YES"}) == (X, 4711, "YES")

        assert await X.staticvalues(**{"id": 4711, "type": "YES"}) == (None, 4711, "YES")
        assert await x.staticvalues(**{"id": 4711, "type": "YES"}) == (None, 4711, "YES")

        completed.append(True)

    assert not completed

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async())

    assert completed
