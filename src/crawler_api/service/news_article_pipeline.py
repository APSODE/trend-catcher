import asyncio
from datetime import datetime

from dns.dnssec import validate

from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.schemas.article import ArticleCreate
from src.crawler_api.service.url_extractor.url_extractor_factory import UrlExtractorFactory
from src.crawler_api.service.url_fetcher.url_fetcher_factory import UrlFetcherFactory
from src.crawler_api.service.url_parser.url_parser_factory import UrlParserFactory


class NewsArticlePipeline:
    """
    sitemap url을

    """
    def __init__(self, source : NewsSitemap):
        self.__source = source
        self.__fetcher = UrlFetcherFactory.create(source)
        self.__extractor = UrlExtractorFactory.create(source)
        self.__parser = UrlParserFactory.create(source)

    async def run(self, date: datetime, limit: int | None = None) -> list[ArticleCreate]:
        sitemap_url = self.__source.value.get_url(date)

        sitemap_content = await self.__fetcher.fetch(sitemap_url)
        urls = await self.__extractor.parse(sitemap_content, self.__source.value.selector, sitemap_url)
        if not urls:
            return []
        if limit is not None:
            urls = urls[:limit]

        page_contents = await self.__fetcher.fetch_by_all(urls, sitemap_url)

        valid_pairs = [(url, content) for url, content in zip(urls, page_contents) if content != ""]
        if not valid_pairs:
            return []

        valid_urls = [url for url, _ in valid_pairs]
        parsed_result = await asyncio.gather(*(self.__parser.parse(content) for _, content in valid_pairs), return_exceptions=True)

        articles : list[ArticleCreate] = []
        crawled_at = datetime.now()
        for url, parsed in zip(valid_urls, parsed_result):

            if isinstance(parsed, Exception):
                continue
            if parsed is None:
                continue
            articles.append(
                ArticleCreate(
                    url = url,
                    title = parsed.title.replace("\n", " "),
                    content = parsed.content.replace("\n", " "),
                    published_at = parsed.published_at,
                    crawled_at = crawled_at,
                    company_name = self.__source.value.company_name,
                    reporter = parsed.reporter.replace("\n", " ") if parsed.reporter else None,
                    category = parsed.category.replace("\n", " ") if parsed.category else None,
                    img_list = parsed.img_urls)
            )
        return articles

    async def run_today(self, limit: int | None = None) -> list[ArticleCreate]:
        return await self.run(datetime.today(), limit=limit)