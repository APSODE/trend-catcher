import asyncio
import os
from dotenv import load_dotenv

from service.extraction_service import ExtractionService
from service.embedding_service import EmbeddingService
from service.reliability_service import ReliabilityService

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("NVIDIA_API_KEY")


async def main():
    extraction = ExtractionService(API_KEY)
    embedding = EmbeddingService(API_KEY)
    reliability = ReliabilityService()

    # 1. 추출 서비스 확인
    result = await extraction.extract(
        title="한국은행, 기준금리 3.5%로 동결",
        content="한국은행 금융통화위원회는 15일 기준금리를 현 3.5%로 유지하기로 결정했다. 물가 상승률 둔화와 경기 둔화 우려를 동시에 반영한 결정으로 풀이된다.",
    )
    print("추출 결과:", result)

    # 2. 임베딩 + 유사도 확인
    embeddings = await embedding.get_embeddings([
        "한국은행, 기준금리 3.5%로 동결",
        "손흥민, 프리미어리그 이번 시즌 첫 골 기록",
    ])
    sim = embedding.cosine_similarity(embeddings[0], embeddings[1])
    print("유사도:", sim, "판정:", embedding.classify_similarity(sim))

    # 3. 신뢰도 계산 확인 (추출 결과의 content_score + 가상의 topic_count 사용)
    if result:
        score_result = reliability.calculate_final_score(result["content_score"], topic_count=3)
        print("최종 점수:", score_result)

    await extraction.close()
    await embedding.close()


if __name__ == "__main__":
    asyncio.run(main())