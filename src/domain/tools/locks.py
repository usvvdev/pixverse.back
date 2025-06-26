# cdoing utf-8

from asyncio import Lock

from collections import defaultdict

account_locks = defaultdict(Lock)


async def run_with_account_lock(
    account_id: int,
    coro,
    *args,
    **kwargs,
):  # -> Any:
    async with account_locks[account_id]:
        return await coro(
            *args,
            **kwargs,
        )
