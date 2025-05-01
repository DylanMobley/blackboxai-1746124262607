# async_engine/runner.py

import asyncio
import logging
from typing import Callable, Dict, Any, Awaitable

# Configure Async Logging
logger = logging.getLogger("AsyncRunner")
logger.setLevel(logging.INFO)

async def run_parallel_tasks(tasks: Dict[str, Callable[[], Awaitable[Any]]]) -> Dict[str, Any]:
    """
    Execute multiple async tasks in parallel.
    :param tasks: Dictionary mapping task name -> async function (no args)
    :return: Dictionary of task name -> result
    """
    results = {}

    async def wrapper(name, coro_func):
        try:
            result = await coro_func()
            logger.info(f"✅ Async task completed: {name}")
            results[name] = result
        except Exception as e:
            logger.error(f"❌ Async task failed: {name}", exc_info=True)
            results[name] = None

    await asyncio.gather(*(wrapper(name, coro) for name, coro in tasks.items()))
    return results

async def run_sequential_tasks(tasks: Dict[str, Callable[[], Awaitable[Any]]]) -> Dict[str, Any]:
    """
    Execute multiple async tasks sequentially (await each one by order).
    :param tasks: Dictionary mapping task name -> async function (no args)
    :return: Dictionary of task name -> result
    """
    results = {}

    for name, coro_func in tasks.items():
        try:
            result = await coro_func()
            logger.info(f"✅ Sequential task completed: {name}")
            results[name] = result
        except Exception as e:
            logger.error(f"❌ Sequential task failed: {name}", exc_info=True)
            results[name] = None

    return results
