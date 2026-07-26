class ReliabilityService:
    CONTENT_WEIGHT = 0.35
    CROSS_CHECK_WEIGHT = 0.65
    CROSS_CHECK_MAX = 6  # TODO: 돌려보며 조정필요

    #중복점수 계산
    def calculate_cross_check_score(self, topic_count: int) -> float:
        return min(topic_count / self.CROSS_CHECK_MAX, 1.0)

    #최종점수 계산
    def calculate_final_score(self, content_score: float, topic_count: int) -> dict:
        cross_check_score = self.calculate_cross_check_score(topic_count)
        final_score = self.CONTENT_WEIGHT * content_score + self.CROSS_CHECK_WEIGHT * cross_check_score
        return {
            "score" : final_score,
            "score_detail" : {
                "content_score" : content_score,
                "cross_check_score" : cross_check_score,
                "weights" : {
                    "content" : self.CONTENT_WEIGHT,
                    "cross_check" : self.CROSS_CHECK_WEIGHT
                }
            }
        }
