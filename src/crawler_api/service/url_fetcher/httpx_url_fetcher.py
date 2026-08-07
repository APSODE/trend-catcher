import asyncio
import logging
import random
import httpx

from src.crawler_api.exception.fetch_value_exception import FetchValueException
from src.crawler_api.service.url_fetcher.base_url_fetcher import BaseUrlFetcher
from src.crawler_api.util.check_robots import CheckRobots


headers = {"User-Agent": "Mozilla/5.0"}
logger = logging.getLogger(__name__)

class HTTPXUrlFetcher(BaseUrlFetcher):

    def __init__(self):
        self._semaphore = asyncio.Semaphore(5)

    async def fetch(self, url: str) -> str | None:
        robots = CheckRobots(url)
        await robots.load()

        try:
            if not await robots.is_allowed(url):
                return None

            async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
                response = await client.get(url)

                if response.status_code != 200:
                    raise FetchValueException(f"상태코드 : {response.status_code} : {url}")
                return response.text

        except FetchValueException:
            raise

        except Exception as e:
            raise FetchValueException(str(e)) from e

    async def _fetch_one(
        self,
        client: httpx.AsyncClient,
        url: str,
        robots: CheckRobots
    ) -> str | None:

        async with self._semaphore:

            try:
                if not await robots.is_allowed(url):
                    return ""

                response = await client.get(url)

                if response.status_code != 200:
                    return ""

                return response.text

            except httpx.TimeoutException:
                return ""

            except httpx.RequestError:
                return ""

            except Exception as e:
                logger.exception("httpx fetch  all 오류 발생 : %s",e)
                return ""

            finally:
                await asyncio.sleep(random.uniform(1.5, 3.5))

    async def fetch_by_all(self, urls: list[str], base_url: str) -> list[str]:
        robots = CheckRobots(base_url)
        await robots.load()

        async with httpx.AsyncClient(headers=headers, timeout=20.0) as client:
            tasks = [self._fetch_one(client, url, robots) for url in urls]
            results = await asyncio.gather(*tasks)

        return results