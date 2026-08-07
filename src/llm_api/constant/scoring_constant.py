class ScoringConstant:
    #주제 유사도 기준
    TOPIC_SIMILARITY_THRESHOLD = 0.75
    
    #키워드 유사도 기준
    KEYWORD_SIMILARITY_THRESHOLD = 0.92  #실험해보면서 조정 필요
    
    #신뢰도 점수 가중치 및 뉴스사 수
    CONTENT_WEIGHT = 0.35 #자체평가 점수 가중치
    CROSS_CHECK_WEIGHT = 1.0 - CONTENT_WEIGHT #중복도 점수 가중치
    CROSS_CHECK_MAX = 4  #크롤러에서 받아서 수정