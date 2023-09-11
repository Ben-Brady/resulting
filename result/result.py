from typing import TypeVar, Generic, TypeAlias, Protocol, NoReturn, Any
import types
from ._traceback import _generate_traceback

OkT = TypeVar("OkT", covariant=True)
ErrT = TypeVar("ErrT", covariant=True)


class ResultInterface(Protocol):
    def unwrap(self):
        ...

    def unwrap_err(self):
        ...

    def unwrap_or(self, optb):
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

    def unwrap_err(self) -> NoReturn:
        raise RuntimeError(f"Unwrapped Err on {self}")

    def unwrap_or(self, default: Any) -> OkT:
        return self._value



class Err(ResultInterface, Generic[ErrT]):
    __slots__ = ("_value", "_traceback")
    __match_args__ = ("_value",)
    _value: ErrT
    _traceback: types.TracebackType|None

    is_err = True
    is_ok = False

    def __init__(self, err: ErrT):
        self._value = err
        self._traceback = _generate_traceback()

    def __repr__(self) -> str:
        return f"Err({self._value})"

    def unwrap(self) -> NoReturn:
        raise RuntimeError(f"Unwrapped {self}").with_traceback(self._traceback)

    def unwrap_err(self) -> ErrT:
        return self._value

    T = TypeVar("T")
    def unwrap_or(self, value: T) -> T:
        return value


Result: TypeAlias = Ok[OkT] | Err[ErrT]

