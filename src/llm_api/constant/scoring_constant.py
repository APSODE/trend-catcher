class ScoringConstant:
    #신뢰도 점수 가중치 및 뉴스사 수
    CONTENT_WEIGHT = 0.35 #자체평가 점수 가중치
    CROSS_CHECK_WEIGHT = 1.0 - CONTENT_WEIGHT #중복도 점수 가중치
    CROSS_CHECK_MAX = 4  #크롤러에서 받아서 수정
