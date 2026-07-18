import asyncio
import random

import httpx
from src.crawler_api.exception.fetch_value_exception import FetchValueException
from src.crawler_api.service.url_fetcher.base_url_fetcher import BaseUrlFetcher
from src.crawler_api.util.check_robots import CheckRobots

headers = {"User-Agent": "Mozilla/5.0"}

class HTTPXUrlFetcher(BaseUrlFetcher):
    def __init__(self):
        self.__semaphore = asyncio.Semaphore(10)

    async def fetch(self, url: str) -> str | None:
        robots = CheckRobots(url)
        await robots.load()

        try:
            if not await robots.is_allowed(url):
                return None
            async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    raise Exception()
                return response.text
        except Exception:
            raise FetchValueException()

    async def fetch_one(self, client: httpx.AsyncClient, url: str, robots: CheckRobots) -> str | None:
        async with self.__semaphore:
            try:
                if not await robots.is_allowed(url):
                    return ""
                response = await client.get(url)

                if response.status_code != 200:
                    return ""

                await asyncio.sleep(
                    random.uniform(1.5, 3.5)
                )
                return response.text

            except Exception:
                return None


    async def fetch_by_all(self, urls: list[str], base_url: str) -> list[str]:
        robots = CheckRobots(base_url)
        await robots.load()

        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            tasks = [self.fetch_one(client, url, robots) for url in urls]
            results = await asyncio.gather(*tasks)

        return [html for html in results if html is not None]