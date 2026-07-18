from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.crawler_api.route import article_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_router.router)