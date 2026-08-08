import numpy as np


class SimilarityUtil:
    #벡터 두개 비교
    @staticmethod
    def get_cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
        a, b = np.array(vec_a), np.array(vec_b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    #후보 중 가장 비슷한 대상 찾기
    @staticmethod
    def find_most_similar(target: list[float], candidates: list[list[float]]) -> tuple[int, float] | None:
        if not candidates:
            return None

        similarity_matrix = SimilarityUtil._get_cosine_similarities(target, candidates)
        
        best_index = int(np.argmax(similarity_matrix)) #최댓값 인덱스 꺼내기
        return best_index, float(similarity_matrix[best_index])
    
    #후보 중 특정 기준 이상 비슷한 대상 찾기
    @staticmethod
    def find_similar_above(target: list[float], candidates: list[list[float]], threshold: float) -> list[tuple[int, float]]:
        if not candidates:
            return []
        
        similarity_matrix = SimilarityUtil._get_cosine_similarities(target, candidates)

        matched_indices = np.where(similarity_matrix >= threshold)[0]
        return [(int(idx), float(similarity_matrix[idx])) for idx in matched_indices]
        
    #다중 벡터 계산
    @staticmethod
    def _get_cosine_similarities(target:list[float], candidates: list[list[float]]) -> np.ndarray:
        #매트릭스화
        target_vec = np.array(target)
        matrix = np.array(candidates)

        # 정규화
        target_norm = target_vec / np.linalg.norm(target_vec)
        matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)

        similarity_matrix = matrix_norm @ target_norm #내적 = 유사도
        return similarity_matrix