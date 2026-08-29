import logging

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import get_settings

settings = get_settings()
logger = logging.getLogger("sns.scheduler")


async def _trigger_dispatch(slot: str) -> None:
    # 60초까지 응답 기다리기
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{settings.self_base_url}/dispatch/{slot}",
                headers={"X-Internal-Token": settings.internal_token},
            )
            response.raise_for_status()
            logger.info("dispatch triggered: slot=%s status=%s", slot, response.status_code)
        except Exception:
            logger.exception("dispatch trigger failed: slot=%s", slot)


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=settings.timezone)
    # 오전 9시
    scheduler.add_job(
        _trigger_dispatch,
        trigger=CronTrigger.from_crontab(settings.morning_cron),
        args=["MORNING"],
        id="morning_dispatch",
        replace_existing=True,
    )
    # 오후 9시
    scheduler.add_job(
        _trigger_dispatch,
        trigger=CronTrigger.from_crontab(settings.evening_cron),
        args=["EVENING"],
        id="evening_dispatch",
        replace_existing=True,
    )
    return scheduler