import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Coroutine, List, Union

from starlette.concurrency import run_in_threadpool

from pic_back.settings import get_settings
from pic_back.shared import EnvType

settings = get_settings()
logger = logging.getLogger(name="only_on_envs")

NoArgsNoReturnFuncT = Callable[[], None]
NoArgsNoReturnAsyncFuncT = Callable[[], Coroutine[Any, Any, None]]
ExcArgNoReturnFuncT = Callable[[Exception], None]
ExcArgNoReturnAsyncFuncT = Callable[[Exception], Coroutine[Any, Any, None]]
NoArgsNoReturnAnyFuncT = Union[NoArgsNoReturnFuncT, NoArgsNoReturnAsyncFuncT]
ExcArgNoReturnAnyFuncT = Union[ExcArgNoReturnFuncT, ExcArgNoReturnAsyncFuncT]
NoArgsNoReturnDecorator = Callable[[NoArgsNoReturnAnyFuncT], NoArgsNoReturnAsyncFuncT]


async def _handle_func(func: NoArgsNoReturnAnyFuncT) -> None:
    if asyncio.iscoroutinefunction(func):
        await func()
    else:
        await run_in_threadpool(func)


def only_on_envs(envs: List[EnvType]) -> NoArgsNoReturnDecorator:
    """
    This function returns a decorator that modifies a function so it is triggered only on specified envs.

    The function it decorates should accept no arguments and return nothing. Supports sync and async functions.
    """

    def decorator(func: NoArgsNoReturnAnyFuncT) -> NoArgsNoReturnAsyncFuncT:
        """
        Converts the decorated function into a repeated, periodically-called version of itself.
        """

        @wraps(func)
        async def wrapped() -> None:
            if settings.environment not in envs:
                logger.info(f"Function {func.__name__} omitted on current env ({settings.environment})")
                return None
            await _handle_func(func)

        return wrapped

    return decorator
