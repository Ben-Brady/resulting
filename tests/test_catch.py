from result import catch, Err
from typing import get_type_hints
from pytest import raises


def test_a():
    @catch(ValueError)
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(ValueError):
        result.unwrap()


def test_catch_all():
    @catch()
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(ValueError):
        result.unwrap()
