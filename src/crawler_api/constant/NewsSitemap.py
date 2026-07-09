from datetime import datetime
from dataclasses import dataclass
from enum import Enum, auto

from src.crawler_api.exception.SelectorValueException import SelectorValueError


class SitemapType(Enum):
    XML = auto()
    PAGE = auto()


@dataclass(frozen=True)
class NewsUrlData:
    url : str
    kr_name : str
    sitemap_type : SitemapType
    selector : str | None = None

    """
    날짜마다 URL이 달라지는 경우가 있음으로 무조건 value.get_url 사용
    """

    def __post_init__(self):
        if self.sitemap_type == SitemapType.PAGE and self.selector is None:
            raise SelectorValueError("페이지 타입에 셀렉터가 존재하지 않습니다")
        if self.sitemap_type != SitemapType.PAGE and self.selector:
            raise SelectorValueError("페이지 타입이 아닌 값에 셀렉터가 존재합니다")

    def get_url(self, date : datetime = datetime.today()):
        return self.url.format(
            yyyy = date.strftime("%Y"),
            yyyymmdd = date.strftime("%Y%m%d"),
            mm = date.strftime("%m"),
            dd = date.strftime("%d")
        )

class NewsSitemap(Enum):

    #DONGA = NewsURLData(
    #    "https://www.donga.com/sitemap/donga-newsmap.xml",
    #    "동아일보",
    #    SitemapType.DATE_IN_NEWS) #일간

    DONGA_PAGE = NewsUrlData(
        "https://www.donga.com/news/sitemap?p1={yyyy}&p2={mm}&p3={dd}",
        "동아일보",
        SitemapType.PAGE,
        "#contents > div > div > div.sitemap_list.contents_list > div > ul li a"
)

    #CHOSUN = NewsURLData(
    #    "https://www.chosun.com/arc/outboundfeeds/news-sitemap/?outputType=xml",
    #    "조선일보",
    #    SitemapType.DATE_IN_URL)  # 최신순

    CHOSUN_PAGE = NewsUrlData(
        "https://www.chosun.com/sitemap/{yyyy}/{mm}/{dd}/",
        "조선일보",
        SitemapType.PAGE,
        "#fusion-app > div:nth-child(2) > div > div > section > div > div:nth-child(5) > div")


    KMIB = NewsUrlData(
        "https://www.kmib.co.kr/rss/data/sitemap/daily/{yyyy}/{mm}/dailyArticleList_{yyyymmdd}.xml",
        "국민일보",
        SitemapType.XML)  # 일간


    MUNHWA = NewsUrlData(
        "https://www.munhwa.com/sitemap/articles/{yyyy}/{yyyymmdd}",
        "문화일보",
        SitemapType.XML)


    #SEGYE = NewsURLData(
    #    "https://www.segye.com/sitemap_day0.xml",
    #    "세계일보",
    #    SitemapType.DATE_IN_NEWS) # 일간


    JOONGANG = NewsUrlData(
        "https://www.joongang.co.kr/sitemap/articles/{yyyy}/{yyyymmdd}",
        "중앙일보",
        SitemapType.XML)  # 일간


    HANKOOK = NewsUrlData(
        "https://www.hankookilbo.com/sitemap/daily-articles/{yyyymmdd}",
        "한국일보",
        SitemapType.XML)  # 일간

    SEOUL_PAGE = NewsUrlData(
        "https://www.seoul.co.kr/sitemap/sitemap_index_{yyyymmdd}",
        "서울신문",
        SitemapType.PAGE,
        "#articleArea > ul li a")


