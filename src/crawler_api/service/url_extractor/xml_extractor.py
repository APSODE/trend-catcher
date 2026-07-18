from bs4 import BeautifulSoup

from src.crawler_api.service.url_extractor.base_extractor import BaseExtractor

class XMLExtractor(BaseExtractor):
    async def parse(
            self,
            raw_content : str,
            selector : str | None = None,
            base_url : str | None = None) -> list[str]:
        soup = BeautifulSoup(raw_content, "xml")
        items : list[str] = []
        seems : set[str] = set()
        for item in soup.find_all("url"):
            loc = item.find("loc")
            if not loc:
                continue
            loc = loc.text.strip()
            if loc not in seems:
                seems.add(loc)
                items.append(loc)
        return items
