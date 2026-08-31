import asyncio, logging

from datetime import date
from typing import Callable, Awaitable

from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.schemas.article import ArticleCreate
from src.crawler_api.service.url_extractor.url_extractor_factory import UrlExtractorFactory
from src.crawler_api.service.url_fetcher.url_fetcher_factory import UrlFetcherFactory
from src.crawler_api.service.url_parser.url_parser_factory import UrlParserFactory
from src.crawler_api.util.normalize_datetime import now_normalized, now_date

logger = logging.getLogger(__name__)

UrlFilter = Callable[[list[str]], Awaitable[list[str]]]

#스킵할 url 생기면 여기 추가
SOURCE_SKIP_URLS: dict[NewsSitemap, list[str]] = {
    NewsSitemap.SEOUL: ["/peoples/"]
}

class CrawlingPipeline:
    """
    -> sitemap url fetch(fetch 함수)
    -> xml / page 파싱(extractor parse)
    -> 파싱한 데이터 (url list) 다시 fetch (fetch_by_all)
    -> fetch한 뉴스 기사 html 다시 파싱 (parser parse)
    """
    def __init__(self, source: NewsSitemap):
        self._source = source
        self._fetcher = UrlFetcherFactory.create(source)
        self._extractor = UrlExtractorFactory.create(source)
        self._parser = UrlParserFactory.create(source)

    async def run(
        self,
        dates: list[date],
        limit: int | None = None,
        url_filter: UrlFilter | None = None
    ) -> list[ArticleCreate]:

        if dates is None:
            return []

        skip_patterns = SOURCE_SKIP_URLS.get(self._source, [])

        try:
            urls = []
            base_url: str = ""

            for date_val in dates:
                sitemap_url = self._source.value.get_url(date_value=date_val)
                base_url = sitemap_url

                sitemap_content = await self._fetcher.fetch(sitemap_url)

                extract_urls = await self._extractor.parse(
                    raw_content=sitemap_content,
                    selector=self._source.value.selector,
                    base_url=sitemap_url
                )

                if not extract_urls:
                    continue

                if skip_patterns:
                    skip_urls = []

                    for url in extract_urls:
                        if any(pattern in url for pattern in skip_patterns):
                            logger.info("%s: skip url : %s", self._source.value.company_name, url)
                        else:
                            skip_urls.append(url)
                    extract_urls = skip_urls

                    if not extract_urls:
                        continue

                if url_filter is not None:
                    extract_urls = await url_filter(extract_urls)
                    if not extract_urls:
                        continue

                if limit is not None:
                    extract_urls = extract_urls[:limit]

                urls.extend(extract_urls)

            if not urls:
                return []

            page_contents = await self._fetcher.fetch_by_all(urls=urls, base_url=base_url)

            valid_pairs = [(url, content) for url, content in zip(urls, page_contents) if content != ""]
            if not valid_pairs:
                return []

            valid_urls = [url for url, _ in valid_pairs]
            parsed_result = await asyncio.gather(
                *(self._parser.parse(content) for _, content in valid_pairs),
                return_exceptions=True
            )

            articles : list[ArticleCreate] = []
            crawled_at = now_normalized()
            for url, parsed in zip(valid_urls, parsed_result):
                if isinstance(parsed, Exception):
                    logger.exception("parsing error occurred : %s\nurl : %s", parsed,  url)
                    continue

                if parsed is None:
                    continue

                articles.append(ArticleCreate(
                    url = url,
                    title = parsed.title.replace("\n", " "),
                    content = parsed.content.replace("\n", " "),
                    published_at = parsed.published_at,
                    crawled_at = crawled_at,
                    company_name = self._source.value.company_name,
                    reporter = parsed.reporter.replace("\n", " ") if parsed.reporter else None,
                    category = parsed.category.replace("\n", " ") if parsed.category else None,
                    img_list = parsed.img_urls)
                )

            return articles

        finally:
            if hasattr(self._fetcher, "close"): #fetcher에 close가 있는경우(selenium인 경우)
                self._fetcher.close()

    async def run_today(
            self,
            limit: int | None = None,
            url_filter: UrlFilter | None = None
    ) -> list[ArticleCreate]:
        return await self.run(dates=[now_date()], limit=limit, url_filter=url_filter)

    @staticmethod
    async def run_all(
        sources: list[NewsSitemap] | None,
        dates: list[date],
        limit: int | None = None,
        url_filter: UrlFilter | None = None
    ) ->list[ArticleCreate]:

        if not sources:
            sources = list(NewsSitemap)

        pipelines = [CrawlingPipeline(source) for source in sources]

        results = await asyncio.gather(
            *(pipe.run(dates=dates, limit=limit, url_filter=url_filter) for pipe in pipelines),
            return_exceptions=True
        )

        articles : list[ArticleCreate] = []

        for source, result in zip(sources, results):
            if isinstance(result, Exception):
                logger.exception("error occurred : %s ", result)
                continue

            articles.extend(result)

        return articles

    @staticmethod
    async def run_all_today(
        sources: list[NewsSitemap] | None = None,
        limit: int | None = None,
        url_filter: UrlFilter | None = None
    ) ->list[ArticleCreate]:

        return await CrawlingPipeline.run_all(sources=sources, dates=[now_date()], limit=limit, url_filter=url_filter)