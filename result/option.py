from typing import TypeVar, Generic, TypeAlias, Protocol, NoReturn, Any
SomeT = TypeVar("SomeT", covariant=True)

class OptionProtocol(Protocol):
    def __repr__(self) -> str:
        ...

    def unwrap(self):
        ...

    def unwrap_or(self, optb):
        ...

    def expect(self, error: str|Exception):
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

    def expect(self, error: str|Exception) -> SomeT:
        return self._value


class none(OptionProtocol):
    __slots__ = ()

    is_some = False
    is_none = True

    def __repr__(self) -> str:
        return f"none"

    def unwrap(self) -> NoReturn:
        raise RuntimeError(f"Unwrapped {self}")

    T = TypeVar("T")
    def unwrap_or(self, value: T) -> T:
        return value

    def expect(self, error: str):
        if isinstance(error, Exception):
            raise error
        else:
            raise RuntimeError(f"{self}: {error}")

Option: TypeAlias = Some[SomeT] | none
