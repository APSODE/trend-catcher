import httpx
from src.crawler_api.exception.FetchValueException import FetchValueException
from src.crawler_api.service.url_extractor.BaseUrlFetcher import BaseUrlFetcher

headers = {"User-Agent": "Mozilla/5.0"}

class HTTPXUrlFetcher(BaseUrlFetcher):

    async def fetch(self, url: str) -> str:
        try:
            response = httpx.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception()
            return response.text
        except Exception as e:
            raise FetchValueException("Fetch 과정에서 문제가 발생했습니다" + "\n" + e.__str__())

    async def fetch_base_url(self, urls: list[str]) -> list[str]:
        results = []
        try:
            for i in urls:
                response = httpx.get(i, headers=headers)
                if response.status_code != 200:
                    continue
                results.append(response.text)
        except Exception as e:
            raise FetchValueException("Fetch 과정에서 문제가 발생했습니다" + "\n" + e.__str__())
        finally:
            return results
