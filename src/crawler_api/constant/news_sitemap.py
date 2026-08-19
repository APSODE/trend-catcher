from datetime import datetime, date
from enum import Enum, auto
from pydantic import BaseModel

from src.crawler_api.exception.selector_value_exception import SelectorValueException
from src.crawler_api.util.normalize_datetime import now_date


class SitemapType(Enum):
    XML = auto()
    PAGE = auto()


class NewsUrlData(BaseModel):
    url: str
    company_name: str
    sitemap_type: SitemapType
    selector: str | None = None

    """
    날짜마다 URL이 달라지는 경우가 있음으로 무조건 value.get_url 사용
    """

    def __post_init__(self):
        if self.sitemap_type == SitemapType.PAGE and self.selector is None:
            raise SelectorValueException()

        if self.sitemap_type != SitemapType.PAGE and self.selector:
            raise SelectorValueException()

    def get_url(self, date_value: date = now_date()):
        return self.url.format(
            yyyy=date_value.strftime("%Y"),
            yyyymmdd=date_value.strftime("%Y%m%d"),
            mm=date_value.strftime("%m"),
            dd=date_value.strftime("%d")
        )

class NewsSitemap(Enum):

    #DONGA_PAGE = NewsUrlData(
    #    url="https://www.donga.com/news/sitemap?p1={yyyy}&p2={mm}&p3={dd}",
    #    company_name="동아일보",
    #    sitemap_type=SitemapType.PAGE,
    #    selector="#contents > div > div > div.sitemap_list.contents_list > div > ul li a")

    CHOSUN_PAGE = NewsUrlData(
        url="https://www.chosun.com/sitemap/{yyyy}/{mm}/{dd}/",
        company_name="조선일보",
        sitemap_type=SitemapType.PAGE,
        selector="a.story-card__headline")


    #KMIB = NewsUrlData(
    #    url="https://www.kmib.co.kr/rss/data/sitemap/daily/{yyyy}/{mm}/dailyArticleList_{yyyymmdd}.xml",
    #    company_name="국민일보",
    #    sitemap_type=SitemapType.XML) # 일간

    MUNHWA = NewsUrlData(
        url="https://www.munhwa.com/sitemap/articles/{yyyy}/{yyyymmdd}",
        company_name="문화일보",
        sitemap_type=SitemapType.XML)


    #SEGYE = NewsURLData(
    #    url="https://www.segye.com/sitemap_day0.xml",
    #    company_name="세계일보",
    #    sitemap_type=SitemapType.DATE_IN_NEWS) # 일간

    #AI봇 많이 차단
    JOONGANG = NewsUrlData(
        url="https://www.joongang.co.kr/sitemap/articles/{yyyy}/{yyyymmdd}",
        company_name="중앙일보",
        sitemap_type=SitemapType.XML)  # 일간

    #AI 학습용 데이터 크롤링 금지
    #HANKOOK = NewsUrlData(
    #    url="https://www.hankookilbo.com/sitemap/daily-articles/{yyyymmdd}",
    #    company_name="한국일보",
    #    sitemap_type=SitemapType.XML)  # 일간

    #SEOUL_PAGE = NewsUrlData(
    #    url="https://www.seoul.co.kr/sitemap/sitemap_index_{yyyymmdd}",
    #    company_name="서울신문",
    #    sitemap_type=SitemapType.PAGE_HTTPX,
    #    selector="#articleArea > ul li a")

    #후보
    #조선일보
    #문화일보
    #mbn <- ai 규제 심함
    #중앙일보 <- ai 규제 심함