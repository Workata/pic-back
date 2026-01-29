import logging
from functools import wraps

from .shared import handle_func
from .types import NoArgsNoReturnAnyFuncT, NoArgsNoReturnAsyncFuncT

logger = logging.getLogger(name="skip_first_call")


def skip_first_call(func: NoArgsNoReturnAnyFuncT) -> NoArgsNoReturnAsyncFuncT:
    """
    Decorator for async functions that skips the first call.
    """

    called: bool = False

    @wraps(func)
    async def wrapped() -> None:
        nonlocal called

        if not called:
            called = True
            logger.info(f"Function {func.__name__} omitted - first call")
            return None

        await handle_func(func)

    return wrapped
