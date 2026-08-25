from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from src.llm_api.constant.schedule_constant import ScheduleConstant
from src.llm_api.constant.scoring_constant import ScoringConstant
from src.llm_api.infrastructure.database import session_scope
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.repository.topic_repository import TopicRepository
from src.llm_api.service.scoring_service import ScoringService
from src.llm_api.usecase.analysis_runner import AnalysisRunner
from src.llm_api.usecase.hashtag_preparer import HashtagPreparer
import logging

logger = logging.getLogger(__name__)

#기사 분석
async def run_analysis_job(app: FastAPI) -> None:
    runner = AnalysisRunner(app.state.crawler_client, app.state.nvidia_client)
    result = await runner.run()
    logger.info("정기 분석 완료: 처리 %d건, 스킵 %d건, 실패 %d건", len(result.processed), result.skipped, result.failed)

#해시태그 확장
async def run_hashtag_prepare_job(app: FastAPI) -> None:
    preparer = HashtagPreparer(app.state.user_api_client, app.state.nvidia_client)
    result = await preparer.run()
    logger.info("정기 확장 완료: 신규 %d건, 실패 %d건", result.prepared, result.failed)

#점수 산정
async def run_scoring_job() -> None:
    async with session_scope() as session:
        service = ScoringService(NewsAnalysisRepository(session), TopicRepository(session))
        scored = await service.fill_scores(ScoringConstant.SCORING_LIMIT)
    logger.info("정기 점수 산정 완료: %d건", scored)

#스케줄러
def init_scheduler(app: FastAPI) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone = ScheduleConstant.TIMEZONE)

    #정기 분석
    scheduler.add_job(
        run_analysis_job,
        CronTrigger(hour = ScheduleConstant.ANALYSIS_HOURS, minute = ScheduleConstant.ANALYSIS_FIRST_MINUTE),
        args = [app],
        max_instances = 1,
        id = "analysis_first"
    )

    #실패 대비 2차분석
    scheduler.add_job(
        run_analysis_job,
        CronTrigger(hour = ScheduleConstant.ANALYSIS_HOURS, minute = ScheduleConstant.ANALYSIS_SECOND_MINUTE),
        args = [app],
        max_instances = 1,
        id = "analysis_second"
    )

    #해시태그 준비
    scheduler.add_job(
        run_hashtag_prepare_job,
        CronTrigger(hour = ScheduleConstant.HASHTAG_HOURS, minute = ScheduleConstant.HASHTAG_MINUTE),
        args = [app],
        max_instances = 1,
        id = "hashtag_prepare"
    )

    #점수산정
    scheduler.add_job(
        run_scoring_job,
        CronTrigger(hour = ScheduleConstant.SCORING_HOURS, minute = ScheduleConstant.SCORING_MINUTE),
        max_instances = 1,
        id = "scoring"
    )

    return scheduler