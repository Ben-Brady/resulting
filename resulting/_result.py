from . import UnwrapError
from ._traceback import _generate_traceback
from typing import (
    TypeVar, Generic, TypeAlias,
    Protocol, NoReturn, Any,
    Literal
)
import types

OkT = TypeVar("OkT", covariant=True)
ErrT = TypeVar("ErrT", covariant=True)


class ResultInterface(Protocol):
    def unwrap(self):
        ...

    def expect(self, message: str):
        ...

    def unwrap_err(self):
        ...

    def expect_err(self, message: str):
        ...

    def unwrap_or(self, optb):
        ...


class Ok(ResultInterface, Generic[OkT]):
    __slots__ = ("_value",)
    __match_args__ = ("_value", "_traceback")
    _value: OkT
    _traceback: types.TracebackType|None

    is_ok: Literal[True] = True
    is_err: Literal[False] = False

    def __init__(self, value: OkT, *, with_traceback: bool = True):
        self._value = value
        if with_traceback:
            self._traceback = _generate_traceback()
        else:
            self._traceback = None

    def __repr__(self) -> str:
        return f"Ok({self._value})"

    def unwrap(self) -> OkT:
        return self._value

    def expect(self, message: str) -> OkT:
        return self._value

    def unwrap_err(self) -> NoReturn:
        raise UnwrapError(f"Unwrapped Err on {self}").with_traceback(self._traceback)

    def expect_err(self, message: str) -> NoReturn:
        raise UnwrapError(message).with_traceback(self._traceback)

    def unwrap_or(self, default: Any) -> OkT:
        return self._value




class Err(ResultInterface, Generic[ErrT]):
    __slots__ = ("_value", "_traceback")
    __match_args__ = ("_value",)
    _value: ErrT
    _traceback: types.TracebackType|None

    is_ok: Literal[False] = False
    is_err: Literal[True] = True

    def __init__(self, err: ErrT, *, with_traceback: bool = True):
        """
        Use `with_traceback=False` to disable traceback generation,
        this provides a minotr speed-up when creating Err.
        """
        self._value = err

        if with_traceback:
            self._traceback = _generate_traceback()
        else:
            self._traceback = None

    def __repr__(self) -> str:
        return f"Err({self._value})"


    def unwrap(self) -> NoReturn:
        raise UnwrapError(f"Unwrapped Err on {self}").with_traceback(self._traceback)

    def expect(self, message: str) -> NoReturn:
        raise UnwrapError(message).with_traceback(self._traceback)

    def unwrap_err(self) -> ErrT:
        return self._value

    def expect_err(self, message: str) -> ErrT:
        return self._value

    T = TypeVar("T")
    def unwrap_or(self, value: T) -> T:
        return value


Result: TypeAlias = Ok[OkT] | Err[ErrT]
