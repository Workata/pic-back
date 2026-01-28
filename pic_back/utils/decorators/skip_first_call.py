from __future__ import annotations

from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

# TODO verify

P = ParamSpec("P")
R = TypeVar("R")


def skip_first_call(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    """
    Decorator for async functions that skips the first call.
    First call returns None, later calls run normally.
    """

    called: bool = False

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        nonlocal called

        if not called:
            called = True
            return None  # skipped

        return await func(*args, **kwargs)

    return wrapper
