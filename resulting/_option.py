from . import UnwrapError
from ._traceback import _generate_traceback
from typing import TypeVar, Generic, TypeAlias, Protocol, NoReturn, Any, Literal
from abc import ABC
import types

SomeT = TypeVar("SomeT", covariant=True)


class OptionBase(ABC, Generic[SomeT]):
    def __init__(self, value: SomeT | None):
        if value is None:
            return none()
        else:
            return Some(value)

    def __repr__(self) -> str: ...

    def unwrap(self): ...

    def expect(self, message: str) -> SomeT | NoReturn: ...

    def unwrap_or(self, default: Any) -> SomeT: ...


class Some(OptionBase, Generic[SomeT]):
    __slots__ = ("_value",)
    __match_args__ = ("_value", "_traceback")

    _value: SomeT
    _traceback: types.TracebackType | None

    is_some: Literal[True] = True
    is_none: Literal[False] = False

    def __init__(self, value: SomeT, *, with_traceback: bool = True):
        self._value = value

        if with_traceback:
            self._traceback = _generate_traceback()
        else:
            self._traceback = None

    def __repr__(self) -> str:
        return f"Ok({self._value})"

    def unwrap(self) -> SomeT:
        return self._value

    def expect(self, message: str) -> SomeT:
        return self._value

    def unwrap_or(self, default: Any) -> SomeT:
        return self._value


class none(OptionBase):
    __slots__ = ("_traceback",)
    _traceback: types.TracebackType | None

    is_some: Literal[False] = False
    is_none: Literal[True] = True

    def __init__(self, *, with_traceback: bool = True):
        if with_traceback:
            self._traceback = _generate_traceback()
        else:
            self._traceback = None

    def __repr__(self) -> str:
        return f"none"

    def unwrap(self) -> NoReturn:
        raise UnwrapError(f"Unwrapped {self}").with_traceback(self._traceback)

    def expect(self, message: str) -> NoReturn:
        raise UnwrapError(message).with_traceback(self._traceback)

    T = TypeVar("T")

    def unwrap_or(self, value: T) -> T:
        return value


Option: TypeAlias = Some[SomeT] | none
