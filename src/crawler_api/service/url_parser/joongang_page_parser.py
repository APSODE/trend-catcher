from datetime import datetime

from bs4 import BeautifulSoup
from src.crawler_api.service.url_parser.base_page_parser import BasePageParser, ParsedData


class JoongangPageParser(BasePageParser):
    async def parse(self, content: str) -> ParsedData | None:
        soup = BeautifulSoup(content, "html.parser")

        title = soup.select_one("#container > section > article > header > h1")

        date = soup.select_one("time[itemprop='datePublished']")

        section = soup.select_one("#article_body")

        category = soup.select_one("#container > section > article > header > div.subhead > a.title")

        reporter = soup.select_one("#container > section > article > header > div.byline > a")

        if not title or not section:
            return None

        img_urls = []
        for img in section.find_all("img"):
            src = img.get("src")
            if src:
                img_urls.append(src)

        published_at = None
        if date:
           published_at = datetime.fromisoformat(date.get("datetime"))

        return ParsedData(
            title=title.get_text(strip=True),
            content=section.get_text(strip=True),
            reporter=reporter.get_text(strip=True) if reporter else None,
            category=category.get_text(strip=True) if category else None,
            published_at=published_at,
            img_urls=img_urls)