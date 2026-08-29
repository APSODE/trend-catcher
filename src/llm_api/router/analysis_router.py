from src.llm_api.dependency import AnalysisRunnerDep
from src.llm_api.schema.response import AnalysisRunResponseData
from fastapi import APIRouter

router = APIRouter(prefix = "/analysis", tags = ["Analysis"])

@router.post("/run", response_model = AnalysisRunResponseData)
async def run_analysis(runner: AnalysisRunnerDep) -> AnalysisRunResponseData:
    result = await runner.run()
    return AnalysisRunResponseData(total = result.total, processed = len(result.processed), skipped = result.skipped, failed = result.failed)