import random
import time

import httpx
from src.crawler_api.exception.FetchValueException import FetchValueException
from src.crawler_api.service.url_fetcher.BaseUrlFetcher import BaseUrlFetcher

headers = {"User-Agent": "Mozilla/5.0"}

class HTTPXUrlFetcher(BaseUrlFetcher):

    async def fetch(self, url: str) -> str:
        try:
            response = httpx.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception()
            return response.text
        except Exception as e:
            raise FetchValueException()

    async def fetch_by_all(self, urls: list[str]) -> list[str]:
        results = []
        for url in urls:
            try:
                response = httpx.get(url, headers=headers)
                if response.status_code != 200:
                    continue
                results.append(response.text)
                time.sleep(random.uniform(1.5, 3.5))
            except Exception as e:
                continue
        return results
