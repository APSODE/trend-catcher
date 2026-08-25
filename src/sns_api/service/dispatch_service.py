from src.sns_api.handler.crawler_client import CrawlerClient
from src.sns_api.handler.discord_client import DiscordClient, build_payload
from src.sns_api.handler.llm_client import LLMClient
from src.sns_api.model.schema_model import NewsBundleData
from src.sns_api.repository.dispatch_repository import DispatchRepository
from src.sns_api.repository.subscription_repository import SubscriptionRepository


class DispatchService:
    def __init__(self) -> None:
        self.subscription_repository = SubscriptionRepository()
        self.dispatch_repository = DispatchRepository()

    # 주요 뉴스 -> 서버 채널로 한 번 발송
    async def dispatch_major(
        self,
        discord_client: DiscordClient,
        llm_client: LLMClient,
        crawler_client: CrawlerClient,
        channel_id: str,
        slot_label: str,
    ) -> None:
        # LLM에게 주요뉴스 참조 받기
        references = await llm_client.get_major_news()

        # 참조 기반 크롤러로부터 주요뉴스 딕셔너리로 받기
        articles = await crawler_client.get_articles([ref.crawled_id for ref in references])

        # llm으로 받은 크롤러 아이디와 기사들의 아이디가 일치한다면 item으로 포장
        items = []
        for reference in references:
            if reference.crawled_id in articles:
                items.append(articles[reference.crawled_id])

        bundle = NewsBundleData(major=items)
        payload = build_payload(bundle, slot_label)

        # 주요뉴스 디스코드 채널 전송
        await discord_client.send_to_channel(channel_id, payload)

        # 개인화된 뉴스 DM 발송 방식