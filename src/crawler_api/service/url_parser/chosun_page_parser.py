from datetime import datetime

from bs4 import BeautifulSoup
from src.crawler_api.service.url_parser.base_page_parser import BasePageParser, ParsedData


class ChosunPageParser(BasePageParser):
    async def parse(self, content: str) -> ParsedData | None:
        soup = BeautifulSoup(content, "html.parser")

        title = soup.select_one(
            "#fusion-app > div.article.\\| > div:nth-child(2) > div > div > div.article-header__headline-container.\\|.box--pad-left-md.box--pad-right-md > h1 > span"
        )
        date = soup.select_one(
            "#fusion-app > div:nth-of-type(1) > div:nth-of-type(2) > div > section > article > div:nth-of-type(1) > div:nth-of-type(2) > span > span:nth-of-type(1)"
        )

        section = soup.select_one(
            "#fusion-app > div.article.\\| > div:nth-child(2) > div > section > article > section"
        )

        category = soup.select_one(
            "a.flex.flex--align-items-center.font--size-md-18.font--primary.text--line-height-1\\.43.text--black"
        )

        reporter = soup.select_one(
            "#fusion-app > div:nth-of-type(1) > div:nth-of-type(2) > div > section > article > div:nth-of-type(1) > div:nth-of-type(1) > div > a"
        )

        if not title or not section:
            return None
        img_urls = []
        for img in section.find_all("img"):
            src = img.get("src")
            if src:
                img_urls.append(src)
        published_at = None

        if date:
            date_text = date.get_text(strip=True).replace("입력", "").strip()
            try:
                published_at = datetime.strptime(date_text, "%Y.%m.%d. %H:%M")
            except ValueError:
                pass
        return ParsedData(
            title=title.get_text(strip=True),
            content=section.get_text(strip=True),
            reporter=reporter.get_text(strip=True) if reporter else None,
            category=category.get_text(strip=True) if category else None,
            published_at=published_at,
            img_urls=img_urls)

"""
TODO : 기자가 리다이렉팅이 안되는 경우 기자이름을 못받아옴
"""