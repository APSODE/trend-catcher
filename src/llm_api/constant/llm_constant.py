class LLMConstant:
    BASE_URL = "https://integrate.api.nvidia.com/v1"

    #추출
    EXTRACTION_URL = BASE_URL + "/chat/completions"
    EXTRACTION_MODEL = "nvidia/nemotron-3-nano-30b-a3b"
    EXTRACTION_TIMEOUT = 300
    PROMPT_TEMPLATE = """
다음 뉴스 기사를 읽고, 아래 지침에 따라 핵심 키워드와 주제, 신뢰도를 추출해줘
#지침
- keywords는 기사의 핵심 명사(지명, 인물, 기관, 사건명 등) 3~5개 
- keywords는 고유명사 우선. 일반명사는 구체적인 형태로 (예: "축제"❌ → "국제축구축제"⭕) 띄어쓰기 없이 붙여쓸 것
- topic은 이 기사가 다루는 핵심 사건을 20자 내외로 간결하게 (부가 정보 제외)
- content_score는 이 기사가 얼마나 사실 위주로 작성되었는지 0.0 ~ 1.0으로 평가 (구체적 수치, 기관명, 인용이 있으면 높게, 추측성 표현이 많으면 낮게)
- 반드시 아래 형식의 JSON만 출력할 것. 설명이나 다른 텍스트 덧붙이기 절대 금지

#출력양식
{{"keywords": ["인천", "송도", "축구축제", "손흥민"], "topic": "인천 송도에서 개최된 축구축제에 손흥민이 참여했다", "content_score": 0.8}}

#기사
제목: {title}
본문: {content}
"""

    #임베딩
    EMBEDDING_URL = BASE_URL + "/embeddings"
    EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-1b-v2"
    EMBEDDING_TIMEOUT = 30
    
    #재시도
    EXTRACTION_RETRY_ATTEMPTS = 2
    RETRY_BASE_DELAY = 1.0