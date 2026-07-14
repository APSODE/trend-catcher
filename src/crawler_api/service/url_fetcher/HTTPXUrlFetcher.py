import random
import time

import httpx
from src.crawler_api.exception.FetchValueException import FetchValueException
from src.crawler_api.service.url_fetcher.BaseUrlFetcher import BaseUrlFetcher
from src.crawler_api.util.CheckRobots import CheckRobots

headers = {"User-Agent": "Mozilla/5.0"}

class HTTPXUrlFetcher(BaseUrlFetcher):

    async def fetch(self, url: str) -> str:
        robots = CheckRobots(url)

        try:
            if not await robots.is_allowed(url):
                return None
            response = httpx.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception()
            return response.text
        except Exception as e:
            raise FetchValueException()

    async def fetch_by_all(self, urls: list[str], base_url : str) -> list[str]:
        results = []
        robots = CheckRobots(base_url)
        for url in urls:
            try:
                if not await robots.is_allowed(url):
                    continue
                response = httpx.get(url, headers=headers)
                if response.status_code != 200:
                    continue
                results.append(response.text)
                time.sleep(random.uniform(1.5, 3.5))
            except Exception as e:
                continue
        return results
