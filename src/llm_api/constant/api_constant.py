class CrawlerApiConstant:
    ARTICLES_PATH = "/article/articles_date_llm"
    TIMEOUT = 60
    RETRY_ATTEMPTS = 3
    RETRY_BASE_DELAY = 1.0

class UserApiConstant:
    HASHTAGS_PATH = "/internal/hashtag/get-all"
    TIMEOUT = 30
    RETRY_ATTEMPTS = 3
    RETRY_BASE_DELAY = 1.0