from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.infra.config.setting import get_settings
import src.infra.proxy.forwarder as proxy_module
from src.infra.middleware.auth_middleware import AuthMiddleware
from src.infra.proxy.forwarder import proxy_request

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    proxy_module.client = httpx.AsyncClient(timeout=settings.default_timeout)
    yield
    await proxy_module.client.aclose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

#서버 상태 확인용 api
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print("REQUEST:", request.method, request.url)
    response = await call_next(request)
    print("RESPONSE:", response.status_code)
    print("HEADER:", response.headers)
    print("======================================================")
    return response
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def catch_all(request: Request, full_path: str):
    return await proxy_request(request)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("src.infra.main:app", host="0.0.0.0", port=8080, workers=1, log_level="info", reload=True)