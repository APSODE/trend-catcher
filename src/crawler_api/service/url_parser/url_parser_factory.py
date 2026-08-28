from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.exception.unsupported_site_exception import UnsupportedSiteException
from src.crawler_api.service.url_parser.base_page_parser import BasePageParser
from src.crawler_api.service.url_parser.chosun_page_parser import ChosunPageParser
from src.crawler_api.service.url_parser.donga_page_parser import DongaPageParser
from src.crawler_api.service.url_parser.joongang_page_parser import JoongangPageParser
from src.crawler_api.service.url_parser.kmib_page_parser import KMIBPageParser
from src.crawler_api.service.url_parser.munhwa_page_parser import MunhwaPageParser
from src.crawler_api.service.url_parser.seoul_page_parser import SeoulPageParser

_PARSER_MAP: dict[NewsSitemap, type[BasePageParser]] = {
    # NewsSitemap.CHOSUN: ChosunPageParser,
    NewsSitemap.MUNHWA: MunhwaPageParser,
    NewsSitemap.JOONGANG: JoongangPageParser,
    NewsSitemap.SEOUL: SeoulPageParser,
    NewsSitemap.DONGA: DongaPageParser,
    # NewsSitemap.KMIB: KMIBPageParser,
}

class UrlParserFactory:
    @staticmethod
    def create(source: NewsSitemap) -> BasePageParser:
        parser_class = _PARSER_MAP.get(source)
        if parser_class is None:
            raise UnsupportedSiteException()
        return parser_class()