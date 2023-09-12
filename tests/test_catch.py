from resulting import catch, Err, UnwrapError
from pytest import raises

def test_catch_specific():
    @catch(ValueError)
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(UnwrapError):
        result.unwrap()


def test_catch_multiple():
    @catch([TypeError, ValueError])
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(UnwrapError):
        result.unwrap()


def test_catch_all():
    @catch()
    def throw_ValueError():
        raise ValueError()

    result = throw_ValueError()
    assert throw_ValueError().is_err
    with raises(UnwrapError):
        result.unwrap()
