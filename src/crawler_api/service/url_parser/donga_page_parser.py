from datetime import datetime
from bs4 import BeautifulSoup

from src.crawler_api.service.url_parser.base_page_parser import BasePageParser, ParsedData
from src.crawler_api.util.normalize_datetime import normalize_datetime


class DongaPageParser(BasePageParser):
    async def parse(self, content: str) -> ParsedData | None:
        soup = BeautifulSoup(content, "html.parser")

        title = soup.select_one("#contents > header > div > section > h1")

        date = soup.select_one("#contents > header > div > section > div.view_news_info > ul > li:nth-child(2) > button > span:nth-child(1)")

        section = soup.select_one("#contents > div:nth-of-type(2) > div > div:nth-of-type(1) > section:nth-of-type(1)")

        category = soup.select_one("#contents > header > div > section > nav > ol > li > a")

        reporter = soup.select_one("#contents > header > div > section > article > a")

        if not title or not section:
            return None

        img_urls = []
        for img in section.find_all("img"):
            src = img.get("src")
            if src:
                img_urls.append(src)

        published_at = None
        if date:
            date_text = date.get_text(strip=True)
            try:
                published_at = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
            except ValueError:
                pass

        return ParsedData(
            title=title.get_text(strip=True),
            content=" ".join(p.strip() for p in section.find_all(string=True, recursive=False) if p.strip()),
            reporter=reporter.get_text(strip=True) if reporter else None,
            category=category.get_text(strip=True) if category else None,
            published_at=normalize_datetime(published_at) if published_at else None,
            img_urls=img_urls
        )