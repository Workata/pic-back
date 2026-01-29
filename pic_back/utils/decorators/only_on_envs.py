import logging
from functools import wraps
from typing import List

from pic_back.settings import get_settings
from pic_back.shared import EnvType

from .shared import handle_func
from .types import NoArgsNoReturnAnyFuncT, NoArgsNoReturnAsyncFuncT, NoArgsNoReturnDecorator

settings = get_settings()
logger = logging.getLogger(name="only_on_envs")


def only_on_envs(envs: List[EnvType]) -> NoArgsNoReturnDecorator:
    """
    This function returns a decorator that modifies a function so it is triggered only on specified envs.

    The function it decorates should accept no arguments and return nothing. Supports sync and async functions.
    """

    def decorator(func: NoArgsNoReturnAnyFuncT) -> NoArgsNoReturnAsyncFuncT:
        @wraps(func)
        async def wrapped() -> None:
            if settings.environment not in envs:
                logger.info(f"Function {func.__name__} omitted on current env ({settings.environment})")
                return None
            await handle_func(func)

        return wrapped

    return decorator
