import convention


def test_class_methods():
    class X:
        called = 0

        @classmethod
        def clsmethod(cls, id_=0):
            def _fn(id_=0):
                cls.called += 1
                return id_

            return convention.decorator(1, 2, 3, 4)(_fn)(id=id_)

        @convention
        @classmethod
        def classicclassmethod(cls, id_=0):
            def _fn(id_=0):
                cls.called += 1
                return id_

            return _fn(id_=id_)

        @convention(value="yes")
        def func(self, id_=0):
            @convention
            def _fn(id_=0):
                return id_

            return _fn(id=id_)

        @staticmethod
        def stat(**kwargs):
            return kwargs.get('id_', 0)

        @convention.decorator
        @staticmethod
        def dstat(**kwargs):
            return kwargs.get('type_', 0)

    @convention(id=4711, id_=1338, type_=0)
    def local_func(id_, type_):
        return id_ * type_

    assert X.clsmethod(id_=20) == 20
    assert X().clsmethod(id_=19) == 19
    assert convention(X.clsmethod)(id_=18) == 18
    assert convention(X.clsmethod)(id=17) == 17
    assert convention.decorator(X().clsmethod)(id=16) == 16

    assert X.called == 5

    assert X().func(id_=15) == 15
    assert X().func(id=14) == 14

    assert X.stat(id_=13) == 13
    assert X().stat(id_=12) == 12
    assert convention(X.stat)(id=11) == 11
    assert convention(X().stat)(id=10) == 10

    assert X.dstat(type=9) == 9
    assert X().dstat(type=8) == 8
    assert X.dstat(type_=7) == 7
    assert X().dstat(type_=6) == 6

    assert local_func(**{"id": 13, "type": 7}) - 86 == 5
    assert local_func(**{"id": 13, "type_": 7}) - 87 == 4
    assert local_func(type=7, **{"id": 13}) - 88 == 3

    assert X.classicclassmethod(id=2) == 2
    assert X().classicclassmethod(id=1) == 1

    assert X.called == 7
