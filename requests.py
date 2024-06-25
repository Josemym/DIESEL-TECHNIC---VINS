import asyncio
import random
from time import perf_counter
import aiohttp

URL_ROOT = 'http://10.17.100.182:8801/impact3/application/services/parts.json/search?vin=YV2AS02A160867877&brand=VTB'

semaphore = asyncio.Semaphore(10)


async def make_request(async_session: aiohttp.ClientSession, url: str):
    # Semaphore for limiting concurrent requests to 8
    async with semaphore:
        # Asynchronous GET request
        async with async_session.get(url=url) as _response:
            # avoid overpowering the URL right away by having this happen first                   
            #content = await _response.headers
            
            await asyncio.sleep(random.randint(1,4))    

            print(_response.status)


async def makes_all_requests(urls: list[str]):
    # Stores all tasks that will later be used on `asyncio.gather`
    async with aiohttp.ClientSession() as async_session:
        tasks = []
        for url in urls:
            # Creates asyncio.Task that will return a future
            task = asyncio.create_task(
                coro=make_request(
                    async_session=async_session,
                    url=f"http://10.17.100.182:8801/impact3/application/services/parts.json/search?vin={url}&brand=VTB",
                )
            )

            tasks.append(task)

        # Tasks are ran with asyncio.gather
        # By setting `return_exceptions` to False, we will raise Exceptions within
        #   their asyncio task instance and everything will stop, by putting True, it
        #   will raise when `result()` is called on the future.
        await asyncio.gather(*tasks, return_exceptions=False)



