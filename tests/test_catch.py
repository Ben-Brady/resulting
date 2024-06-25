from resulting import catch, Err, UnwrapError
from pytest import raises


def test(name):
    name = " " + name

    def wrapper(func):
        globals()[name] = func
        return func

    return wrapper


@test("'@catch' catches specified errors")
def _():
    @catch(ValueError)
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(UnwrapError):
        result.unwrap()


@test("'@catch' doesn't catch unspecified errors")
def _():
    @catch(ValueError)
    def throw_KeyError():
        raise KeyError()

    with raises(KeyError):
        throw_KeyError()


@test("'@catch' can catch multiple specified errors")
def test_catch_multiple():
    @catch([TypeError, ValueError])
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(UnwrapError):
        result.unwrap()


@test("'@catch' by default catches all errors")
def test_catch_all():
    @catch()
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(UnwrapError):
        result.unwrap()
