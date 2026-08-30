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
        self.tree = discord.app_commands.CommandTree(self)

    # 봇 시작 시 슬래시 커맨드 등록
    async def setup_hook(self) -> None:
        @self.tree.command(name="구독연동", description="알림 연동 상태를 다시 확인합니다")
        async def resync_subscription(interaction: discord.Interaction):
            async with AsyncSessionLocal() as session:
                try:
                    service = SubscriptionService(self.user_client)
                    await service.upsert_by_discord_id(session, str(interaction.user.id))
                    await session.commit()
                    await interaction.response.send_message(
                        "연동을 다시 확인했어요! 알림 설정이 정상적으로 반영됩니다.",
                        ephemeral=True,
                    )
                except Exception:
                    await session.rollback()
                    logger.exception("수동 재연동 실패: discord_id=%s", interaction.user.id)
                    await interaction.response.send_message(
                        "연동 확인 중 문제가 발생했어요. 프론트에서 디스코드 연동을 먼저 완료했는지 확인해주세요.",
                        ephemeral=True,
                    )

        await self.tree.sync()

    async def on_ready(self):
        logger.info("디스코드 봇 로그인 완료: %s", self.user)

    # 서버 입장시 (신규 입장자 자동 처리)
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