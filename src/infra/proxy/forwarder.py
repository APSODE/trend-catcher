import logging

import httpx

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from src.infra.config.setting import get_settings
from src.infra.proxy.route_table import resolve_target


logger = logging.getLogger(__name__)
settings = get_settings()

EXCLUDED_RESPONSE_HEADERS = {
    "content-encoding", "content-length", "transfer-encoding", "connection"
}

client: httpx.AsyncClient | None = None


async def proxy_request(request: Request) -> Response:
    if client is None:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "message": "HTTP client가 초기화되지 않았습니다"}
        )
    path = request.url.path

    target_base = resolve_target(path)
    if target_base is None:
        return JSONResponse(
            status_code=404,
            content={"detail": "Not Found", "message": "잘못된 접근 경로입니다"})

    target_url = f"{target_base}{path}"
    print("path:", path)
    print("target_base:", target_base)
    print("target_url:", target_url)
    forward_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }

    #llm api인경우 추가시간
    timeout = settings.llm_api_timeout if target_base == settings.llm_api_url else settings.default_timeout
    forward_params = {
        k: v
        for k, v in request.query_params.multi_items()
        if k != "_full_path"
    }
    try:
        upstream_request = client.build_request(
            method=request.method,
            url=target_url,
            headers=forward_headers,
            params=forward_params,
            content=await request.body(),
            timeout=timeout,
        )
        print("=== PROXY ===")
        print("method:", request.method)
        print("target_url:", target_url)
        print("query_params:", dict(request.query_params))
        print("body:", await request.body())
        upstream_response = await client.send(upstream_request)
    except httpx.ConnectError:
        return JSONResponse(
            status_code=502,
            content={"detail": "Upstream service unavailable", "message": "서버가 비활성화 상태입니다"})
    except httpx.TimeoutException:
        return JSONResponse(
            status_code=504,
            content={"detail": "Upstream service timeout", "message": "시간이 초과되었습니다"})

    response_headers = {
        k: v for k, v in upstream_response.headers.items()
        if k.lower() not in EXCLUDED_RESPONSE_HEADERS
    }

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=response_headers,
    )