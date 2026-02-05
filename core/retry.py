import asyncio

async def retry_async(func, params, retries=3):
    for i in range(retries):
        try:
            return await func(params)
        except Exception:
            if i == retries - 1:
                raise
            await asyncio.sleep(1)
