import asyncio

from starlette.concurrency import run_in_threadpool

from .types import ExcArgNoReturnAnyFuncT, NoArgsNoReturnAnyFuncT


async def handle_func(func: NoArgsNoReturnAnyFuncT) -> None:
    if asyncio.iscoroutinefunction(func):
        await func()
    else:
        await run_in_threadpool(func)


async def handle_exc(exc: Exception, on_exception: ExcArgNoReturnAnyFuncT | None) -> None:
    if on_exception:
        if asyncio.iscoroutinefunction(on_exception):
            await on_exception(exc)
        else:
            await run_in_threadpool(on_exception, exc)
