from datetime import datetime
from dataclasses import dataclass
from enum import Enum, auto


class SitemapType(Enum):
    DATE_IN_NEWS = auto()
    DATE_IN_URL = auto()
    ONLY_URL = auto()


@dataclass(frozen=True)
class NewsURLData:
    url : str
    kr_name : str
    sitemap_type : SitemapType

    """
    날짜마다 URL이 달라지는 경우가 있음으로 무조건 value.get_url 사용
    """

    @property
    def get_url(self):
        today = datetime.today()
        if self.sitemap_type == SitemapType.ONLY_URL:
            return self.url.format(
                yyyy = today.strftime("%Y"),
                yyyymmdd = today.strftime("%Y%m%d"),
                mm = today.strftime("%m")
            )
        return self.url





class NewsSitemap(Enum):
    KHAN = NewsURLData("https://www.khan.co.kr/sitemap/latest-articles.xml", "경향신문",
                       SitemapType.DATE_IN_URL) #최신순

    DONGA = NewsURLData("https://www.donga.com/sitemap/donga-newsmap.xml", "동아일보",
                        SitemapType.DATE_IN_NEWS) #일간

    CHOSUN = NewsURLData("https://www.chosun.com/arc/outboundfeeds/news-sitemap/?outputType=xml", "조선일보",
                         SitemapType.DATE_IN_URL)  # 최신순

    KMIB = NewsURLData("https://www.kmib.co.kr/rss/data/sitemap/daily/{yyyy}/{mm}/dailyArticleList_{yyyymmdd}.xml", "국민일보",
                             SitemapType.ONLY_URL)  # 일간
    #날짜 알고리즘

    MUNHWA = NewsURLData("https://www.munhwa.com/sitemap/articles/{yyyy}/{yyyymmdd}", "문화일보",
                               SitemapType.ONLY_URL)

    #날짜 알고리즘

    SEGYE = NewsURLData("https://www.segye.com/sitemap_day0.xml", "세계일보",
                        SitemapType.DATE_IN_NEWS) # 일간


    JOONGANG = NewsURLData("https://www.joongang.co.kr/sitemap/articles/{yyyy}/{yyyymmdd}", "중앙일보",
                                 SitemapType.ONLY_URL)  # 일간
    #날짜 알고리즘

    HANKOOK = NewsURLData("https://www.hankookilbo.com/sitemap/daily-articles/{yyyymmdd}", "한국일보",
                                SitemapType.ONLY_URL)  # 일간

    #날짜 알고리즘
