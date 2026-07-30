from datetime import datetime

from bs4 import BeautifulSoup
from src.crawler_api.service.url_parser.base_page_parser import BasePageParser, ParsedData


class MunhwaPageParser(BasePageParser):
    async def parse(self, content: str) -> ParsedData | None:
        soup = BeautifulSoup(content, "html.parser")

        title = soup.select_one("#container > div.inner > div > header > h1")
        date = soup.select_one("#container > div.inner > div > header > div.article-header-bottom > div.byline > p.date-publish")

        section = soup.select_one("#article-body")

        category = soup.select_one("#container > div.inner > div > header > div.section-title > a.depth1")

        reporter = soup.select_one("#container > div.inner > div > header > div.article-header-bottom > div.byline > p.writer > span > a")

        if not title or not section:
            #raise ParsingFailException("문화일보 제목이나 내용이 존재하지않습니다")
            return None

        img_urls = []

        for img in section.select("figure img"):
            src = img.get("src")
            if not src:
                continue
            if "1X1.png" in src:
                src = img.get("data-thum")
            img_urls.append(src)

        published_at = None

        if date:
            date_text = date.get_text(strip=True).replace("입력", "").strip()
            try:
                published_at = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
            except ValueError:
                pass
        return ParsedData(
            title=title.get_text(strip=True),
            content=" ".join(p.get_text(strip = True) for p in section.find_all("p") if p.get_text(strip = True)),
            reporter=reporter.get_text(strip=True) + " 기자" if reporter else None,
            category=category.get_text(strip=True) if category else None,
            published_at=published_at,
            img_urls=img_urls)