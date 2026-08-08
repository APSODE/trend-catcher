from src.crawler_api.constant.news_sitemap import NewsSitemap, SitemapType
from src.crawler_api.service.url_extractor.page_extractor import PageExtractor
from src.crawler_api.service.url_extractor.xml_extractor import XMLExtractor


class UrlExtractorFactory:
    @staticmethod
    def create(source : NewsSitemap):
        if source.value.sitemap_type == SitemapType.XML:
            return XMLExtractor()
        return PageExtractor()