class UnwrapError(Exception):
    pass

from ._result import Result, Ok, Err
from ._option import Option, Some, none
from ._wrappers import catch, optional, acatch, aoptional

__all__ = [
    "Result",
    "Ok",
    "Err",
    "Option",
    "Some",
    "none",
    "catch",
    "optional",
    "acatch",
    "aoptional",
]
