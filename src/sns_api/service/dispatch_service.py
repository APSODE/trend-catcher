from datetime import datetime

from src.sns_api.handler.crawler_client import CrawlerClient
from src.sns_api.handler.discord_client import DiscordClient, PermanentWebhookError, build_payload
from src.sns_api.handler.llm_client import LLMClient
from src.sns_api.handler.user_client import UserClient
from src.sns_api.model.entity_model import DispatchLogModel, DispatchStatus, Slot
from src.sns_api.model.schema_model import NewsBundleData
from src.sns_api.repository.dispatch_repository import DispatchRepository
from src.sns_api.repository.subscription_repository import SubscriptionRepository

# 개인화 뉴스 최대 개수
MAX_PERSONALIZED_ARTICLES = 10


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

    # 해시태그별로 한바퀴씩 돌면서 기사 뽑기
    @staticmethod
    def _pick_round_robin(
        hashtags: list[str], hashtag_to_articles: dict[str, list[str]], limit: int
    ) -> list[str]:
        tag_queues = [list(hashtag_to_articles.get(tag, [])) for tag in hashtags]

        crawled_ids: list[str] = []
        seen: set[str] = set()

        while len(crawled_ids) < limit and any(tag_queues):
            for queue in tag_queues:
                if not queue:
                    continue
                cid = queue.pop(0)
                if cid not in seen:
                    crawled_ids.append(cid)
                    seen.add(cid)
                    if len(crawled_ids) >= limit:
                        break

        return crawled_ids

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

        # LLM에 해시태그별 매칭된 기사 목록
        hashtag_to_articles = await llm_client.get_latest_hashtags()

        subscriptions = await self.subscription_repository.list_active_for_slot(session, slot)

        # 구독자 순회하며 구독자의 해시태그 파악
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
                hashtags = await user_client.get_user_hashtags(sub.user_id)

                # 해시태그별로 한바퀴씩 돌면서 기사 뽑기
                crawled_ids = self._pick_round_robin(hashtags, hashtag_to_articles, MAX_PERSONALIZED_ARTICLES)

                if not crawled_ids:
                    await self.dispatch_repository.mark_failed(session, log, "no_matched_articles")
                    continue

                articles = await crawler_client.get_articles(crawled_ids)

                items = [articles[cid] for cid in crawled_ids if cid in articles]

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