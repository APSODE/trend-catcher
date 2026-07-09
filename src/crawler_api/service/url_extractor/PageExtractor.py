
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from src.crawler_api.exception.SelectorValueException import SelectorValueException
from src.crawler_api.service.url_extractor.BaseExtractor import BaseExtractor


class PageExtractor(BaseExtractor):
    async def parse(
            self,
            raw_content : str,
            selector : str | None = None,
            base_url : str | None = None) -> list[str]:
        if not selector or not base_url:
            raise SelectorValueException()

        soup = BeautifulSoup(raw_content, "html.parser")
        items = soup.select(selector)

        urls : list[str] = []
        seen : set[str] = set()

        for item in items:
            url = item.get("href")

            # url 비어있는경우
            if not url:
                continue

            absolute_url = urljoin(base_url, url)
            if absolute_url not in seen:
                seen.add(absolute_url)
                urls.append(absolute_url)

        return urls


