import re
from datetime import datetime
from bs4 import BeautifulSoup

from src.crawler_api.service.url_parser.base_page_parser import BasePageParser, ParsedData
from src.crawler_api.util.normalize_datetime import normalize_datetime


class KMIBPageParser(BasePageParser):
    async def parse(self, content: str) -> ParsedData | None:
        soup = BeautifulSoup(content, "html.parser")

        title = soup.select_one("#article_header > h1")

        date = soup.select_one("#article_header > div.flex.flex_fw.flex_jcsb.flex_aicn.rgap_xs2 > div.datetime.flex.flex_xscol.fs_lg14.lh_lg15.gray500.cgap_lg2.ls-2 > div > span")

        section = soup.select_one("#articleBody")
        if not title or not section:
            return None

        category = None
        content = " ".join(p.strip() for p in section.find_all(string=True, recursive=False) if p.strip())
        matches = re.search(r'([가-힣]{2,6}\s*[가-힣\s·]*기자)', content)
        reporter = matches.group(1) if matches else None

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
            content=content,
            reporter=reporter if reporter else None,
            category=category,
            published_at=normalize_datetime(published_at) if published_at else None,
            img_urls=img_urls
        )