"""
Source: https://github.com/fastapiutils/fastapi-utils
> from fastapi_utils.tasks import repeat_every

The package itself is no longer updated and I only need this one decorator.
Hence I decided to remove fastapi_utils from deps and just copy the decorator to the application codebase.
"""

import asyncio
import logging
import warnings
from functools import wraps
from traceback import format_exception

from .shared import handle_exc, handle_func
from .types import ExcArgNoReturnAnyFuncT, NoArgsNoReturnAnyFuncT, NoArgsNoReturnAsyncFuncT, NoArgsNoReturnDecorator


def repeat_every(
    *,
    seconds: float,
    wait_first: float | None = None,
    logger: logging.Logger | None = None,
    raise_exceptions: bool = False,
    max_repetitions: int | None = None,
    on_complete: NoArgsNoReturnAnyFuncT | None = None,
    on_exception: ExcArgNoReturnAnyFuncT | None = None,
) -> NoArgsNoReturnDecorator:
    """
    This function returns a decorator that modifies a function so it is periodically re-executed after its first call.
    Supports sync and async functions.

    The function it decorates should accept no arguments and return nothing. If necessary, this can be accomplished
    by using `functools.partial` or otherwise wrapping the target function prior to decoration.

    Parameters
    ----------
    seconds: float
        The number of seconds to wait between repeated calls
    wait_first: float (default None)
        If not None, the function will wait for the given duration before the first call
    logger: Optional[logging.Logger] (default None)
        Warning: This parameter is deprecated and will be removed in the 1.0 release.
        The logger to use to log any exceptions raised by calls to the decorated function.
        If not provided, exceptions will not be logged by this function (though they may be handled by the event loop).
    raise_exceptions: bool (default False)
        Warning: This parameter is deprecated and will be removed in the 1.0 release.
        If True, errors raised by the decorated function will be raised to the event loop's exception handler.
        Note that if an error is raised, the repeated execution will stop.
        Otherwise, exceptions are just logged and the execution continues to repeat.
        See https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler for more info.
    max_repetitions: Optional[int] (default None)
        The maximum number of times to call the repeated function. If `None`, the function is repeated forever.
    on_complete: Optional[Callable[[], None]] (default None)
        A function to call after the final repetition of the decorated function.
    on_exception: Optional[Callable[[Exception], None]] (default None)
        A function to call when an exception is raised by the decorated function.
    """

    def decorator(func: NoArgsNoReturnAnyFuncT) -> NoArgsNoReturnAsyncFuncT:
        """
        Converts the decorated function into a repeated, periodically-called version of itself.
        """

        @wraps(func)
        async def wrapped() -> None:
            async def loop() -> None:
                if wait_first is not None:
                    await asyncio.sleep(wait_first)

                repetitions = 0
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        await handle_func(func)

                    except Exception as exc:
                        if logger is not None:
                            warnings.warn(
                                "'logger' is to be deprecated in favor of 'on_exception' in the 1.0 release.",
                                DeprecationWarning,
                            )
                            formatted_exception = "".join(format_exception(type(exc), exc, exc.__traceback__))
                            logger.error(formatted_exception)
                        if raise_exceptions:
                            warnings.warn(
                                "'raise_exceptions' is to be deprecated in favor of 'on_exception' in the 1.0 release.",
                                DeprecationWarning,
                            )
                            raise exc
                        await handle_exc(exc, on_exception)

                    repetitions += 1
                    await asyncio.sleep(seconds)

                if on_complete:
                    await handle_func(on_complete)

            asyncio.ensure_future(loop())

        return wrapped

    return decorator
