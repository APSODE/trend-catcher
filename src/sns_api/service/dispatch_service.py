from datetime import datetime

from src.sns_api.handler.crawler_client import CrawlerClient
from src.sns_api.handler.discord_client import DiscordClient, PermanentWebhookError, build_payload
from src.sns_api.handler.llm_client import LLMClient
from src.sns_api.handler.user_client import UserClient
from src.sns_api.model.entity_model import DispatchLogModel, DispatchStatus, Slot
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
        references = await llm_client.get_major_news()
        articles = await crawler_client.get_articles([ref.crawled_id for ref in references])

        items = []
        for reference in references:
            if reference.crawled_id in articles:
                items.append(articles[reference.crawled_id])

        bundle = NewsBundleData(major=items)
        payload = build_payload(bundle, slot_label)

        await discord_client.send_to_channel(channel_id, payload)

    # 개인화 뉴스 -> 구독자 각각에게 DM 발송
    async def dispatch_personalized(
        self,
        session,
        slot: Slot,
        slot_label: str,
        discord_client: DiscordClient,
        user_client: UserClient,
        llm_client: LLMClient,
        crawler_client: CrawlerClient,
    ) -> None:
        dispatch_date = datetime.now().strftime("%Y-%m-%d")

        # 해시태그별 매칭된 기사 목록
        hashtag_to_articles = await llm_client.get_latest_hashtags()

        subscriptions = await self.subscription_repository.list_active_for_slot(session, slot)

        for sub in subscriptions:
            if await self.dispatch_repository.is_already_sent(session, sub.user_id, slot, dispatch_date):
                continue

            log = await self.dispatch_repository.save(
                session,
                DispatchLogModel(
                    user_id=sub.user_id,
                    subscription_id=sub.id,
                    slot=slot.value,
                    channel=sub.channel,
                    dispatch_date=dispatch_date,
                    status=DispatchStatus.PENDING.value,
                ),
            )

            try:
                # 이 유저의 팔로우 해시태그 조회
                hashtags = await user_client.get_user_hashtags(sub.user_id)

                # 해시태그로 매칭된 크롤러 아이디 모으기
                crawled_ids = set()
                for tag in hashtags:
                    crawled_ids.update(hashtag_to_articles.get(tag, []))

                if not crawled_ids:
                    await self.dispatch_repository.mark_failed(session, log, "no_matched_articles")
                    continue

                articles = await crawler_client.get_articles(list(crawled_ids))
                items = list(articles.values())

                # 캐싱된 discord_id 사용
                discord_user_id = sub.discord_id
                if discord_user_id is None:
                    await self.dispatch_repository.mark_failed(session, log, "discord_not_linked")
                    continue

                bundle = NewsBundleData(personalized=items)
                payload = build_payload(bundle, slot_label)

                await discord_client.send_dm(discord_user_id, payload)
                await self.dispatch_repository.mark_success(session, log)

            except PermanentWebhookError as e:
                await self.dispatch_repository.mark_failed(session, log, str(e))
                sub.is_active = False
                await session.flush()

            except Exception as e:
                await self.dispatch_repository.mark_failed(session, log, str(e))