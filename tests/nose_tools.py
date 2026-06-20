import pytest


def eq_(a, b):
    assert a == b


def raises(exception):
    def deco(function):
        def wrapper(*args, **kwords):
            with pytest.raises(exception):
                function(*args, **kwords)

        return wrapper

    return deco


def assert_not_in(a, b):
    assert a not in b
