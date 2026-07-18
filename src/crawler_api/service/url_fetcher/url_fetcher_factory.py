from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.service.url_fetcher.base_url_fetcher import BaseUrlFetcher
from src.crawler_api.service.url_fetcher.httpx_url_fetcher import HTTPXUrlFetcher
from src.crawler_api.service.url_fetcher.selenium_url_fetcher import SeleniumURLFetcher

_PAGE_SELENIUM : set[NewsSitemap] = {
    NewsSitemap.CHOSUN_PAGE
}

class UrlFetcherFactory:
    @staticmethod
    def create(source : NewsSitemap) -> BaseUrlFetcher:
        if source in _PAGE_SELENIUM:
            return SeleniumURLFetcher()
        return HTTPXUrlFetcher()