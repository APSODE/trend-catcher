from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from src.llm_api.repository.news_topic_map_repository import NewsTopicMapRepository
from src.llm_api.repository.topic_repository import TopicRepository
from src.llm_api.service.embedding_service import EmbeddingService
from sqlalchemy.ext.asyncio import AsyncSession
import numpy

class HashtagSearchService:
    TOPIC_RELEVANCE_STANDARD = 0.45
    KEYWORD_RELEVANCE_STANDARD = 0.89

    def __init__(
            self,
            topic_repo: TopicRepository,
            keyword_repo: KeywordRepository,
            news_topic_map_repo: NewsTopicMapRepository,
            news_keyword_map_repo: NewsKeywordMapRepository,
            embedding_service: EmbeddingService
    ):
        self.topic_repo = topic_repo
        self.keyword_repo = keyword_repo
        self.news_topic_map_repo = news_topic_map_repo
        self.news_keyword_map_repo = news_keyword_map_repo
        self.embedding_service = embedding_service

    #검색
    async def search(self, session:AsyncSession, hashtags: list[str]) -> list[int]:
        topic_list = await self.topic_repo.get_all(session) #주제 다꺼내기
        keyword_list = await self.keyword_repo.get_all(session) #키워드 다꺼내기
        hashtag_embeddings = await self.embedding_service.get_embeddings(hashtags) #해시태그 임베딩

        matched_topic_ids = self._find_matches(hashtag_embeddings, topic_list, lambda t: t.representative_embedding, self.TOPIC_RELEVANCE_STANDARD) #주제 매칭
        matched_keyword_ids = self._find_matches(hashtag_embeddings, keyword_list, lambda k : k.embedding, self.KEYWORD_RELEVANCE_STANDARD) #해시태그 매칭

        matched_results = set() #중복x 결과담을 그릇

        #그릇에 매칭된 결과들 담기
        for topic_id in matched_topic_ids:
            matched_results.update(await self.news_topic_map_repo.get_news_by_topic(session, topic_id))
        for keyword_id in matched_keyword_ids:
            matched_results.update(await self.news_keyword_map_repo.get_news_by_keyword(session, keyword_id))

        return list(matched_results)


    #임베딩 기반 매칭: candidates는 topic도 keyword도 가능
    #numpy 너무 어려워요 선형대수학에서 배운 걸 바로 쓸 줄은 몰랐는데
    #그렇다고 for문으로 돌리면 해시태그 수십개 x 주제&키워드 수백~수천개라 연산 미쳐돌아가서 numpy 씀
    def _find_matches(self, hashtag_embeddings: list[list[float]], candidates: list, get_vector, standard: float) -> set[int]:
        #비교할게 없으면 빈 set 리턴
        if not candidates:
            return set()

        #행렬화
        candidate_matrix = numpy.array([get_vector(candidate) for candidate in candidates])
        hashtag_matrix = numpy.array(hashtag_embeddings)

        #두 행렬의 노름 구하기
        candidate_norms = numpy.linalg.norm(candidate_matrix, axis = 1)
        hashtag_norms = numpy.linalg.norm(hashtag_matrix, axis = 1)

        #유사도 구하기: 행렬 내적 / 노름 곱
        similarity_matrix = (hashtag_matrix @ candidate_matrix.T) / numpy.outer(hashtag_norms, candidate_norms)

        #기준 넘는 것들만 담아 리턴
        matched_indices = numpy.where(similarity_matrix >= standard)[1]
        result = {candidates[i].id for i in matched_indices}
        return result