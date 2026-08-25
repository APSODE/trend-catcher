from src.infra.config.setting import get_settings

settings = get_settings()

#외부에서 접근하는 라우터 추가시 여기 추가
PUBLIC_ROUTES: dict[str, str] = {
    "/user":          settings.user_api_url,
    "/subscriptions": settings.sns_api_url,
    "/TODO":          settings.user_api_url,
    "/hashtag":       settings.user_api_url,
    "/news/daily":    settings.llm_api_url
}

#주소 url에 맞게 수정
def resolve_target(path: str) -> str | None:

    for prefix, base_url in PUBLIC_ROUTES.items():
        if path == prefix or path.startswith(prefix + "/"):
            return base_url
    return None