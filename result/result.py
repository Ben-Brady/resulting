from typing import TypeVar, Generic, TypeAlias, Protocol, NoReturn, Any

OkT = TypeVar("OkT", covariant=True)
ErrT = TypeVar("ErrT", covariant=True)


class ResultInterface(Protocol):
    def unwrap(self):
        ...

    def unwrap_err(self):
        ...

    def unwrap_or(self, optb):
        ...

    def expect(self, error: str|Exception):
        ...

    def expect_err(self, error: str|Exception):
        ...

    is_ok: bool
    is_err: bool


class Ok(ResultInterface, Generic[OkT]):
    __slots__ = ("_value",)
    __match_args__ = ("_value",)
    _value: OkT

    is_ok = True
    is_err = False

    def __init__(self, value: OkT):
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({self._value})"

    def unwrap(self) -> OkT:
        return self._value

    def unwrap_or(self, default: Any) -> OkT:
        return self._value

    def unwrap_err(self) -> NoReturn:
        raise RuntimeError(f"Unwrapped Err on {self}")

    def expect(self, error: str|Exception) -> OkT:
        return self._value

    def expect_err(self, error: str|Exception):
        if isinstance(error, Exception):
            raise error
        else:
            raise RuntimeError(error)

import sys
import types

def _generate_traceback(err: type[Exception], msg: str|None = None) -> Exception:
    tb = None
    depth = 0
    while True:
        try:
            frame = sys._getframe(depth)
            depth += 1
        except ValueError:
            break

        tb = types.TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)

    return err(msg).with_traceback(tb)


class Err(ResultInterface, Generic[ErrT]):
    __slots__ = ("_value", "_traceback")
    __match_args__ = ("_value",)
    _value: ErrT
    _traceback: Exception

    is_err = True
    is_ok = False

    def __init__(self, err: ErrT):
        self._value = err

        if isinstance(err, type) and issubclass(err, Exception):
            self._traceback = _generate_traceback(err)
        else:
            _

    def __repr__(self) -> str:
        return f"Err({self._value})"

    def unwrap(self) -> NoReturn:
        if isinstance(self._value, Exception):
            raise self._value
        else:
            raise RuntimeError(f"Unwrapped {self}")

    def unwrap_err(self) -> ErrT:
        return self._value

    T = TypeVar("T")
    def unwrap_or(self, value: T) -> T:
        return value

    def expect(self, error: str|Exception) -> ErrT:
        if isinstance(error, Exception):
            raise error
        else:
            raise RuntimeError(f"{self}: {error}")

    def expect_err(self, error: str):
        return self._value


Result: TypeAlias = Ok[OkT] | Err[ErrT]
