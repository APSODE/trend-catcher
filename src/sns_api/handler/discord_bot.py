import logging

import discord

from src.sns_api.handler.user_client import UserClient
from src.sns_api.model.database_model import AsyncSessionLocal
from src.sns_api.service.subscription_service import SubscriptionService

logger = logging.getLogger("sns.bot")

intents = discord.Intents.default()
intents.members = True


class SNSBot(discord.Client):
    def __init__(self, user_client: UserClient, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user_client = user_client

    async def on_ready(self):
        logger.info("디스코드 봇 로그인 완료: %s", self.user)

    # 서버 입장시
    async def on_member_join(self, member: discord.Member):
        async with AsyncSessionLocal() as session:
            try:
                service = SubscriptionService(self.user_client)
                await service.upsert_by_discord_id(session, str(member.id))
                await session.commit()
            except Exception:
                await session.rollback()
                logger.exception("구독 생성/재활성화 실패: discord_id=%s", member.id)

    # 서버 퇴장시
    async def on_member_remove(self, member: discord.Member):
        async with AsyncSessionLocal() as session:
            try:
                service = SubscriptionService(self.user_client)
                await service.deactivate_by_discord_id(session, str(member.id))
                await session.commit()
            except Exception:
                await session.rollback()
                logger.exception("구독 비활성화 실패: discord_id=%s", member.id)