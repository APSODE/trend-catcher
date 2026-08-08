from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.exception.unsupported_site_exception import UnsupportedSiteException
from src.crawler_api.service.url_parser.base_page_parser import BasePageParser
from src.crawler_api.service.url_parser.chosun_page_parser import ChosunPageParser
from src.crawler_api.service.url_parser.joongang_page_parser import JoongangPageParser
from src.crawler_api.service.url_parser.munhwa_page_parser import MunhwaPageParser

_PARSER_MAP : dict[NewsSitemap, type[BasePageParser]] = {
    NewsSitemap.CHOSUN_PAGE : ChosunPageParser,
    NewsSitemap.MUNHWA : MunhwaPageParser,
    NewsSitemap.JOONGANG : JoongangPageParser
}

class UrlParserFactory:
    @staticmethod
    def create(source : NewsSitemap) -> BasePageParser:
        parser_class = _PARSER_MAP.get(source)
        if parser_class is None:
            raise UnsupportedSiteException()
        return parser_class()