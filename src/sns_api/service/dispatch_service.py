from sqlalchemy.exc import IntegrityError

from src.sns_api.handler.crawler_client import CrawlerClient
from src.sns_api.handler.discord_client import DiscordClient, PermanentWebhookError, build_payload
from src.sns_api.handler.llm_client import LLMClient
from src.sns_api.handler.user_client import UserClient
from src.sns_api.model.database_model import AsyncSessionLocal
from src.sns_api.model.entity_model import Channel, DispatchLogModel, DispatchStatus, Slot, utc_now
from src.sns_api.model.schema_model import NewsBundleData
from src.sns_api.repository.dispatch_repository import DispatchRepository
from src.sns_api.repository.subscription_repository import SubscriptionRepository

MAX_PERSONALIZED_ARTICLES = 10
MAJOR_DISPATCH_USER_ID = 0


class DispatchService:
    def __init__(self) -> None:
        self.subscription_repository = SubscriptionRepository()
        self.dispatch_repository = DispatchRepository()

    # 주요 뉴스 -> 서버 채널로 한 번 발송 (라우터가 준 세션 그대로 사용)
    async def dispatch_major(
        self,
        session,
        slot: Slot,
        slot_label: str,
        discord_client: DiscordClient,
        llm_client: LLMClient,
        crawler_client: CrawlerClient,
        channel_id: str,
    ) -> None:
        dispatch_date = utc_now().strftime("%Y-%m-%d")

        if await self.dispatch_repository.is_already_sent(
            session, MAJOR_DISPATCH_USER_ID, slot, dispatch_date
        ):
            return

        try:
            log = await self.dispatch_repository.save(
                session,
                DispatchLogModel(
                    user_id=MAJOR_DISPATCH_USER_ID,
                    subscription_id=0,
                    slot=slot.value,
                    channel=Channel.DISCORD.value,
                    dispatch_date=dispatch_date,
                    status=DispatchStatus.PENDING.value,
                ),
            )
        except IntegrityError:
            await session.rollback()
            return

        try:
            references = await llm_client.get_major_news()
            articles = await crawler_client.get_articles([ref.crawled_id for ref in references])

            items = []
            for reference in references:
                if reference.crawled_id in articles:
                    items.append(articles[reference.crawled_id])

            if not items:
                await self.dispatch_repository.mark_failed(session, log, "no_matched_articles")
                await session.commit()
                return

            bundle = NewsBundleData(major=items)
            payload = build_payload(bundle, slot_label)

            await discord_client.send_to_channel(channel_id, payload)
            await self.dispatch_repository.mark_success(session, log)
            await session.commit()

        except Exception as e:
            await self.dispatch_repository.mark_failed(session, log, str(e))
            await session.commit()

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

    # 한 명의 개인화 뉴스 처리 (독립된 세션 하나로 이 사람만 처리)
    async def _dispatch_one_personalized(
        self,
        user_id: int,
        subscription_id: int,
        discord_user_id: str | None,
        channel: str,
        slot: Slot,
        slot_label: str,
        dispatch_date: str,
        discord_client: DiscordClient,
        user_client: UserClient,
        llm_client: LLMClient,
        crawler_client: CrawlerClient,
    ) -> None:
        async with AsyncSessionLocal() as session:
            if await self.dispatch_repository.is_already_sent(session, user_id, slot, dispatch_date):
                return

            try:
                log = await self.dispatch_repository.save(
                    session,
                    DispatchLogModel(
                        user_id=user_id,
                        subscription_id=subscription_id,
                        slot=slot.value,
                        channel=channel,
                        dispatch_date=dispatch_date,
                        status=DispatchStatus.PENDING.value,
                    ),
                )
            except IntegrityError:
                await session.rollback()
                return

            try:
                hashtags = await user_client.get_user_hashtags(user_id)

                if not hashtags:
                    await self.dispatch_repository.mark_failed(session, log, "no_hashtags")
                    await session.commit()
                    return

                hashtag_to_articles = await llm_client.search_hashtags(hashtags)
                crawled_ids = self._pick_round_robin(hashtags, hashtag_to_articles, MAX_PERSONALIZED_ARTICLES)

                if not crawled_ids:
                    await self.dispatch_repository.mark_failed(session, log, "no_matched_articles")
                    await session.commit()
                    return

                articles = await crawler_client.get_articles(crawled_ids)
                items = [articles[cid] for cid in crawled_ids if cid in articles]

                if not items:
                    await self.dispatch_repository.mark_failed(session, log, "no_matched_articles")
                    await session.commit()
                    return

                if discord_user_id is None:
                    await self.dispatch_repository.mark_failed(session, log, "discord_not_linked")
                    await session.commit()
                    return

                bundle = NewsBundleData(personalized=items)
                payload = build_payload(bundle, slot_label)

                await discord_client.send_dm(discord_user_id, payload)
                await self.dispatch_repository.mark_success(session, log)
                await session.commit()

            except PermanentWebhookError as e:
                await self.dispatch_repository.mark_failed(session, log, str(e))
                sub = await self.subscription_repository.get_by_id(session, subscription_id)
                if sub:
                    sub.is_active = False
                await session.commit()

            except Exception as e:
                await self.dispatch_repository.mark_failed(session, log, str(e))
                await session.commit()

    # 개인화 뉴스 -> 구독자 각각에게 DM 발송 (유저마다 독립 세션)
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
        dispatch_date = utc_now().strftime("%Y-%m-%d")

        subscriptions = await self.subscription_repository.list_active_for_slot(session, slot)

        # 세션 넘기기 전에, 필요한 값만 미리 뽑아서 순수 데이터로 만들어둠
        targets = [
            (sub.user_id, sub.id, sub.discord_id, sub.channel)
            for sub in subscriptions
        ]

        for user_id, subscription_id, discord_user_id, channel in targets:
            await self._dispatch_one_personalized(
                user_id, subscription_id, discord_user_id, channel,
                slot, slot_label, dispatch_date,
                discord_client, user_client, llm_client, crawler_client,
            )