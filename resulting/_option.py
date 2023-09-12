from ._traceback import  _generate_traceback
from ._shared import UnwrapError
from typing import TypeVar, Generic, TypeAlias, Protocol, NoReturn, Any
import types

SomeT = TypeVar("SomeT", covariant=True)

class OptionProtocol(Protocol):
    def __repr__(self) -> str:
        ...

    def unwrap(self):
        ...

    def unwrap_or(self, optb):
        ...

    is_some: bool
    is_none: bool


class Some(OptionProtocol, Generic[SomeT]):
    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    _value: SomeT

    is_some = True
    is_none = False

    def __init__(self, value: SomeT):
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({self._value})"

    def unwrap(self) -> SomeT:
        return self._value

    def unwrap_or(self, default: Any) -> SomeT:
        return self._value


class none(OptionProtocol):
    __slots__ = ()
    _traceback: types.TracebackType|None
    __slots__ = ()

    is_some = False
    is_none = True

    def __init__(self):
        self._traceback = _generate_traceback()

    def __repr__(self) -> str:
        return f"none"

    def unwrap(self) -> NoReturn:
        raise UnwrapError(f"Unwrapped {self}").with_traceback(self._traceback)

    T = TypeVar("T")
    def unwrap_or(self, value: T) -> T:
        return value


Option: TypeAlias = Some[SomeT] | none
