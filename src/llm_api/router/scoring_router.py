from src.llm_api.constant.scoring_constant import ScoringConstant
from src.llm_api.dependency import ScoringServiceDep
from src.llm_api.schema.response import ScoringRunResponseData
from fastapi import APIRouter

router = APIRouter(prefix = "/scoring", tags = ["Scoring"])

@router.post("/run", response_model = ScoringRunResponseData)
async def run_scoring(service: ScoringServiceDep) -> ScoringRunResponseData:
    scored = await service.fill_scores(ScoringConstant.SCORING_LIMIT)
    return ScoringRunResponseData(scored = scored)
