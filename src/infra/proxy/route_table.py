from src.infra.config.setting import get_settings

settings = get_settings()


PATH_REWRITES: dict[str, tuple[str, str]] = {
    "/news/my-interest": (settings.llm_api_url, "/hashtag/search_front"),
}

PUBLIC_ROUTES: dict[str, str] = {
    "/user":          settings.user_api_url,
    "/subscriptions": settings.sns_api_url,
    "/TODO":          settings.user_api_url,
    "/hashtag":       settings.user_api_url,
    "/news/daily":    settings.llm_api_url,
    "/article/articles_ids_front": settings.crawler_api_url,
}

#주소 url에 맞게 수정
def resolve_target(path: str) -> tuple[str, str] | None:
    if path in PATH_REWRITES:
        return PATH_REWRITES[path]

    best_match: str | None = None
    best_prefix_length = -1

    for prefix, base_url in PUBLIC_ROUTES.items():
        if path == prefix or path.startswith(prefix + "/"):
            if len(prefix) > best_prefix_length:
                best_match = base_url
                best_prefix_length = len(prefix)

    if best_match is None:
        return None

    return best_match, path