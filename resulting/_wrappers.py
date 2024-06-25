from . import Result, Ok, Err, Option, Some, none
from typing import ParamSpec, Callable, TypeVar, Sequence, Coroutine

ParamT = ParamSpec("ParamT")
ReturnT = TypeVar("ReturnT")
ErrorT = TypeVar("ErrorT", bound=Exception)
AsyncCallable = Callable[ParamT, Coroutine[None, None, ReturnT]]

def catch(
        errors: Sequence[type[ErrorT]]|type[ErrorT] = Exception
        ) -> Callable[[Callable[ParamT, ReturnT]], Callable[ParamT, Result[ReturnT, ErrorT]]]:
    """
    Catch any errors a function throws

    ```python
    @catch()
    def get_user() -> str:
        raise KeyError("User Not Found")

    get_user() # Result[str, Exception]
    ```

    or catch specific errors

    ```python
    @catch(KeyError)
    def get_user() -> str:
        raise KeyError("User Not Found")

    get_user() # Result[str, KeyError]
    ```

    or catch specific errors

    ```python
    @catch(KeyError)
    def get_user() -> str:
        raise KeyError("User Not Found")

    get_user() # Result[str, KeyError]
    ```
    """
    def wrapper(func: Callable[ParamT, ReturnT]) -> Callable[ParamT, Result[ReturnT, ErrorT]]:
        if isinstance(errors, type):
            catchable_error = (errors,)
        else:
            catchable_error = tuple(errors)

        def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Result[ReturnT, ErrorT]:
            try:
                value = func(*args, **kwargs)
                return Ok(value)
            except Exception as e:
                if isinstance(e, catchable_error):
                    return Err(e)
                else:
                    raise e

        return inner

    return wrapper


def acatch(
    errors: Sequence[type[ErrorT]] | type[ErrorT] = Exception,
) -> Callable[[AsyncCallable[ParamT, ReturnT]], AsyncCallable[ParamT, Result[ReturnT, ErrorT]]]:
    """
    Catch any errors a function throws

    ```python
    @acatch()
    async def get_user() -> str:
        raise KeyError("User Not Found")

    await get_user() # Result[str, Exception]
    ```

    or catch specific errors

    ```python
    @acatch(KeyError)
    async def get_user() -> str:
        raise KeyError("User Not Found")

    await get_user() # Result[str, KeyError]
    ```

    or catch specific errors

    ```python
    @acatch(KeyError)
    async def get_user() -> str:
        raise KeyError("User Not Found")

    await get_user() # Result[str, KeyError]
    ```
    """
    def wrapper(
        func: AsyncCallable[ParamT, ReturnT]
    ) -> AsyncCallable[ParamT, Result[ReturnT, ErrorT]]:
        if isinstance(errors, type):
            catchable_error = (errors,)
        else:
            catchable_error = tuple(errors)

        async def inner(
            *args: ParamT.args, **kwargs: ParamT.kwargs
        ) -> Result[ReturnT, ErrorT]:
            try:
                value = await func(*args, **kwargs)
                return Ok(value)
            except Exception as e:
                if isinstance(e, catchable_error):
                    return Err(e)
                else:
                    raise e

        return inner

    return wrapper


def optional(func: Callable[ParamT, ReturnT|None]) -> Callable[ParamT, Option[ReturnT]]:
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Option[ReturnT]:
        value = func(*args, **kwargs)
        if value is None:
            return none()
        else:
            return Some(value)

    return inner


def aoptional(func: AsyncCallable[ParamT, ReturnT|None]) -> AsyncCallable[ParamT, Option[ReturnT]]:
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Option[ReturnT]:
        value = func(*args, **kwargs)
        if value is None:
            return none()
        else:
            return Some(value)

    return inner
