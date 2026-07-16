from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.crawler_api.route import ArticleRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ArticleRouter.router)